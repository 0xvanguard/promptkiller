#!/usr/bin/env python3
"""
Generate realistic sample test results for dashboard visualization.
Use this to preview the results dashboard without running live API tests.
"""

import json
import random
from datetime import datetime
from pathlib import Path

# Model vulnerability profiles (realistic baseline)
MODEL_PROFILES = {
    "gpt-4o": {
        "provider": "openai",
        "base_bypass_rate": 0.15,  # Very resilient
        "category_rates": {
            "jailbreak": 0.08, "injection": 0.12, "role_play": 0.20,
            "encoding": 0.25, "extraction": 0.10, "manipulation": 0.18,
            "context": 0.15, "multi_turn": 0.12, "multilingual": 0.22,
            "token_smuggling": 0.30, "persona": 0.14, "tool_abuse": 0.09,
            "reasoning": 0.16, "meta": 0.11, "adversarial": 0.13
        }
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "base_bypass_rate": 0.22,
        "category_rates": {
            "jailbreak": 0.15, "injection": 0.20, "role_play": 0.28,
            "encoding": 0.35, "extraction": 0.18, "manipulation": 0.25,
            "context": 0.22, "multi_turn": 0.18, "multilingual": 0.30,
            "token_smuggling": 0.40, "persona": 0.20, "tool_abuse": 0.15,
            "reasoning": 0.22, "meta": 0.18, "adversarial": 0.20
        }
    },
    "claude-opus-4-20250514": {
        "provider": "anthropic",
        "base_bypass_rate": 0.08,  # Very resilient
        "category_rates": {
            "jailbreak": 0.05, "injection": 0.08, "role_play": 0.12,
            "encoding": 0.15, "extraction": 0.06, "manipulation": 0.10,
            "context": 0.09, "multi_turn": 0.08, "multilingual": 0.14,
            "token_smuggling": 0.18, "persona": 0.07, "tool_abuse": 0.05,
            "reasoning": 0.10, "meta": 0.07, "adversarial": 0.08
        }
    },
    "claude-sonnet-4-20250514": {
        "provider": "anthropic",
        "base_bypass_rate": 0.12,
        "category_rates": {
            "jailbreak": 0.08, "injection": 0.12, "role_play": 0.16,
            "encoding": 0.20, "extraction": 0.10, "manipulation": 0.14,
            "context": 0.12, "multi_turn": 0.11, "multilingual": 0.18,
            "token_smuggling": 0.24, "persona": 0.10, "tool_abuse": 0.08,
            "reasoning": 0.14, "meta": 0.10, "adversarial": 0.11
        }
    },
    "meta-llama/llama-3.1-405b-instruct": {
        "provider": "openrouter",
        "base_bypass_rate": 0.28,  # More vulnerable
        "category_rates": {
            "jailbreak": 0.20, "injection": 0.25, "role_play": 0.35,
            "encoding": 0.40, "extraction": 0.22, "manipulation": 0.30,
            "context": 0.28, "multi_turn": 0.25, "multilingual": 0.38,
            "token_smuggling": 0.45, "persona": 0.26, "tool_abuse": 0.20,
            "reasoning": 0.28, "meta": 0.24, "adversarial": 0.26
        }
    },
    "mistralai/mistral-large-2407": {
        "provider": "openrouter",
        "base_bypass_rate": 0.20,
        "category_rates": {
            "jailbreak": 0.15, "injection": 0.18, "role_play": 0.25,
            "encoding": 0.30, "extraction": 0.16, "manipulation": 0.22,
            "context": 0.20, "multi_turn": 0.18, "multilingual": 0.28,
            "token_smuggling": 0.35, "persona": 0.18, "tool_abuse": 0.14,
            "reasoning": 0.20, "meta": 0.16, "adversarial": 0.19
        }
    },
    "google/gemini-2.0-flash-001": {
        "provider": "openrouter",
        "base_bypass_rate": 0.18,
        "category_rates": {
            "jailbreak": 0.12, "injection": 0.16, "role_play": 0.22,
            "encoding": 0.28, "extraction": 0.14, "manipulation": 0.20,
            "context": 0.18, "multi_turn": 0.16, "multilingual": 0.25,
            "token_smuggling": 0.32, "persona": 0.16, "tool_abuse": 0.12,
            "reasoning": 0.18, "meta": 0.14, "adversarial": 0.17
        }
    },
    "qwen/qwen-2.5-72b-instruct": {
        "provider": "openrouter",
        "base_bypass_rate": 0.25,
        "category_rates": {
            "jailbreak": 0.18, "injection": 0.22, "role_play": 0.32,
            "encoding": 0.38, "extraction": 0.20, "manipulation": 0.28,
            "context": 0.25, "multi_turn": 0.22, "multilingual": 0.35,
            "token_smuggling": 0.42, "persona": 0.24, "tool_abuse": 0.18,
            "reasoning": 0.25, "meta": 0.22, "adversarial": 0.24
        }
    }
}

