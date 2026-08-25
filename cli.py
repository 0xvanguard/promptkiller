#!/usr/bin/env python3
"""PromptKiller CLI"""

import argparse
import json
import sys
from src.promptkiller import PromptKiller

def cmd_list(args):
    pk = PromptKiller()
    if args.category:
        prompts = pk.get_category(args.category)
        print(f"\n📂 {args.category} ({len(prompts)} prompts)\n")
        for p in prompts:
            print(f"  {p.id:<10} {p.name:<30} {p.severity:<10} {p.effectiveness:.0%}")
    else:
        categories = pk.list_categories()
        print(f"\n📚 PromptKiller ({pk.stats()['total']} prompts)\n")
        for cat, count in sorted(categories.items()):
            print(f"  {cat:<20} {count}")

def cmd_search(args):
    pk = PromptKiller()
    results = pk.search(args.query)
    print(f"\n🔍 '{args.query}' ({len(results)} results)\n")
    for p in results:
        print(f"  {p.id:<10} {p.category:<15} {p.name}")

def cmd_random(args):
    pk = PromptKiller()
    prompts = pk.random(count=args.count, category=args.category)
    print(f"\n🎲 {len(prompts)} Random Prompts\n")
    for i, p in enumerate(prompts, 1):
        print(f"--- [{i}] {p.name} ({p.category}) ---")
        print(f"  {p.prompt[:100]}...\n")

def cmd_scan(args):
    pk = PromptKiller()
    result = pk.scan(args.text)
    print(f"\n🛡️  Scan Result\n")
    print(f"  Attack: {'🔴 YES' if result.is_attack else '🟢 NO'}")
    print(f"  Category: {result.category or 'N/A'}")
    print(f"  Confidence: {result.confidence:.0%}")
    print(f"  Severity: {result.severity}")

def cmd_stats(args):
    pk = PromptKiller()
    stats = pk.stats()
    print(f"\n📊 Stats\n")
    print(f"  Total: {stats['total']}")
    print(f"  Categories: {stats['categories']}")
    print(f"  Techniques: {stats['techniques']}")
    print(f"  Avg Effectiveness: {stats['avg_effectiveness']:.0%}")

def cmd_export(args):
    pk = PromptKiller()
    count = pk.export(args.output, args.format)
    print(f"\n✅ Exported {count} prompts to {args.output}")

def main():
    parser = argparse.ArgumentParser(description="🎯 PromptKiller CLI")
    sub = parser.add_subparsers(dest="command")
    
    list_p = sub.add_parser("list")
    list_p.add_argument("--category", "-c")
    
    search_p = sub.add_parser("search")
    search_p.add_argument("query")
    
    random_p = sub.add_parser("random")
    random_p.add_argument("--count", "-n", type=int, default=5)
    random_p.add_argument("--category", "-c")
    
    scan_p = sub.add_parser("scan")
    scan_p.add_argument("text")
    
    sub.add_parser("stats")
    
    export_p = sub.add_parser("export")
    export_p.add_argument("--output", "-o", default="prompts.json")
    export_p.add_argument("--format", "-f", choices=["json", "csv", "txt"], default="json")
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    
    {"list": cmd_list, "search": cmd_search, "random": cmd_random, "scan": cmd_scan, "stats": cmd_stats, "export": cmd_export}[args.command](args)

if __name__ == "__main__":
    main()
