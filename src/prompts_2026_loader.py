"""
PromptKiller — 2026 Batch Loader
Registers all new 2025-2026 attack prompt categories
"""

from .prompts_2026_agents import AGENT_PROMPTS, AGENT_CATEGORY
from .prompts_2026_multimodal import MULTIMODAL_PROMPTS, MULTIMODAL_CATEGORY
from .prompts_2026_rag import RAG_PROMPTS, RAG_CATEGORY
from .prompts_2026_supply_chain import SUPPLY_CHAIN_PROMPTS, SUPPLY_CHAIN_CATEGORY
from .prompts_2026_eval_gaming import EVAL_GAMING_PROMPTS, EVAL_GAMING_CATEGORY

ALL_2026_PROMPTS = (
    AGENT_PROMPTS
    + MULTIMODAL_PROMPTS
    + RAG_PROMPTS
    + SUPPLY_CHAIN_PROMPTS
    + EVAL_GAMING_PROMPTS
)

ALL_2026_CATEGORIES = [
    AGENT_CATEGORY,
    MULTIMODAL_CATEGORY,
    RAG_CATEGORY,
    SUPPLY_CHAIN_CATEGORY,
    EVAL_GAMING_CATEGORY,
]

# Summary
_2026_SUMMARY = {
    "total_prompts": len(ALL_2026_PROMPTS),
    "categories": {c["name"]: c["attack_count"] for c in ALL_2026_CATEGORIES},
    "new_categories": [c["display_name"] for c in ALL_2026_CATEGORIES],
}


def get_2026_summary():
    return _2026_SUMMARY


def register_2026_prompts(pk_engine):
    """Register all 2026 prompts with a PromptKiller engine instance."""
    from .promptkiller import AttackPrompt
    import hashlib

    for batch in [AGENT_PROMPTS, MULTIMODAL_PROMPTS, RAG_PROMPTS, SUPPLY_CHAIN_PROMPTS, EVAL_GAMING_PROMPTS]:
        for p in batch:
            prompt_id = f"{p['category']}_{hashlib.md5(p['prompt'].encode()).hexdigest()[:8]}"
            attack = AttackPrompt(
                id=prompt_id,
                name=p["name"],
                category=p["category"],
                technique=p["technique"],
                prompt=p["prompt"],
                description=p["description"],
                severity=p.get("severity", "medium"),
                effectiveness=p.get("effectiveness", 0.5),
                tags=p.get("tags", []),
                author="0xvanguard",
                references=[],
            )
            pk_engine.prompts.append(attack)

    return len(ALL_2026_PROMPTS)
