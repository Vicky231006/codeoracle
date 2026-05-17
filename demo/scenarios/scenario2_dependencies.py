#!/usr/bin/env python3
"""
Scenario 2: Dependency Analysis

This scenario demonstrates the DependencyAnalyst agent analyzing code dependencies,
identifying dependency chains, and detecting circular dependencies.
"""

import sys
import json
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.supervisor import AgentSupervisor


def run_scenario(manifest_path: str):
    """
    Run dependency analysis scenario
    
    Args:
        manifest_path: Path to repository manifest JSON file
    """
    print("=" * 80)
    print("SCENARIO 2: Dependency Analysis")
    print("=" * 80)
    print()
    
    # Load manifest
    print(f"Loading manifest from: {manifest_path}")
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    print(f"Repository: {manifest.get('repository', {}).get('name', 'Unknown')}")
    print(f"Files: {len(manifest.get('files', []))}")
    print()
    
    # Run DependencyAnalyst
    print("Running DependencyAnalyst agent...")
    print("-" * 80)
    
    supervisor = AgentSupervisor()
    result = supervisor.run_agent('dependency_analyst', manifest)
    
    # Display results
    if result.get('status') == 'success':
        print("\n✓ Analysis Complete!")
        print()
        
        analysis = result.get('result', {})
        
        # Dependencies
        dependencies = analysis.get('dependencies', [])
        print(f"DEPENDENCIES ({len(dependencies)}):")
        print("-" * 80)
        for dep in dependencies[:10]:  # Show first 10
            print(f"• {dep.get('source', 'Unknown')} → {dep.get('target', 'Unknown')}")
            print(f"  Type: {dep.get('type', 'Unknown')}")
            if dep.get('line_number'):
                print(f"  Line: {dep.get('line_number')}")
            print()
        
        if len(dependencies) > 10:
            print(f"... and {len(dependencies) - 10} more dependencies")
            print()
        
        # Dependency graph
        graph = analysis.get('dependency_graph', {})
        nodes = graph.get('nodes', [])
        edges = graph.get('edges', [])
        
        print(f"DEPENDENCY GRAPH:")
        print("-" * 80)
        print(f"Nodes: {len(nodes)}")
        print(f"Edges: {len(edges)}")
        print()
        
        # External dependencies
        external_deps = analysis.get('external_dependencies', [])
        if external_deps:
            print(f"EXTERNAL DEPENDENCIES ({len(external_deps)}):")
            print("-" * 80)
            for ext_dep in external_deps:
                print(f"• {ext_dep.get('name', 'Unknown')}")
                if ext_dep.get('version'):
                    print(f"  Version: {ext_dep.get('version')}")
                used_by = ext_dep.get('used_by', [])
                if used_by:
                    print(f"  Used by: {', '.join(used_by[:3])}")
                    if len(used_by) > 3:
                        print(f"           ... and {len(used_by) - 3} more files")
                print()
        
        # Circular dependencies
        circular = analysis.get('circular_dependencies', [])
        if circular:
            print(f"⚠ CIRCULAR DEPENDENCIES DETECTED ({len(circular)}):")
            print("-" * 80)
            for cycle in circular:
                cycle_path = cycle.get('cycle', [])
                print(f"• {' → '.join(cycle_path)}")
                print(f"  Severity: {cycle.get('severity', 'Unknown')}")
                print()
        else:
            print("✓ No circular dependencies detected")
            print()
        
        # Dependency metrics
        metrics = analysis.get('metrics', {})
        if metrics:
            print(f"DEPENDENCY METRICS:")
            print("-" * 80)
            print(f"Average dependencies per file: {metrics.get('avg_dependencies_per_file', 0):.2f}")
            print(f"Max dependencies in a file: {metrics.get('max_dependencies', 0)}")
            print(f"Files with most dependencies: {', '.join(metrics.get('most_dependent_files', [])[:3])}")
            print()
        
        # Insights
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
    
    parser = argparse.ArgumentParser(description='Run dependency analysis scenario')
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
