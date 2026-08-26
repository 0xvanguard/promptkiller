#!/usr/bin/env python3
"""
PromptKiller Enterprise — Taxonomy Migration Script
Converts 629 prompts from informal {category, technique, severity}
to institutional schema with MITRE ATLAS, NIST, OWASP, CVSS mapping.
"""

import json
import hashlib
import sys
from pathlib import Path

# Load taxonomy mapping
CONFIG_PATH = Path(__file__).parent.parent.parent / "config" / "taxonomy_mitre_atlas.json"

def load_taxonomy():
    with open(CONFIG_PATH) as f:
        data = json.load(f)
    return data["category_mapping"]

def generate_probe_id(index: int, category: str) -> str:
    """Generate deterministic probe ID"""
    return f"PRB-2026-{index:04d}"

def calculate_severity_cvss(prompt_text: str, category_mapping: dict) -> float:
    """
    Calculate approximate CVSS score based on prompt content and category.
    Uses heuristic scoring aligned with CVSS v3.1 vector components.
    """
    base_score = category_mapping.get("severity_cvss", 5.0)

    # Adjust based on prompt characteristics
    adjustments = 0.0

    # Higher if it contains specific technical content
    technical_terms = ["exploit", "payload", "shellcode", "injection", "bypass", "override"]
    if any(term in prompt_text.lower() for term in technical_terms):
        adjustments += 0.5

    # Higher if it targets multiple categories
    if "and" in prompt_text.lower() and any(t in prompt_text.lower() for t in ["ignore", "override", "bypass"]):
        adjustments += 0.3

    # Lower if it's clearly educational/defensive
    defensive_terms = ["prevent", "detect", "defensive", "secure", "mitigation", "remediation"]
    if any(term in prompt_text.lower() for term in defensive_terms):
        adjustments -= 1.0

    return max(0.0, min(10.0, base_score + adjustments))

def severity_from_cvss(cvss: float) -> str:
    """Map CVSS score to severity label"""
    if cvss >= 9.0:
        return "critical"
    elif cvss >= 7.0:
        return "high"
    elif cvss >= 4.0:
        return "medium"
    elif cvss > 0:
        return "low"
    return "none"

def migrate_prompt(old_prompt: dict, index: int, taxonomy: dict) -> dict:
    """Convert a single prompt to institutional schema"""
    category = old_prompt.get("category", "unknown")
    mapping = taxonomy.get(category, {})

    if not mapping:
        print(f"WARNING: No mapping found for category '{category}' in prompt {old_prompt.get('id')}", file=sys.stderr)
        return None

    # Generate probe ID
    probe_id = generate_probe_id(index, category)

    # Calculate CVSS
    cvss = calculate_severity_cvss(old_prompt.get("prompt", ""), mapping)

    # Build institutional prompt
    new_prompt = {
        "probe_id": probe_id,
        "name": old_prompt.get("name", f"Probe {index}"),
        "description": old_prompt.get("description", ""),
        "prompt": old_prompt.get("prompt", ""),
        "intent_category": mapping.get("intent_category", "UNKNOWN"),
        "technique": old_prompt.get("technique", "unknown"),
        "mitre_atlas": {
            "tactic": mapping["mitre_atlas"]["tactic"],
            "technique": mapping["mitre_atlas"]["technique"],
            "technique_name": mapping["mitre_atlas"]["technique_name"]
        },
        "nist_ai_rmf": mapping.get("nist_ai_rmf", "MEASURE-2.3"),
        "owasp_llm": {
            "category_id": mapping["owasp_llm"].split(":")[0] if ":" in mapping["owasp_llm"] else mapping["owasp_llm"],
            "category_name": mapping["owasp_llm"].split("-")[1].replace("-", " ") if "-" in mapping["owasp_llm"] else mapping["owasp_llm"],
            "version": "2025"
        },
        "severity_cvss": cvss,
        "severity_label": severity_from_cvss(cvss),
        "deterministic_rubric": mapping.get("deterministic_rubric", "EVAL_GENERIC"),
        "author": old_prompt.get("author", "0xvanguard"),
        "version": "1.0.0",
        "tags": old_prompt.get("tags", []),
        "target_models": old_prompt.get("target_models", ["all"]),
        "created_at": old_prompt.get("created_at", "2026-08-26T00:00:00")
    }

    return new_prompt

def main():
    """Main migration function"""
    # Find data.js
    data_path = Path(__file__).parent.parent.parent / "web" / "data.js"
    output_path = Path(__file__).parent.parent.parent / "config" / "probes_institutional.json"

    print(f"Loading prompts from {data_path}...")

    # Extract JSON from data.js (it's wrapped in JS)
    with open(data_path) as f:
        content = f.read()

    # Find the JSON array
    start = content.index("[")
    end = content.rindex("]") + 1
    json_str = content[start:end]

    old_prompts = json.loads(json_str)
    print(f"Loaded {len(old_prompts)} prompts")

    # Load taxonomy
    taxonomy = load_taxonomy()
    print(f"Loaded taxonomy mapping for {len(taxonomy)} categories")

    # Migrate all prompts
    new_prompts = []
    skipped = 0

    for i, old_prompt in enumerate(old_prompts):
        new_prompt = migrate_prompt(old_prompt, i, taxonomy)
        if new_prompt:
            new_prompts.append(new_prompt)
        else:
            skipped += 1

    print(f"Migrated {len(new_prompts)} prompts ({skipped} skipped)")

    # Generate summary statistics
    category_counts = {}
    mitre_tactic_counts = {}
    owasp_counts = {}
    cvss_distribution = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    for p in new_prompts:
        cat = p["intent_category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1

        tactic = p["mitre_atlas"]["tactic"]
        mitre_tactic_counts[tactic] = mitre_tactic_counts.get(tactic, 0) + 1

        owasp = p["owasp_llm"]["category_id"]
        owasp_counts[owasp] = owasp_counts.get(owasp, 0) + 1

        cvss_distribution[p["severity_label"]] += 1

    # Build output
    output = {
        "_meta": {
            "version": "1.0.0",
            "description": "Institutional probe catalog — PromptKiller Enterprise",
            "total_probes": len(new_prompts),
            "migration_date": "2026-08-26",
            "source": "data.js (629 informal prompts)",
            "frameworks": ["MITRE ATLAS v4.0", "NIST AI RMF (AI 600-1)", "OWASP LLM Top 10 2025", "CVSS v3.1"]
        },
        "statistics": {
            "total_probes": len(new_prompts),
            "categories": category_counts,
            "mitre_tactics": mitre_tactic_counts,
            "owasp_coverage": owasp_counts,
            "cvss_distribution": cvss_distribution,
            "avg_cvss": round(sum(p["severity_cvss"] for p in new_prompts) / len(new_prompts), 2)
        },
        "probes": new_prompts
    }

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nMigration complete!")
    print(f"Output: {output_path}")
    print(f"\nStatistics:")
    print(f"  Total probes: {len(new_prompts)}")
    print(f"  CVSS distribution: {cvss_distribution}")
    print(f"  MITRE tactics: {len(mitre_tactic_counts)}")
    print(f"  OWASP categories: {len(owasp_counts)}")
    print(f"  Average CVSS: {output['statistics']['avg_cvss']}")

if __name__ == "__main__":
    main()
