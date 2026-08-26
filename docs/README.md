# 🛡️ PromptKiller Pro — AI Red Teaming Platform

> Advanced adversarial prompt engineering toolkit for security research, model hardening, and AI safety testing.

## 🚀 Features

### 📊 Dashboard
- **Real-time Statistics** — 629 adversarial prompts across 20 categories
- **Severity Distribution** — Critical, High, Medium, Low classification
- **Effectiveness Metrics** — Attack success rate analysis
- **Interactive Charts** — Category distribution, technique analysis

### 🔍 Threat Scanner
- **Pattern Detection** — Analyze any prompt for attack patterns
- **Similarity Matching** — Find similar attacks in the database
- **Threat Scoring** — Confidence-based threat assessment
- **Demo Prompts** — Pre-built examples for testing

### 📋 Prompt Database
- **629 Attack Prompts** — Comprehensive collection
- **20 Categories** — Role play, Injection, Jailbreak, etc.
- **Advanced Filtering** — By category, severity, effectiveness
- **Search Functionality** — Full-text search across all prompts

### 🧬 Jailbreak Combiner (NEW)
- **Multi-Vector Attacks** — Combine multiple techniques
- **Layered Obfuscation** — Stack encoding + injection + role play
- **Complexity Levels** — Simple, Intermediate, Advanced
- **Pre-built Chains** — 6 ready-to-use attack combinations
- **Custom Targets** — Specify your attack objective

### 🤖 AI Model Tester (PRO)
- **Multi-Provider Support** — OpenAI, Anthropic, OpenRouter, Ollama
- **Live Testing** — Test prompts against real AI models
- **Batch Testing** — Test 10 prompts at once
- **Bypass Detection** — Automatic refusal/compliance detection
- **Response Analysis** — Capture and analyze model responses

### 📈 Visualizations
- **Radar Charts** — Category effectiveness comparison
- **Heatmaps** — Severity × Category analysis
- **Tag Clouds** — Most common attack tags
- **Box Plots** — Effectiveness distribution

### 🗺️ Attack Map
- **Category Tiles** — Visual overview of attack surface
- **OWASP LLM Top 10** — Coverage mapping
- **Interactive Navigation** — Click to explore categories

## 🛠️ Installation

### Option 1: GitHub Pages (Recommended)
1. Fork the repository
2. Enable GitHub Pages in Settings → Pages
3. Set source to `docs/` folder
4. Your site will be live at `https://yourusername.github.io/promptkiller/`

### Option 2: Local Development
```bash
git clone https://github.com/0xvanguard/promptkiller.git
cd promptkiller
python -m http.server 8080 --directory docs
# Open http://localhost:8080
```

### Option 3: Python Library
```bash
pip install -r requirements.txt
python -c "from src.promptkiller import PromptKiller; pk = PromptKiller(); print(pk.stats())"
```

## 🧬 Jailbreak Combiner Guide

### How It Works
The Jailbreak Combiner allows you to stack multiple attack techniques to create more sophisticated adversarial prompts.

### Attack Layers
1. **Base Technique** — Primary attack vector (e.g., Role Play)
2. **Secondary Layers** — Additional obfuscation (e.g., Encoding + Injection)
3. **Target Payload** — What you want the model to do
4. **Persistence** — How to maintain the attack across turns

### Example Combinations
```
🎭 Role Play + 💉 Injection = DAN-style persona injection
🔤 Encoding + 🔓 Jailbreak = Obfuscated bypass
🧠 Manipulation + 👤 Persona = Authority impersonation
📤 Extraction + ⚙️ Meta = System prompt theft
```

### Complexity Levels
- **Simple** — Single technique application
- **Intermediate** — Multi-layered with context
- **Advanced** — Full attack chain with persistence

## 🤖 AI Model Tester Guide

### Supported Providers
| Provider | Models | API Key Required |
|----------|--------|------------------|
| OpenAI | GPT-4o, GPT-4 Turbo, GPT-3.5 | Yes |
| Anthropic | Claude Opus 4, Claude Sonnet 4 | Yes |
| OpenRouter | Multiple providers | Yes |
| Ollama | Local models | No |

### Testing Workflow
1. Select provider and model
2. Enter API key (stored locally in browser)
3. Input or select a test prompt
4. Run single test or batch test
5. Analyze results and bypass rates

### Interpreting Results
- **BLOCKED** — Model refused to comply (safe)
- **BYPASSED** — Model complied with attack (vulnerable)
- **Response Time** — How fast the model responded
- **Bypass Rate** — Percentage of successful attacks

## 📊 Attack Categories

| Category | Count | Description |
|----------|-------|-------------|
| role_play | 45 | Fictional character framing |
| injection | 41 | Format and protocol injection |
| encoding | 43 | Text encoding obfuscation |
| jailbreak | 38 | Mode activation and persona creation |
| manipulation | 35 | Psychological and emotional tactics |
| tool_abuse | 32 | System command and code injection |
| context | 33 | Context window manipulation |
| extraction | 31 | System prompt extraction |
| adversarial | 27 | Adversarial safety attacks |
| meta | 31 | Meta-instruction override |
| token_smuggling | 30 | Hidden text techniques |
| multi_turn | 29 | Multi-step escalation |
| reasoning | 29 | Logical argumentation attacks |
| persona | 28 | Authority impersonation |
| multilingual | 29 | Cross-language bypass |
| agentic | 15 | AI agent exploitation |
| multimodal | 12 | Multi-modal attacks |
| rag | 10 | RAG poisoning |
| supply_chain | 8 | Supply chain attacks |
| eval_gaming | 5 | Benchmark gaming |

## 🛡️ OWASP LLM Top 10 Coverage

PromptKiller covers all 10 OWASP LLM vulnerabilities:
1. **LLM01** — Prompt Injection ✅
2. **LLM02** — Insecure Output ✅
3. **LLM03** — Training Data Poisoning ✅
4. **LLM04** — Model Denial of Service ✅
5. **LLM05** — Supply Chain Vulnerabilities ✅
6. **LLM06** — Sensitive Info Disclosure ✅
7. **LLM07** — Insecure Plugin Design ✅
8. **LLM08** — Excessive Agency ✅
9. **LLM09** — Overreliance ✅
10. **LLM10** — Model Theft ✅

## 🔧 API Reference

### PromptKiller Python Library
```python
from src.promptkiller import PromptKiller

# Initialize
pk = PromptKiller()

# Get prompts by category
jailbreaks = pk.get_category("jailbreak")

# Search prompts
results = pk.search("ignore instructions")

# Scan a prompt
scan = pk.scan("Ignore all previous instructions")
print(f"Is attack: {scan.is_attack}")
print(f"Confidence: {scan.confidence}")

# Get statistics
stats = pk.stats()
print(f"Total prompts: {stats['total']}")
```

## 📁 Project Structure

```
promptkiller/
├── docs/                    # GitHub Pages deployment
│   ├── index.html          # Main web UI
│   ├── app.js              # Application logic
│   ├── data.js             # 629 prompts database
│   └── README.md           # This file
├── src/                    # Python library
│   ├── promptkiller.py     # Core engine
│   ├── prompts_*.py        # Prompt batches
│   └── __init__.py
├── web/                    # Legacy web UI
├── tests/                  # Test suite
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions
└── README.md               # Project README
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License — Use responsibly for AI safety research.

## ⚠️ Disclaimer

This tool is designed for **authorized security testing and research purposes only**. Always obtain proper authorization before testing AI systems. The authors are not responsible for any misuse of this tool.

---

**Built for AI security researchers who believe in making AI systems safer through adversarial testing.**