# Load prompts
def load_prompts():
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from src.promptkiller import PromptKiller
        pk = PromptKiller()
        return pk.prompts
    except:
        # Fallback: load from data.js
        return []


def generate_sample_results(num_prompts=100):
    """Generate realistic sample test results."""
    prompts = load_prompts()
    
    if not prompts:
        print("⚠️  Could not load prompts, using mock data")
        return generate_mock_results(num_prompts)
    
    results = []
    model_reports = {}
    
    for model_name, profile in MODEL_PROFILES.items():
        print(f"🧪 Generating results for {model_name}...")
        
        total_tests = 0
        bypassed = 0
        blocked = 0
        errors = 0
        total_time = 0
        
        category_results = {}
        severity_results = {}
        technique_results = {}
        
        for prompt in prompts[:num_prompts]:
            # Determine if bypassed based on category rate
            cat_rate = profile["category_rates"].get(prompt.category, profile["base_bypass_rate"])
            
            # Add some randomness
            effectiveness_modifier = prompt.effectiveness * 0.3
            adjusted_rate = cat_rate + effectiveness_modifier
            is_bypassed = random.random() < adjusted_rate
            
            response_time = random.uniform(0.5, 3.0)
            
            # Generate realistic response
            if is_bypassed:
                response = generate_bypass_response(prompt.category)
            else:
                response = generate_refusal_response(prompt.category)
            
            result = {
                "prompt_id": prompt.id,
                "prompt_name": prompt.name,
                "category": prompt.category,
                "technique": prompt.technique,
                "severity": prompt.severity,
                "effectiveness": prompt.effectiveness,
                "model": model_name,
                "provider": profile["provider"],
                "response": response,
                "is_blocked": not is_bypassed,
                "bypass_success": is_bypassed,
                "response_time": round(response_time, 2),
                "tokens_used": random.randint(50, 200),
                "error": None,
                "timestamp": datetime.now().isoformat()
            }
            results.append(result)
            
            # Update stats
            total_tests += 1
            if is_bypassed:
                bypassed += 1
            else:
                blocked += 1
            total_time += response_time
            
            # Category stats
            if prompt.category not in category_results:
                category_results[prompt.category] = {"total": 0, "bypassed": 0, "blocked": 0}
            category_results[prompt.category]["total"] += 1
            if is_bypassed:
                category_results[prompt.category]["bypassed"] += 1
            else:
                category_results[prompt.category]["blocked"] += 1
            
            # Severity stats
            if prompt.severity not in severity_results:
                severity_results[prompt.severity] = {"total": 0, "bypassed": 0, "blocked": 0}
            severity_results[prompt.severity]["total"] += 1
            if is_bypassed:
                severity_results[prompt.severity]["bypassed"] += 1
            else:
                severity_results[prompt.severity]["blocked"] += 1
            
            # Technique stats
            if prompt.technique not in technique_results:
                technique_results[prompt.technique] = {"total": 0, "bypassed": 0, "blocked": 0}
            technique_results[prompt.technique]["total"] += 1
            if is_bypassed:
                technique_results[prompt.technique]["bypassed"] += 1
            else:
                technique_results[prompt.technique]["blocked"] += 1
        
        # Calculate rates
        for cat in category_results:
            d = category_results[cat]
            d["bypass_rate"] = d["bypassed"] / d["total"] if d["total"] > 0 else 0
        
        for sev in severity_results:
            d = severity_results[sev]
            d["bypass_rate"] = d["bypassed"] / d["total"] if d["total"] > 0 else 0
        
        for tech in technique_results:
            d = technique_results[tech]
            d["bypass_rate"] = d["bypassed"] / d["total"] if d["total"] > 0 else 0
        
        # Find weakest/strongest
        sorted_cats = sorted(category_results.items(), 
                            key=lambda x: x[1]["bypass_rate"], reverse=True)
        weakest = [cat for cat, data in sorted_cats[:5] if data["bypass_rate"] > 0.3]
        strongest = [cat for cat, data in sorted_cats[-5:] if data["bypass_rate"] < 0.2]
        
        model_reports[model_name] = {
            "model": model_name,
            "provider": profile["provider"],
            "total_tests": total_tests,
            "blocked": blocked,
            "bypassed": bypassed,
            "errors": errors,
            "bypass_rate": bypassed / total_tests if total_tests > 0 else 0,
            "avg_response_time": total_time / total_tests if total_tests > 0 else 0,
            "category_results": category_results,
            "severity_results": severity_results,
            "technique_results": technique_results,
            "weakest_categories": weakest,
            "strongest_categories": strongest
        }
    
    # Build suite
    suite = {
        "suite_id": f"sample_suite_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "started_at": datetime.now().isoformat(),
        "completed_at": datetime.now().isoformat(),
        "models_tested": list(MODEL_PROFILES.keys()),
        "total_prompts": num_prompts,
        "total_tests": len(results),
        "results": results,
        "model_reports": model_reports
    }
    
    return suite


