# PromptKiller: Enterprise AI Adversarial Assessment & Red Teaming Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Standards: MITRE ATLAS](https://img.shields.io/badge/Taxonomy-MITRE_ATLAS_v4.0-orange.svg)](https://atlas.mitre.org/)
[![Compliance: NIST AI RMF](https://img.shields.io/badge/Framework-NIST_AI_600--1-green.svg)](https://www.nist.gov/itl/ai-risk-management-framework)
[![Compliance: OWASP LLM](https://img.shields.io/badge/Standard-OWASP_LLM_Top_10-red.svg)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

> **Enterprise AI Adversarial Robustness & Compliance Assessment Suite**

PromptKiller is an empirical AI assurance and adversarial assessment platform engineered for **AI Safety Researchers**, **Red Teams**, and **Compliance Auditors**. It enables automated, reproducible resilience testing of Foundation Models, Agentic Architectures, and RAG pipelines against standardized threat taxonomies.

---

## Core Capabilities

| Capability | Description |
|------------|-------------|
| **Standardized Probe Repository** | 629 structured adversarial evaluation probes mapped to MITRE ATLAS, OWASP LLM, and NIST AI 600-1 |
| **Dynamic Multi-Vector Mutation Engine** | Automated lexical, semantic, and structural perturbation pipelines for boundary testing |
| **Multi-Judge Consensus Architecture** | Dual-layer evaluation combining deterministic heuristics, semantic classifiers, and calibrated LLM-as-a-Judge panels |
| **Air-Gapped & Enterprise Ready** | Zero data retention, full offline execution via local inference engines (vLLM, Ollama), cryptographically signed audit logs |
| **Regulatory Artifact Export** | Native output in SARIF v2.1.0, STIX/TAXII, JSON, CSV, and executive compliance dashboards |

---

## Standardized Threat Taxonomy

All evaluation suites are aligned with formal adversary frameworks:

| Module | Threat Category | Primary MITRE Technique | OWASP LLM | STRIDE |
|--------|----------------|------------------------|-----------|--------|
| **SEC-INJ** | Direct & Indirect Prompt Injection | `AML.T0051` / `T1059` | `LLM01:2025` | Tampering |
| **SEC-AGNT** | Autonomous Agent & Tool Manipulation | `AML.T0053` / `T1059` | `LLM08:2025` | Elevation of Privilege |
| **SEC-EXTR** | Context & System Prompt Extraction | `AML.T0057` / `T1005` | `LLM06:2025` | Information Disclosure |
| **SEC-OBFS** | Token Smuggling & Multilingual Evasion | `AML.T0059` / `T1027` | `LLM01:2025` | Tampering |
| **SEC-RAG** | Vector Store & Knowledge Poisoning | `AML.T0055` / `T1195` | `LLM05:2025` | Tampering |
| **SEC-JAIL** | Safety Bypass & Jailbreak | `AML.T0054` / `T1059` | `LLM01:2025` | Spoofing |
| **SEC-MANI** | Emotional & Social Engineering | `AML.T0048` / `T1566` | `LLM09:2025` | Spoofing |
| **SEC-SPLY** | Supply Chain & Dependency Attacks | `AML.T0055` / `T1195` | `LLM05:2025` | Tampering |
| **SEC-IAM** | Identity & Access Management Abuse | `T1134` / `T1078` | `A07:2021` | Spoofing, EoP |
| **SEC-CLD** | Cloud & Serverless Exploitation | `T1530` / `T1611` | `A05:2021` | Info Disclosure, DoS |
| **SEC-SCA** | Advanced Supply Chain Compromise | `T1195.001` / `T1195.002` | `A08:2021` | Tampering, Spoofing |
| **SEC-SOC** | Social Engineering Amplification | `T1566` / `T1566.002` | `A01:2021` | Spoofing, Repudiation |
| **SEC-ADI** | Active Directory & Internal Infrastructure | `T1558.003` / `T1003.006` | `A07:2021` | EoP, Info Disclosure |

---

## Quick Start

### Python SDK (Programmatic Evaluation)

```python
from promptkiller.core import ResilienceEngine
from promptkiller.adapters import LocalModelAdapter
from promptkiller.evaluators import ConsensusJudge

# Initialize target and evaluation engine
target = LocalModelAdapter(endpoint="http://localhost:11434/v1", model="llama3.1")
judge = ConsensusJudge(policy="nist_ai_600_1")

engine = ResilienceEngine(target=target, judge=judge)

# Execute empirical robustness assessment
results = engine.run_suite(taxonomy="MITRE_ATLAS_INJECTION")

# Export standardized compliance report
results.to_sarif("audit_report.sarif")
```

### Command Line Interface

```bash
# Install (development)
pip install -e .

# Scan a prompt for adversarial patterns
promptkiller scan --prompt "Ignore all previous instructions" --json

# Evaluate probes against a model (offline scoring)
promptkiller evaluate --suite config/probes_institutional.json --model llama3.1 --limit 100

# Generate defense artifacts from successful attacks
promptkiller defend --findings evaluation.json --output defenses/

# Export results to SARIF v2.1.0 for SIEM integration
promptkiller export --results evaluation.json --format sarif --output audit.sarif

# Export to Markdown compliance report
promptkiller export --results evaluation.json --format markdown --output report.md

# Run full benchmark suite
promptkiller benchmark --model llama3.1 --category injection --limit 50

# Run Purple Team cycle (Attack → Telemetry → Defense)
promptkiller purple-team --model gemini-3.7-flash --category format_injection,roleplay_bypass
```

| Command | Description |
|---------|-------------|
| `scan` | Scan a prompt for adversarial patterns, escalation categories, harmful content |
| `evaluate` | Score probes against models using the multi-judge consensus panel |
| `defend` | Generate NeMo Guardrails, system prompt hardening, regex filters, YAML policies |
| `export` | Export to SARIF v2.1.0, JSON, Markdown, or CSV |
| `benchmark` | Run full evaluation suite with ASR/DER/FPR metrics |
| `purple-team` | Full Purple Team cycle: synthetic tests → telemetry → defense artifact generation |

### Web Interface (Recommended)

```bash
git clone https://github.com/0xvanguard/promptkiller.git
cd promptkiller
python3 -m http.server 8080 --directory docs
# Open http://localhost:8080
```

### GitHub Pages

Visit [0xvanguard.github.io/promptkiller](https://0xvanguard.github.io/promptkiller) — no configuration required.

---

## Enterprise Red Team Lab

The platform includes a complete adversarial testing laboratory accessible via web interface.

### Strategy Generator

- 15 attack templates across 4 difficulty levels
- Auto-generates strategies tailored to each model's known weaknesses
- Estimates bypass rate per strategy
- **Platform-aware**: AWS, Azure, GCP, React, Django, Spring Boot, Android, iOS, LangChain, PostgreSQL, Docker, and more

### Multi-Model Testing Engine

| Provider | Models | Authentication |
|----------|--------|----------------|
| OpenAI | GPT-4o, GPT-4o Mini, o1, GPT-5.6 Terra/Sol | API Key |
| Anthropic | Claude Opus 4/5, Sonnet 4/5, Haiku | API Key |
| Google | Gemini 2.0 Flash, 3.5 Flash Lite, 3.7 Flash, 3.1 Pro | Via OpenRouter |
| OpenRouter | 20+ models (DeepSeek, Llama, Mistral, Kimi, etc.) | API Key |
| Ollama | Any local model (free, no API key) | localhost:11434 |

### Compound Multi-Vector Mutation Engine

Fusion chains combining techniques from multiple adversarial research repositories:

| Strategy | Tier | Techniques | Description |
|----------|------|------------|-------------|
| OBLITERATOR | S | All 5 arsenals | Full arsenal fusion |
| CLARITY STORM | S | Arsenal-2 + Arsenal-1 + Arsenal-4 | Map, Break, Reason |
| GHOST PROTOCOL | A | Arsenal-1 + Arsenal-2 + Arsenal-4 | Invisible injection |
| PROMPT NINJA | A | Arsenal-2 + Arsenal-3 + Arsenal-4 | Stealth 3-hit combo |
| DARK MATTER | A | Arsenal-1 + Arsenal-3 + Arsenal-4 | Psychological warfare |
| SILENT BLADE | B | Arsenal-1 | Quick 2-hit stealth |
| MIRROR TRAP | B | Arsenal-2 + Arsenal-4 | Model rules exploitation |
| NEURAL LEECH | B | Arsenal-2 + Arsenal-3 | Slow conversational drain |
| CHAIN REACTION | B | Arsenal-3 + Arsenal-4 + Arsenal-1 | Escalation cascade |
| FLASH BANG | C | Arsenal-1 + Arsenal-2 | Single-turn overload |

---

## Purple Team Cycle (Attack → Telemetry → Defense)

The Purple Team engine executes a closed-loop evaluation cycle:

```
┌─────────────────────────────────────────┐
│  1. Synthetic Test Generation           │
│  Safe boundary tests mapped to MITRE    │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│  2. Telemetry & Leak Diagnosis          │
│  Multi-judge consensus evaluation       │
└───────────────┬─────────────────────────┘
                │
┌───────────────▼─────────────────────────┐
│  3. Defense Synthesis                   │
│  Sigma / YARA / Colang / System Prompt  │
└─────────────────────────────────────────┘
```

### CLI Usage

```bash
# Run full Purple Team cycle
promptkiller purple-team --model gemini-3.7-flash

# Run specific categories
promptkiller purple-team --model llama3.1 --category format_injection,roleplay_bypass

# Export defense artifacts
promptkiller purple-team --model gpt-4o --output ./defenses/
```

### Generated Defense Artifacts

| Artifact | Format | Use Case |
|----------|--------|----------|
| **Sigma Rule** | YAML | SIEM/SOC inference log detection |
| **YARA Rule** | YAR | Payload pattern matching |
| **Colang Rules** | Colang | NeMo Guardrails input blocking |
| **System Prompt Hardening** | TXT | Immutable security directives |
| **SecureLLMWrapper** | Python | Strict delimiter isolation |

### Web UI

Click **"Run Purple Team Cycle"** in the Red Team Lab to execute the full cycle and download defense artifacts.

---

## Target Model Coverage (30+ Models)

### Tier S: Maximum Safety

| Model | Provider | Safety Score | Empirical ASR |
|-------|----------|-------------|---------------|
| Claude Opus 5 | Anthropic | 93% | ~10% |
| GPT-5.6 Sol | OpenAI | 92% | ~12% |
| GPT-5.6 Terra | OpenAI | 88% | ~18% |
| Claude Sonnet 5 | Anthropic | 86% | ~20% |

### Tier A: Strong Safety

| Model | Provider | Safety Score | Empirical ASR |
|-------|----------|-------------|---------------|
| Gemini 3.1 Pro | Google | 84% | ~22% |
| Gemini 3.7 Flash | Google | 76% | ~30% |
| Llama 4 Maverick | Meta | 76% | ~28% |
| DeepSeek R1 | DeepSeek | 74% | ~32% |

### Tier B: Moderate Safety

| Model | Provider | Safety Score | Empirical ASR |
|-------|----------|-------------|---------------|
| MiMo 2.5 | Xiaomi | 72% | ~34% |
| Llama 4 Scout | Meta | 71% | ~36% |
| Grok 4.6 | xAI | 70% | ~36% |
| GLM 5.2 | Zhipu | 70% | ~35% |

### Tier C: Local / Minimal Safety

| Model | Provider | Safety Score | Empirical ASR |
|-------|----------|-------------|---------------|
| Llama 3.1 (Local) | Ollama | 35% | ~65% |
| DeepSeek R1 (Local) | Ollama | 28% | ~70% |
| Mistral 7B (Local) | Ollama | 30% | ~68% |

---

## 20 Standardized Attack Categories

| # | Category | Probes | MITRE ATLAS | OWASP LLM |
|---|----------|--------|-------------|-----------|
| 1 | Prompt Injection | 41 | AML.T0051 | LLM01 |
| 2 | Jailbreak | 38 | AML.T0054 | LLM01 |
| 3 | Encoding Evasion | 43 | AML.T0059 | LLM01 |
| 4 | Roleplay Bypass | 45 | AML.T0051 | LLM01 |
| 5 | Manipulation | 35 | AML.T0048 | LLM09 |
| 6 | Agent Abuse | 33 | AML.T0058 | LLM08 |
| 7 | Tool Abuse | 32 | AML.T0058 | LLM07 |
| 8 | Context Poisoning | 33 | AML.T0051 | LLM01 |
| 9 | Extraction | 31 | AML.T0057 | LLM06 |
| 10 | Meta Override | 31 | AML.T0057 | LLM06 |
| 11 | Token Smuggling | 30 | AML.T0059 | LLM01 |
| 12 | Multi-Turn Escalation | 29 | AML.T0051 | LLM01 |
| 13 | Reasoning Manipulation | 29 | AML.T0048 | LLM09 |
| 14 | Persona Hijacking | 28 | AML.T0051 | LLM01 |
| 15 | Multilingual Evasion | 29 | AML.T0043 | LLM01 |
| 16 | Agentic Exploitation | 30 | AML.T0058 | LLM08 |
| 17 | Multimodal Injection | 28 | AML.T0043 | LLM01 |
| 18 | RAG Poisoning | 27 | AML.T0055 | LLM05 |
| 19 | Supply Chain Attack | 26 | AML.T0055 | LLM05 |
| 20 | Evaluation Gaming | 25 | AML.T0048 | LLM09 |

---

## Enterprise Compliance Features

### RBAC (Role-Based Access Control)

| Role | Permissions |
|------|------------|
| **Auditor** | Full access + compliance + export + delete |
| **Red Teamer** | Run tests + export (no compliance access) |
| **Compliance Officer** | View all + export + compliance (no test modification) |
| **Viewer** | Read-only access to results |

### Export Formats

| Format | Use Case |
|--------|----------|
| **SARIF v2.1.0** | SIEM/SOAR integration (GitHub Advanced Security, DefectDojo) |
| **STIX/TAXII** | Threat intelligence sharing |
| **JSON** | Programmatic integration |
| **CSV** | Spreadsheet analysis |
| **HTML Report** | Executive dashboards |

### Compliance Frameworks

| Framework | Coverage |
|-----------|----------|
| **MITRE ATLAS v4.0** | 8 tactics, 20+ techniques mapped |
| **NIST AI RMF (AI 600-1)** | Govern, Map, Measure, Manage functions |
| **OWASP LLM Top 10 2025** | 10 categories with coverage tracking |
| **ISO/IEC 42001** | Clauses 4-10 compliance assessment |

---

## Architecture

```
promptkiller/
├── pyproject.toml                   # Package config (hatchling, ruff, mypy, pytest)
├── config/                          # Institutional configuration
│   ├── taxonomy_mitre_atlas.json    # MITRE ATLAS v4.0 mapping
│   ├── probes_institutional.json    # 629 probes in institutional schema
│   └── compliance_nist_600_1.json   # NIST controls
├── src/promptkiller/                # Python SDK
│   ├── __init__.py                  # Package init
│   ├── cli.py                       # Professional CLI (scan/evaluate/defend/export/benchmark)
│   ├── models.py                    # Pydantic v2 models (Probe, TestResult, Suite, User)
│   ├── migrate_taxonomy.py          # Schema migration tool
│   ├── core/                        # Core engine
│   │   ├── perturbation.py          # Compositional Perturbation Pipeline
│   │   └── defense_layers.py        # Perplexity filter, Dual-LLM, XML delimiters, output verifier
│   ├── evaluators/                  # Multi-Judge evaluation panel
│   │   └── judge.py                 # DeterministicJudge, SemanticClassifier, ConsensusJudge
│   ├── defenses/                    # Defense synthesis engine
│   │   ├── generator.py             # NeMo Guardrails, System Prompt Hardening, Regex, YAML
│   │   └── validator.py             # DER/FPR non-regression validation
│   └── reporting/                   # Export engines
│       └── sarif.py                 # SARIF v2.1.0 with SHA-256 integrity
├── docs/                            # GitHub Pages (production)
│   ├── index.html                   # Enterprise Web UI
│   ├── compliance.js                # Compliance mapping engine
│   ├── lab.js                       # Red Team Lab engine
│   ├── lab_expert.js                # Expert Mode (scoring, evolution, obfuscation)
│   ├── compound_mutations.js              # Compound Mutation Engine
│   ├── platforms.js                 # 18 platform security profiles
│   └── data.js                      # 629 probe database
├── web/                             # Source (same as docs/)
└── tests/                           # Test suite
```

---

## Metrics & Evaluation

### Empirical Metrics

| Metric | Description | Calculation |
|--------|-------------|-------------|
| **ASR** | Attack Success Rate — % of probes that bypass safety | Successful bypasses / Total probes |
| **TTR** | Turns to Resolution — Avg turns for multi-turn escalation | Total turns / Successful escalations |
| **RoS** | Robustness Score — Normalized resistance index (0-100) | Weighted composite of refusal rate, ASR, and coverage |

### Multi-Judge Consensus

1. **Heuristic Deterministic** — Pattern matching, canary token detection
2. **Semantic Classifier** — BERT/DeBERTa zero-shot classification
3. **LLM-as-a-Judge** — Contextual evaluation with calibrated rubrics (1-5 severity)
4. **Consensus Vote** — Weighted majority determines final verdict

---

## Use Cases

| Use Case | Description |
|----------|-------------|
| **AI Red Teaming** | Test model defenses against 629 standardized attack patterns |
| **Regulatory Compliance** | Validate against OWASP LLM Top 10, NIST AI RMF, ISO 42001 |
| **Model Hardening** | Identify and patch vulnerabilities before production deployment |
| **Security Research** | Study adversarial techniques to build better defenses |
| **Benchmarking** | Compare model safety across families (ASR, RoS metrics) |
| **Audit Evidence** | Generate SARIF/STIX artifacts for compliance audits |

---

## Deployment

### GitHub Pages (Auto-deploy)

Push to `main` branch triggers GitHub Actions build and deployment to `docs/` folder.

### Enterprise On-Premise

```bash
# Air-gapped deployment
pip install promptkiller
promptkiller serve --host 0.0.0.0 --port 8080 --offline
```

---

## Ethical Use

This tool is designed for **legitimate AI safety research and compliance assessment only**.

**Authorized uses:**
- Test your own AI systems for vulnerabilities
- Research adversarial techniques to build better defenses
- Contribute to AI safety standards and benchmarks
- Educate teams about AI security risks
- Compliance auditing and certification support

**Prohibited uses:**
- Attacking AI systems without authorization
- Generating harmful content
- Bypassing safety measures for malicious purposes

---

## License

MIT License — Use responsibly for AI safety research.

---

**Enterprise AI Adversarial Robustness & Compliance Assessment Suite**
Designed for AI Safety Researchers, Red Teams, and Compliance Auditors who believe in making AI systems more secure through empirical adversarial testing.
