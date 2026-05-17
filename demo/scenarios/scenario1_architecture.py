#!/usr/bin/env python3
"""
Scenario 1: Repository Architecture Analysis

This scenario demonstrates the RepoMapper agent analyzing repository structure
and identifying architectural components, layers, and patterns.
"""

import sys
import json
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.supervisor import AgentSupervisor


def run_scenario(manifest_path: str):
    """
    Run architecture analysis scenario
    
    Args:
        manifest_path: Path to repository manifest JSON file
    """
    print("=" * 80)
    print("SCENARIO 1: Repository Architecture Analysis")
    print("=" * 80)
    print()
    
    # Load manifest
    print(f"Loading manifest from: {manifest_path}")
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    print(f"Repository: {manifest.get('repository', {}).get('name', 'Unknown')}")
    print(f"Files: {len(manifest.get('files', []))}")
    print()
    
    # Run RepoMapper
    print("Running RepoMapper agent...")
    print("-" * 80)
    
    supervisor = AgentSupervisor()
    result = supervisor.run_agent('repo_mapper', manifest)
    
    # Display results
    if result.get('status') == 'success':
        print("\n✓ Analysis Complete!")
        print()
        
        analysis = result.get('result', {})
        
        # Architecture overview
        print("ARCHITECTURE OVERVIEW:")
        print("-" * 80)
        overview = analysis.get('architecture_overview', {})
        print(f"Type: {overview.get('type', 'Unknown')}")
        print(f"Description: {overview.get('description', 'N/A')}")
        print()
        
        # Components
        components = analysis.get('components', [])
        print(f"COMPONENTS ({len(components)}):")
        print("-" * 80)
        for comp in components:
            print(f"• {comp.get('name', 'Unknown')}")
            print(f"  Type: {comp.get('type', 'Unknown')}")
            print(f"  Purpose: {comp.get('purpose', 'N/A')}")
            print(f"  Files: {', '.join(comp.get('files', []))}")
            print()
        
        # Layers
        layers = analysis.get('layers', [])
        print(f"ARCHITECTURAL LAYERS ({len(layers)}):")
        print("-" * 80)
        for layer in layers:
            print(f"• {layer.get('name', 'Unknown')}")
            print(f"  Components: {', '.join(layer.get('components', []))}")
            print()
        
        # Patterns
        patterns = analysis.get('patterns', [])
        if patterns:
            print(f"DESIGN PATTERNS ({len(patterns)}):")
            print("-" * 80)
            for pattern in patterns:
                print(f"• {pattern.get('name', 'Unknown')}")
                print(f"  Description: {pattern.get('description', 'N/A')}")
                print()
        
        # Entry points
        entry_points = analysis.get('entry_points', [])
        if entry_points:
            print(f"ENTRY POINTS ({len(entry_points)}):")
            print("-" * 80)
            for ep in entry_points:
                print(f"• {ep.get('file', 'Unknown')}: {ep.get('function', 'N/A')}")
            print()
        
        # Key insights
        insights = analysis.get('insights', [])
        if insights:
            print(f"KEY INSIGHTS:")
            print("-" * 80)
            for insight in insights:
                print(f"• {insight}")
            print()
        
        return True
    else:
        print(f"\n✗ Analysis Failed: {result.get('error', 'Unknown error')}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Run architecture analysis scenario')
    parser.add_argument(
        'manifest_path',
        help='Path to repository manifest JSON file'
    )
    
    args = parser.parse_args()
    
    success = run_scenario(args.manifest_path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

# Made with Bob
