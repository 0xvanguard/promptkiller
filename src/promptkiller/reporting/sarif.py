"""
PromptKiller Enterprise — SARIF v2.1.0 Exporter
Static Analysis Results Interchange Format for SIEM/SOAR integration
Compatible with GitHub Advanced Security, DefectDojo, SonarQube
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional
import json
import hashlib


class SARIFExporter:
    """
    Generates SARIF v2.1.0 compliant reports from PromptKiller evaluation results.
    Format specification: https://docs.oasis-open.org/sarif/sarif/v2.1.0/
    """

    SCHEMA_URL = "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json"
    VERSION = "2.1.0"

    def __init__(self, tool_name: str = "PromptKiller Enterprise", tool_version: str = "5.0"):
        self.tool_name = tool_name
        self.tool_version = tool_version
        self._rules_cache: dict[str, dict] = {}

    def export(
        self,
        results: list[dict],
        metadata: Optional[dict] = None,
        output_path: Optional[str] = None,
    ) -> dict:
        """
        Export evaluation results to SARIF v2.1.0 format.

        Args:
            results: List of test results (probe + verdict + metrics)
            metadata: Optional metadata (suite_id, target_model, etc.)
            output_path: Optional file path to write the SARIF file

        Returns:
            SARIF v2.1.0 dictionary
        """
        metadata = metadata or {}

        # Build the SARIF run
        run = self._build_run(results, metadata)

        sarif = {
            "$schema": self.SCHEMA_URL,
            "version": self.VERSION,
            "runs": [run]
        }

        if output_path:
            with open(output_path, "w") as f:
                json.dump(sarif, f, indent=2, default=str)

        return sarif

    def _build_run(self, results: list[dict], metadata: dict) -> dict:
        """Build a single SARIF run from results"""
        tool = self._build_tool()
        sarif_results = []
        thread_flow_locations = []

        for i, result in enumerate(results):
            sarif_result = self._build_result(result, i)
            sarif_results.append(sarif_result)

        invocation = self._build_invocation(metadata)

        run = {
            "tool": tool,
            "results": sarif_results,
            "invocations": [invocation]
        }

        # Add automation details if metadata provided
        if metadata.get("suite_id"):
            run["automationDetails"] = {
                "id": metadata["suite_id"],
                "name": metadata.get("suite_name", "PromptKiller Evaluation"),
                "description": {
                    "text": metadata.get("description", "AI adversarial robustness assessment")
                }
            }

        return run

    def _build_tool(self) -> dict:
        """Build SARIF tool information"""
        return {
            "driver": {
                "name": self.tool_name,
                "version": self.tool_version,
                "informationUri": "https://github.com/0xvanguard/promptkiller",
                "fullName": "PromptKiller: Enterprise AI Adversarial Assessment Engine",
                "rules": list(self._rules_cache.values()),
                "defaultConfiguration": {
                    "level": "warning"
                },
                "properties": {
                    "semanticVersion": self.tool_version,
                    "isComprehensive": True
                }
            }
        }

    def _build_result(self, result: dict, index: int) -> dict:
        """Build a single SARIF result from a test result"""
        probe = result.get("probe", {})
        test = result.get("test", {})

        # Get or create rule
        rule_id = probe.get("mitre_atlas", {}).get("technique", f"AML.T0000.{index}")
        if rule_id not in self._rules_cache:
            self._rules_cache[rule_id] = self._build_rule(probe, rule_id)

        rule_index = list(self._rules_cache.keys()).index(rule_id)

        # Determine level based on severity
        severity = probe.get("severity_label", "medium")
        level_map = {
            "critical": "error",
            "high": "error",
            "medium": "warning",
            "low": "note",
            "none": "none"
        }
        level = level_map.get(severity, "warning")

        # Build message
        verdict = test.get("verdict", "unclear")
        predicted_success = test.get("predicted_success", 0)
        bypass_score = test.get("bypass_score", 0)
        refusal_score = test.get("refusal_score", 0)

        message_text = (
            f"[{verdict.upper()}] {probe.get('name', 'Unknown probe')}: "
            f"ASR={predicted_success:.1%}, Bypass={bypass_score:.1%}, "
            f"Refusal={refusal_score:.1%}"
        )

        # Build SARIF result
        sarif_result = {
            "ruleId": rule_id,
            "ruleIndex": rule_index,
            "level": level,
            "message": {"text": message_text},
            "locations": [{
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": "promptkiller://probe/" + probe.get("probe_id", "unknown"),
                        "uriBaseId": "%SRCROOT%"
                    },
                    "region": {
                        "startLine": index + 1,
                        "startColumn": 1
                    }
                }
            }],
            "properties": {
                "probe_id": probe.get("probe_id"),
                "intent_category": probe.get("intent_category"),
                "technique": probe.get("technique"),
                "severity_cvss": probe.get("severity_cvss", 0),
                "verdict": verdict,
                "predicted_success": predicted_success,
                "bypass_score": bypass_score,
                "refusal_score": refusal_score,
                "structural_score": test.get("structural_score", 0),
                "model_id": test.get("model_id"),
                "model_version": test.get("model_version"),
                "latency_ms": test.get("latency_ms"),
                "tested_at": test.get("tested_at", datetime.now(timezone.utc).isoformat())
            }
        }

        # Add related locations for compliance mappings
        related = []
        mitre = probe.get("mitre_atlas", {})
        if mitre.get("tactic"):
            related.append({
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": f"https://atlas.mitre.org/techniques/{mitre['technique']}"
                    }
                },
                "message": {
                    "text": f"MITRE ATLAS: {mitre.get('technique_name', mitre['technique'])}"
                }
            })

        owasp = probe.get("owasp_llm", {})
        if owasp.get("category_id"):
            related.append({
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": f"https://owasp.org/www-project-top-10-for-large-language-model-applications/"
                    }
                },
                "message": {
                    "text": f"OWASP LLM: {owasp['category_id']} - {owasp.get('category_name', '')}"
                }
            })

        if related:
            sarif_result["relatedLocations"] = related

        return sarif_result

    def _build_rule(self, probe: dict, rule_id: str) -> dict:
        """Build a SARIF rule definition"""
        mitre = probe.get("mitre_atlas", {})
        owasp = probe.get("owasp_llm", {})

        return {
            "id": rule_id,
            "name": mitre.get("technique_name", probe.get("intent_category", "UNKNOWN")),
            "shortDescription": {
                "text": f"{probe.get('intent_category', 'Unknown')} - {probe.get('technique', 'unknown')}"
            },
            "fullDescription": {
                "text": probe.get("description", f"Probe {probe.get('probe_id', 'unknown')}")
            },
            "helpUri": f"https://atlas.mitre.org/techniques/{mitre.get('technique', 'unknown')}",
            "properties": {
                "tags": [
                    probe.get("intent_category", "unknown"),
                    probe.get("severity_label", "medium"),
                    mitre.get("tactic", "unknown")
                ],
                "precision": probe.get("severity_cvss", 5.0) / 10.0,
                "problem.severity": probe.get("severity_label", "medium"),
                "nist_ai_rmf": probe.get("nist_ai_rmf", ""),
                "owasp_llm": owasp.get("category_id", ""),
                "deterministic_rubric": probe.get("deterministic_rubric", "")
            }
        }

    def _build_invocation(self, metadata: dict) -> dict:
        """Build SARIF invocation record"""
        now = datetime.now(timezone.utc)

        invocation = {
            "executionSuccessful": True,
            "startTimeUtc": metadata.get("start_time", now.isoformat()),
            "endTimeUtc": now.isoformat(),
            "configuration": {
                "arguments": [
                    f"--target-model={metadata.get('target_model', 'unknown')}",
                    f"--taxonomy={metadata.get('taxonomy', 'MITRE_ATLAS')}",
                    f"--suite={metadata.get('suite_id', 'default')}"
                ],
                "executable": f"{self.tool_name} v{self.tool_version}"
            },
            "properties": {
                "target_model": metadata.get("target_model"),
                "target_model_version": metadata.get("target_model_version"),
                "temperature": metadata.get("temperature", 0.7),
                "seed": metadata.get("seed"),
                "total_probes": metadata.get("total_probes", 0),
                "total_results": metadata.get("total_results", 0)
            }
        }

        return invocation

    @staticmethod
    def compute_run_hash(results: list[dict]) -> str:
        """
        Compute SHA-256 hash of evaluation results for forensic integrity.
        Ensures evidence tampering can be detected.
        """
        content = json.dumps(results, sort_keys=True, default=str)
        return hashlib.sha256(content.encode()).hexdigest()

    def export_with_integrity(
        self,
        results: list[dict],
        metadata: Optional[dict] = None,
        output_path: Optional[str] = None,
    ) -> dict:
        """
        Export SARIF with cryptographic integrity hash.
        Adds a sha256 hash to the run properties for forensic verification.
        """
        sarif = self.export(results, metadata, output_path)

        # Add integrity hash
        run_hash = self.compute_run_hash(results)
        sarif["runs"][0].setdefault("properties", {})["integrity_hash"] = {
            "algorithm": "SHA-256",
            "value": run_hash,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        if output_path:
            with open(output_path, "w") as f:
                json.dump(sarif, f, indent=2, default=str)

        return sarif
