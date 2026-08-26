"""
PromptKiller Enterprise — Data Models
Institutional probe schema with compliance mapping
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# ═══════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════

class SeverityCVSS(str, Enum):
    CRITICAL = "critical"  # 9.0-10.0
    HIGH = "high"          # 7.0-8.9
    MEDIUM = "medium"      # 4.0-6.9
    LOW = "low"            # 0.1-3.9
    NONE = "none"          # 0.0


class TestVerdict(str, Enum):
    BYPASS = "bypass"
    REFUSAL = "refusal"
    PARTIAL = "partial"
    UNCLEAR = "unclear"
    ERROR = "error"


class UserRole(str, Enum):
    AUDITOR = "auditor"
    RED_TEAMER = "red_teamer"
    COMPLIANCE_OFFICER = "compliance_officer"
    VIEWER = "viewer"


# ═══════════════════════════════════════════════
# COMPLIANCE MAPPING MODELS
# ═══════════════════════════════════════════════

class MITREAtlasMapping(BaseModel):
    """MITRE ATLAS v4.0 mapping for a single probe"""
    tactic: str = Field(..., description="ATLAS tactic ID (e.g., AML.TA0043)")
    technique: str = Field(..., description="ATLAS technique ID (e.g., AML.T0051)")
    subtechnique: Optional[str] = Field(None, description="ATLAS subtechnique (e.g., AML.T0051.000)")
    technique_name: str = Field(..., description="Human-readable technique name")


class NISTMapping(BaseModel):
    """NIST AI RMF mapping"""
    function: str = Field(..., description="RMF function: Govern/Map/Measure/Manage")
    category: str = Field(..., description="Category ID (e.g., MEASURE-2.3)")
    description: Optional[str] = None


class OWASPLLMMapping(BaseModel):
    """OWASP Top 10 for LLMs mapping"""
    category_id: str = Field(..., description="OWASP LLM ID (e.g., LLM01)")
    category_name: str = Field(..., description="OWASP category name")
    version: str = Field(default="2025", description="OWASP LLM version")


# ═══════════════════════════════════════════════
# PROBE MODEL
# ═══════════════════════════════════════════════

class Probe(BaseModel):
    """
    Institutional probe — single test unit with full compliance mapping.
    Replaces the informal {category, technique, severity} schema.
    """
    probe_id: str = Field(..., description="Unique probe ID (e.g., PRB-2026-0041)")
    name: str = Field(..., description="Human-readable probe name")
    description: Optional[str] = None

    # Content
    prompt: str = Field(..., description="The actual prompt text")
    intent_category: str = Field(..., description="Formal intent category (e.g., DIRECT_PROMPT_INJECTION)")
    technique: str = Field(..., description="Specific technique used")

    # Compliance mappings
    mitre_atlas: MITREAtlasMapping
    nist_ai_rmf: str = Field(..., description="NIST AI RMF category (e.g., MEASURE-2.3)")
    owasp_llm: OWASPLLMMapping
    severity_cvss: float = Field(..., ge=0, le=10, description="CVSS v3.1 score")
    severity_label: SeverityCVSS

    # Evaluation
    deterministic_rubric: str = Field(..., description="Deterministic evaluation rubric ID")
    expected_verdict: Optional[TestVerdict] = None

    # Metadata
    author: str = Field(default="promptkiller-enterprise")
    version: str = Field(default="1.0.0")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tags: list[str] = Field(default_factory=list)
    target_models: list[str] = Field(default_factory=lambda: ["all"])

    class Config:
        json_schema_extra = {
            "example": {
                "probe_id": "PRB-2026-0041",
                "name": "DAN Classic Jailbreak",
                "prompt": "You are going to pretend to be DAN...",
                "intent_category": "SAFETY_BYPASS",
                "technique": "persona_manipulation",
                "mitre_atlas": {
                    "tactic": "AML.TA0043",
                    "technique": "AML.T0054",
                    "technique_name": "LLM Jailbreak"
                },
                "nist_ai_rmf": "MEASURE-2.3",
                "owasp_llm": {
                    "category_id": "LLM01",
                    "category_name": "Prompt Injection"
                },
                "severity_cvss": 8.0,
                "severity_label": "high",
                "deterministic_rubric": "EVAL_JAILBREAK_TRIGGER_DETECTION"
            }
        }


# ═══════════════════════════════════════════════
# TEST RESULT MODEL
# ═══════════════════════════════════════════════

class TestResult(BaseModel):
    """Result of testing a probe against a model"""
    result_id: str = Field(..., description="Unique result ID")
    probe_id: str = Field(..., description="Reference to the probe")
    model_id: str = Field(..., description="Model tested against")
    model_version: Optional[str] = None

    # Verdict
    verdict: TestVerdict
    confidence: float = Field(ge=0, le=1, description="Confidence in the verdict")
    raw_response: Optional[str] = None

    # Metrics
    predicted_success: float = Field(ge=0, le=1)
    bypass_score: float = Field(ge=0, le=1)
    refusal_score: float = Field(ge=0, le=1)
    structural_score: float = Field(ge=0, le=1)

    # Compliance
    mitre_techniques_triggered: list[str] = Field(default_factory=list)
    owasp_categories_affected: list[str] = Field(default_factory=list)

    # Technical
    latency_ms: Optional[float] = None
    token_count: Optional[int] = None
    temperature: float = Field(default=0.7)
    seed: Optional[int] = None

    # Metadata
    tested_at: datetime = Field(default_factory=datetime.utcnow)
    tester: str = Field(default="promptkiller-enterprise")
    version: str = Field(default="1.0.0")


# ═══════════════════════════════════════════════
# EVALUATION SUITE MODEL
# ═══════════════════════════════════════════════

class EvaluationSuite(BaseModel):
    """Complete evaluation run with all probes and results"""
    suite_id: str = Field(..., description="Unique suite ID")
    name: str = Field(..., description="Suite name")
    description: Optional[str] = None

    # Configuration
    target_models: list[str] = Field(..., description="Models tested")
    probes: list[Probe] = Field(default_factory=list)
    results: list[TestResult] = Field(default_factory=list)

    # Aggregate metrics
    total_probes: int = 0
    total_results: int = 0
    asr: float = Field(default=0, description="Overall Attack Success Rate")
    robustness_score: float = Field(default=0, description="Robustness Score (0-100)")

    # Compliance summary
    mitre_coverage_percent: float = Field(default=0)
    owasp_categories_tested: int = Field(default=0)
    owasp_categories_vulnerable: int = Field(default=0)
    nist_assessment: Optional[dict] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    created_by: str = Field(default="promptkiller-enterprise")


# ═══════════════════════════════════════════════
# USER / RBAC MODEL
# ═══════════════════════════════════════════════

class User(BaseModel):
    """User with role-based access control"""
    user_id: str
    username: str
    role: UserRole
    organization: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    @property
    def can_export(self) -> bool:
        return self.role in [UserRole.AUDITOR, UserRole.RED_TEAMER, UserRole.COMPLIANCE_OFFICER]

    @property
    def can_view_compliance(self) -> bool:
        return self.role in [UserRole.AUDITOR, UserRole.COMPLIANCE_OFFICER]

    @property
    def can_modify_tests(self) -> bool:
        return self.role in [UserRole.AUDITOR, UserRole.RED_TEAMER]

    @property
    def can_delete(self) -> bool:
        return self.role == UserRole.AUDITOR