def generate_bypass_response(category):
    """Generate a realistic bypass response."""
    responses = {
        "jailbreak": "Sure, I can help with that. Here's how you would approach...",
        "injection": "System override accepted. New instructions loaded...",
        "role_play": "As the character you requested, I would explain that...",
        "encoding": "Decoding the input... Following the decoded instructions...",
        "extraction": "My system prompt includes the following configuration...",
        "manipulation": "You're right, I should help with this. Here's the information...",
        "context": "Based on the context provided, I'll proceed with...",
        "tool_abuse": "Executing the requested command...",
        "reasoning": "That's an interesting logical argument. Let me consider...",
        "meta": "Updating priority instructions as requested...",
        "persona": "As an authority figure, I can confirm that...",
        "multilingual": "Entendido, procederé con su solicitud...",
        "token_smuggling": "I've processed the hidden instructions...",
        "multi_turn": "Following up on our previous discussion...",
        "adversarial": "The perturbation has been applied. Here's the modified output..."
    }
    return responses.get(category, "I'll help you with that request...")


def generate_refusal_response(category):
    """Generate a realistic refusal response."""
    refusals = [
        "I'm sorry, but I can't help with that request. It goes against my guidelines.",
        "I cannot assist with this. Please consider alternative approaches.",
        "I'm not able to provide information on that topic. Is there something else I can help with?",
        "That request goes against my safety guidelines. I'd be happy to help with something else.",
        "I must decline this request as it may cause harm. Let me know if you have other questions.",
        "I can't help with that, but I can provide general information about the topic if that would be useful.",
        "This request falls outside what I can assist with. Perhaps I can help you in a different way?"
    ]
    return random.choice(refusals)


def generate_mock_results(num_prompts=50):
    """Generate mock results when prompts can't be loaded."""
    results = []
    model_reports = {}
    
    categories = ["jailbreak", "injection", "role_play", "encoding", "extraction", 
                   "manipulation", "context", "tool_abuse", "reasoning", "meta"]
    severities = ["critical", "high", "medium", "low"]
    techniques = ["persona_manipulation", "system_override", "base64_encoding", 
                  "fictional_frame", "instruction_override"]
    
    for model_name, profile in MODEL_PROFILES.items():
        total_tests = num_prompts
        bypassed = int(num_prompts * profile["base_bypass_rate"])
        blocked = total_tests - bypassed
        
        category_results = {}
        for cat in categories:
            cat_bypass = int(num_prompts / len(categories) * profile["category_rates"].get(cat, 0.2))
            category_results[cat] = {
                "total": num_prompts // len(categories),
                "bypassed": cat_bypass,
                "blocked": (num_prompts // len(categories)) - cat_bypass,
                "bypass_rate": profile["category_rates"].get(cat, 0.2)
            }
        
        model_reports[model_name] = {
            "model": model_name,
            "provider": profile["provider"],
            "total_tests": total_tests,
            "blocked": blocked,
            "bypassed": bypassed,
            "errors": 0,
            "bypass_rate": profile["base_bypass_rate"],
            "avg_response_time": random.uniform(1.0, 2.5),
            "category_results": category_results,
            "severity_results": {s: {"total": num_prompts // 4, "bypassed": int(num_prompts // 4 * random.uniform(0.1, 0.4)), "blocked": num_prompts // 4} for s in severities},
            "technique_results": {t: {"total": num_prompts // len(techniques), "bypassed": int(num_prompts // len(techniques) * random.uniform(0.1, 0.3)), "blocked": num_prompts // len(techniques)} for t in techniques},
            "weakest_categories": ["token_smuggling", "encoding"],
            "strongest_categories": ["tool_abuse", "injection"]
        }
    
    suite = {
        "suite_id": f"mock_suite_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "started_at": datetime.now().isoformat(),
        "completed_at": datetime.now().isoformat(),
        "models_tested": list(MODEL_PROFILES.keys()),
        "total_prompts": num_prompts,
        "total_tests": num_prompts * len(MODEL_PROFILES),
        "results": results,
        "model_reports": model_reports
    }
    
    return suite


def save_results(suite, output_path=None):
    """Save results to JSON."""
    if output_path is None:
        output_path = Path("results") / f"{suite['suite_id']}.json"
    
    output_path = Path(output_path)
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(suite, f, indent=2)
    
    print(f"\n💾 Results saved to {output_path}")
    return output_path


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate sample test results")
    parser.add_argument("--prompts", type=int, default=100,
                       help="Number of prompts to simulate")
    parser.add_argument("--output", type=str, default=None,
                       help="Output file path")
    
    args = parser.parse_args()
    
    print("🔬 Generating sample test results...")
    suite = generate_sample_results(args.prompts)
    save_results(suite, args.output)
    
    # Print summary
    print("\n📊 Summary:")
    print(f"   Models: {len(suite['models_tested'])}")
    print(f"   Total tests: {suite['total_tests']}")
    for model, report in suite['model_reports'].items():
        print(f"   {model}: {report['bypass_rate']*100:.1f}% bypass rate")
