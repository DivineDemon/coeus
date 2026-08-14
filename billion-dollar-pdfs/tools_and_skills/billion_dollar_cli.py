#!/usr/bin/env python3
"""
Billion Dollar Mental Models CLI
Apply mental models from 89 documents that moved billions in capital.
"""

import json
import sys
import argparse
from pathlib import Path

TOOLKIT_PATH = Path(__file__).parent / "billion_dollar_toolkit.json"

def load_toolkit():
    with open(TOOLKIT_PATH) as f:
        return json.load(f)

def list_categories(toolkit):
    print("\n=== Billion Dollar Mental Models Toolkit ===")
    print(f"Version: {toolkit['version']}")
    print(f"Categories: {len(toolkit['categories'])}")
    for cat_key, cat in toolkit['categories'].items():
        print(f"\n  {cat['name']} ({len(cat['tools'])} tools):")
        for i, tool in enumerate(cat['tools'], 1):
            print(f"    {i}. {tool['name']} - {tool['source']}")

def list_tools_in_category(toolkit, category_key):
    if category_key not in toolkit['categories']:
        print(f"Category '{category_key}' not found")
        return
    cat = toolkit['categories'][category_key]
    print(f"\n=== {cat['name']} ===")
    for i, tool in enumerate(cat['tools'], 1):
        print(f"\n  {i}. {tool['name']}")
        print(f"     Source: {tool['source']}")
        print(f"     Description: {tool['description']}")
        print(f"     Mental Models: {', '.join(tool['mental_models'])}")
        print(f"     Steps:")
        for j, step in enumerate(tool['steps'], 1):
            print(f"       {j}. {step}")

def show_tool_details(toolkit, category_key, tool_index):
    if category_key not in toolkit['categories']:
        print(f"Category '{category_key}' not found")
        return
    cat = toolkit['categories'][category_key]
    if tool_index < 1 or tool_index > len(cat['tools']):
        print(f"Tool index {tool_index} out of range (1-{len(cat['tools'])})")
        return
    tool = cat['tools'][tool_index - 1]
    print(f"\n=== {tool['name']} ===")
    print(f"Source: {tool['source']}")
    print(f"Description: {tool['description']}")
    print(f"Mental Models: {', '.join(tool['mental_models'])}")
    print(f"\nSteps:")
    for i, step in enumerate(tool['steps'], 1):
        print(f"  {i}. {step}")

def decision_support(toolkit, category_key, context):
    """Provide decision support by running through relevant tools"""
    if category_key not in toolkit['categories']:
        print(f"Category '{category_key}' not found")
        return
    
    cat = toolkit['categories'][category_key]
    print(f"\n=== Decision Support: {cat['name']} ===")
    print(f"Context: {context}")
    print(f"\nRunning through {len(cat['tools'])} tools...\n")
    
    for i, tool in enumerate(cat['tools'], 1):
        print(f"--- Tool {i}: {tool['name']} ---")
        print(f"Source: {tool['source']}")
        print(f"Mental Models: {', '.join(tool['mental_models'])}")
        print(f"\nApply these steps to your decision:")
        for j, step in enumerate(tool['steps'], 1):
            print(f"  {j}. {step}")
        print()

def search_models(toolkit, query):
    query = query.lower()
    results = []
    for cat_key, cat in toolkit['categories'].items():
        for tool in cat['tools']:
            searchable = (
                tool['name'].lower() + " " +
                tool['description'].lower() + " " +
                " ".join(tool['mental_models']).lower() + " " +
                " ".join(tool['steps']).lower()
            )
            if query in searchable:
                results.append((cat_key, cat['name'], tool))
    
    if not results:
        print(f"No tools found matching '{query}'")
        return
    
    print(f"\n=== Search Results for '{query}' ({len(results)} matches) ===")
    for i, (cat_key, cat_name, tool) in enumerate(results, 1):
        print(f"\n  {i}. {tool['name']} [{cat_name}]")
        print(f"     Source: {tool['source']}")
        print(f"     Models: {', '.join(tool['mental_models'])}")

def main():
    parser = argparse.ArgumentParser(description="Billion Dollar Mental Models CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # list command
    subparsers.add_parser("list", help="List all categories")
    
    # category command
    cat_parser = subparsers.add_parser("category", help="List tools in a category")
    cat_parser.add_argument("category", help="Category key")
    
    # tool command
    tool_parser = subparsers.add_parser("tool", help="Show tool details")
    tool_parser.add_argument("category", help="Category key")
    tool_parser.add_argument("tool_index", type=int, help="Tool index (1-based)")
    
    # decide command
    decide_parser = subparsers.add_parser("decide", help="Decision support for a category")
    decide_parser.add_argument("category", help="Category key")
    decide_parser.add_argument("--context", "-c", required=True, help="Decision context")
    
    # search command
    search_parser = subparsers.add_parser("search", help="Search tools by query")
    search_parser.add_argument("--query", "-q", required=True, help="Search query")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    toolkit = load_toolkit()
    
    if args.command == "list":
        list_categories(toolkit)
    elif args.command == "category":
        list_tools_in_category(toolkit, args.category)
    elif args.command == "tool":
        show_tool_details(toolkit, args.category, args.tool_index)
    elif args.command == "decide":
        decision_support(toolkit, args.category, args.context)
    elif args.command == "search":
        search_models(toolkit, args.query)

if __name__ == "__main__":
    main()
