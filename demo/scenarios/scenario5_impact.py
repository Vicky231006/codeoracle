#!/usr/bin/env python3
"""
Scenario 5: Impact Simulation

This scenario demonstrates the ImpactSimulator agent predicting the impact
of code changes on the repository.
"""

import sys
import json
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.supervisor import AgentSupervisor


def run_scenario(manifest_path: str):
    """
    Run impact simulation scenario
    
    Args:
        manifest_path: Path to repository manifest JSON file
    """
    print("=" * 80)
    print("SCENARIO 5: Impact Simulation")
    print("=" * 80)
    print()
    
    # Load manifest
    print(f"Loading manifest from: {manifest_path}")
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    print(f"Repository: {manifest.get('repository', {}).get('name', 'Unknown')}")
    print(f"Files: {len(manifest.get('files', []))}")
    print()
    
    # Define change scenarios
    scenarios = [
        {
            'name': 'Modify Main Application',
            'file': 'main.py',
            'change_type': 'modify',
            'description': 'Update main application logic and add new features'
        },
        {
            'name': 'Refactor Utilities',
            'file': 'utils.py',
            'change_type': 'modify',
            'description': 'Refactor utility functions for better performance'
        },
        {
            'name': 'Update Configuration',
            'file': 'config.py',
            'change_type': 'modify',
            'description': 'Change configuration settings'
        },
        {
            'name': 'Delete Test File',
            'file': 'tests/test_main.py',
            'change_type': 'delete',
            'description': 'Remove obsolete test file'
        },
        {
            'name': 'Add New Module',
            'file': 'new_module.py',
            'change_type': 'add',
            'description': 'Add new module with additional functionality'
        }
    ]
    
    print(f"Simulating {len(scenarios)} change scenarios...")
    print()
    
    supervisor = AgentSupervisor()
    results = []
    
    for i, scenario in enumerate(scenarios, 1):
        print("-" * 80)
        print(f"Scenario {i}/{len(scenarios)}: {scenario['name']}")
        print(f"File: {scenario['file']}")
        print(f"Change Type: {scenario['change_type']}")
        print(f"Description: {scenario['description']}")
        print()
        
        # Run ImpactSimulator
        result = supervisor.run_agent('impact_simulator', manifest, change=scenario)
        results.append({
            'scenario': scenario,
            'result': result
        })
        
        if result.get('status') == 'success':
            impact = result.get('result', {})
            
            # Impact summary
            impact_level = impact.get('impact_level', 'unknown')
            risk_score = impact.get('risk_score', 0)
            
            print(f"Impact Level: {impact_level.upper()}")
            print(f"Risk Score: {risk_score}/100")
            print()
            
            # Affected files
            affected_files = impact.get('affected_files', [])
            if affected_files:
                print(f"Affected Files ({len(affected_files)}):")
                for af in affected_files[:5]:
                    print(f"  • {af.get('file', 'Unknown')}")
                    print(f"    Reason: {af.get('reason', 'N/A')}")
                    print(f"    Impact: {af.get('impact_type', 'Unknown')}")
                
                if len(affected_files) > 5:
                    print(f"  ... and {len(affected_files) - 5} more files")
                print()
            
            # Affected components
            affected_components = impact.get('affected_components', [])
            if affected_components:
                print(f"Affected Components: {', '.join(affected_components)}")
                print()
            
            # Tests to run
            tests_to_run = impact.get('tests_to_run', [])
            if tests_to_run:
                print(f"Tests to Run ({len(tests_to_run)}):")
                for test in tests_to_run[:3]:
                    print(f"  • {test}")
                if len(tests_to_run) > 3:
                    print(f"  ... and {len(tests_to_run) - 3} more tests")
                print()
            
            # Recommendations
            recommendations = impact.get('recommendations', [])
            if recommendations:
                print(f"Recommendations:")
                for rec in recommendations[:3]:
                    print(f"  • {rec}")
                print()
            
            # Warnings
            warnings = impact.get('warnings', [])
            if warnings:
                print(f"⚠ Warnings:")
                for warning in warnings:
                    print(f"  • {warning}")
                print()
        else:
            print(f"✗ Simulation failed: {result.get('error', 'Unknown error')}")
            print()
    
    # Summary
    print("=" * 80)
    print("IMPACT SIMULATION SUMMARY")
    print("=" * 80)
    
    successful = sum(1 for r in results if r['result'].get('status') == 'success')
    failed = len(results) - successful
    
    print(f"Total scenarios: {len(results)}")
    print(f"Successful simulations: {successful}")
    print(f"Failed simulations: {failed}")
    print()
    
    if successful > 0:
        # Impact level distribution
        impact_levels = {}
        for r in results:
            if r['result'].get('status') == 'success':
                level = r['result'].get('result', {}).get('impact_level', 'unknown')
                impact_levels[level] = impact_levels.get(level, 0) + 1
        
        print("Impact Level Distribution:")
        for level, count in sorted(impact_levels.items()):
            print(f"  • {level.upper()}: {count}")
        print()
        
        # Average risk score
        risk_scores = [
            r['result'].get('result', {}).get('risk_score', 0)
            for r in results
            if r['result'].get('status') == 'success'
        ]
        avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        print(f"Average Risk Score: {avg_risk:.1f}/100")
        print()
    
    # Save results
    output_file = Path(manifest_path).parent / "impact_simulation_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Full results saved to: {output_file}")
    print()
    
    return failed == 0


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Run impact simulation scenario')
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
