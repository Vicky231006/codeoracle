#!/usr/bin/env python3
"""
Scenario 6: Complete End-to-End Workflow

This scenario demonstrates the complete CodeOracle workflow from ingestion
through all agents to final comprehensive analysis.
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from ingest.ingest import RepositoryIngester
from agents.supervisor import AgentSupervisor
from api.orchestrator import AnalysisOrchestrator


def run_scenario(repo_path: str, output_dir: str = None):
    """
    Run complete end-to-end workflow
    
    Args:
        repo_path: Path to repository to analyze
        output_dir: Optional output directory for results
    """
    print("=" * 80)
    print("SCENARIO 6: Complete End-to-End Workflow")
    print("=" * 80)
    print()
    
    start_time = time.time()
    
    if output_dir is None:
        output_dir = Path(repo_path).parent / "workflow_output"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Repository: {repo_path}")
    print(f"Output Directory: {output_dir}")
    print()
    
    results = {}
    
    # Step 1: Repository Ingestion
    print("-" * 80)
    print("STEP 1: Repository Ingestion")
    print("-" * 80)
    
    try:
        print("Analyzing repository structure...")
        ingester = RepositoryIngester(repo_path)
        manifest = ingester.ingest()
        
        manifest_path = output_dir / "manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"✓ Manifest created: {manifest_path}")
        print(f"  Files analyzed: {len(manifest.get('files', []))}")
        print(f"  Total lines: {sum(f.get('metrics', {}).get('lines_of_code', 0) for f in manifest.get('files', []))}")
        print()
        
        results['ingestion'] = {
            'status': 'success',
            'files_count': len(manifest.get('files', [])),
            'manifest_path': str(manifest_path)
        }
    except Exception as e:
        print(f"✗ Ingestion failed: {str(e)}")
        results['ingestion'] = {'status': 'failed', 'error': str(e)}
        return results
    
    # Step 2: Architecture Analysis
    print("-" * 80)
    print("STEP 2: Architecture Analysis (RepoMapper)")
    print("-" * 80)
    
    try:
        supervisor = AgentSupervisor()
        result = supervisor.run_agent('repo_mapper', manifest)
        
        output_file = output_dir / "architecture_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        if result.get('status') == 'success':
            analysis = result.get('result', {})
            print(f"✓ Architecture analysis complete")
            print(f"  Components: {len(analysis.get('components', []))}")
            print(f"  Layers: {len(analysis.get('layers', []))}")
            print(f"  Patterns: {len(analysis.get('patterns', []))}")
            print()
        
        results['architecture'] = result
    except Exception as e:
        print(f"✗ Architecture analysis failed: {str(e)}")
        results['architecture'] = {'status': 'failed', 'error': str(e)}
    
    # Step 3: Dependency Analysis
    print("-" * 80)
    print("STEP 3: Dependency Analysis (DependencyAnalyst)")
    print("-" * 80)
    
    try:
        result = supervisor.run_agent('dependency_analyst', manifest)
        
        output_file = output_dir / "dependency_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        if result.get('status') == 'success':
            analysis = result.get('result', {})
            print(f"✓ Dependency analysis complete")
            print(f"  Dependencies: {len(analysis.get('dependencies', []))}")
            print(f"  External deps: {len(analysis.get('external_dependencies', []))}")
            print(f"  Circular deps: {len(analysis.get('circular_dependencies', []))}")
            print()
        
        results['dependencies'] = result
    except Exception as e:
        print(f"✗ Dependency analysis failed: {str(e)}")
        results['dependencies'] = {'status': 'failed', 'error': str(e)}
    
    # Step 4: Risk Assessment
    print("-" * 80)
    print("STEP 4: Risk Assessment (RiskDetector)")
    print("-" * 80)
    
    try:
        result = supervisor.run_agent('risk_detector', manifest)
        
        output_file = output_dir / "risk_assessment.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        if result.get('status') == 'success':
            analysis = result.get('result', {})
            risks = analysis.get('risks', [])
            print(f"✓ Risk assessment complete")
            print(f"  Total risks: {len(risks)}")
            print(f"  Risk level: {analysis.get('risk_level', 'Unknown')}")
            print(f"  Risk score: {analysis.get('overall_risk_score', 0)}/100")
            print()
        
        results['risks'] = result
    except Exception as e:
        print(f"✗ Risk assessment failed: {str(e)}")
        results['risks'] = {'status': 'failed', 'error': str(e)}
    
    # Step 5: Knowledge Q&A
    print("-" * 80)
    print("STEP 5: Knowledge Q&A (KnowledgeSynthesizer)")
    print("-" * 80)
    
    try:
        questions = [
            "What is the main purpose of this repository?",
            "What are the key security concerns?",
            "What is the overall code quality?"
        ]
        
        qa_results = []
        for question in questions:
            result = supervisor.run_agent('knowledge_synthesizer', manifest, query=question)
            qa_results.append({'question': question, 'result': result})
        
        output_file = output_dir / "qa_results.json"
        with open(output_file, 'w') as f:
            json.dump(qa_results, f, indent=2)
        
        successful = sum(1 for r in qa_results if r['result'].get('status') == 'success')
        print(f"✓ Q&A complete: {successful}/{len(questions)} questions answered")
        print()
        
        results['qa'] = qa_results
    except Exception as e:
        print(f"✗ Q&A failed: {str(e)}")
        results['qa'] = {'status': 'failed', 'error': str(e)}
    
    # Step 6: Impact Simulation
    print("-" * 80)
    print("STEP 6: Impact Simulation (ImpactSimulator)")
    print("-" * 80)
    
    try:
        scenarios = [
            {'file': 'main.py', 'change_type': 'modify', 'description': 'Update main logic'},
            {'file': 'utils.py', 'change_type': 'modify', 'description': 'Refactor utilities'}
        ]
        
        impact_results = []
        for scenario in scenarios:
            result = supervisor.run_agent('impact_simulator', manifest, change=scenario)
            impact_results.append({'scenario': scenario, 'result': result})
        
        output_file = output_dir / "impact_simulation.json"
        with open(output_file, 'w') as f:
            json.dump(impact_results, f, indent=2)
        
        successful = sum(1 for r in impact_results if r['result'].get('status') == 'success')
        print(f"✓ Impact simulation complete: {successful}/{len(scenarios)} scenarios analyzed")
        print()
        
        results['impact'] = impact_results
    except Exception as e:
        print(f"✗ Impact simulation failed: {str(e)}")
        results['impact'] = {'status': 'failed', 'error': str(e)}
    
    # Step 7: API Integration Test
    print("-" * 80)
    print("STEP 7: API Integration Test")
    print("-" * 80)
    
    try:
        orchestrator = AnalysisOrchestrator()
        result = orchestrator.run_full_analysis(manifest)
        
        output_file = output_dir / "api_integration.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        if result.get('status') == 'success':
            print(f"✓ API integration test passed")
            print(f"  All agents executed successfully through orchestrator")
            print()
        
        results['api_integration'] = result
    except Exception as e:
        print(f"✗ API integration test failed: {str(e)}")
        results['api_integration'] = {'status': 'failed', 'error': str(e)}
    
    # Generate comprehensive report
    end_time = time.time()
    duration = end_time - start_time
    
    print("=" * 80)
    print("WORKFLOW COMPLETE")
    print("=" * 80)
    
    report = {
        'workflow_info': {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': round(duration, 2),
            'repository': repo_path,
            'output_directory': str(output_dir)
        },
        'results': results,
        'summary': {
            'total_steps': 7,
            'successful_steps': sum(
                1 for r in results.values()
                if isinstance(r, dict) and r.get('status') == 'success'
            )
        }
    }
    
    report_file = output_dir / "workflow_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Duration: {duration:.2f} seconds")
    print(f"Successful steps: {report['summary']['successful_steps']}/{report['summary']['total_steps']}")
    print(f"Comprehensive report: {report_file}")
    print()
    
    # Print key findings
    print("KEY FINDINGS:")
    print("-" * 80)
    
    if results.get('architecture', {}).get('status') == 'success':
        arch = results['architecture'].get('result', {})
        print(f"• Architecture: {arch.get('architecture_overview', {}).get('type', 'Unknown')}")
        print(f"  Components: {len(arch.get('components', []))}")
    
    if results.get('dependencies', {}).get('status') == 'success':
        deps = results['dependencies'].get('result', {})
        print(f"• Dependencies: {len(deps.get('dependencies', []))} total")
        circular = len(deps.get('circular_dependencies', []))
        if circular > 0:
            print(f"  ⚠ {circular} circular dependencies detected")
    
    if results.get('risks', {}).get('status') == 'success':
        risks = results['risks'].get('result', {})
        print(f"• Risk Level: {risks.get('risk_level', 'Unknown')}")
        print(f"  Risk Score: {risks.get('overall_risk_score', 0)}/100")
        print(f"  Total Risks: {len(risks.get('risks', []))}")
    
    print()
    
    return report


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Run complete end-to-end workflow')
    parser.add_argument(
        'repo_path',
        help='Path to repository to analyze'
    )
    parser.add_argument(
        '--output-dir',
        help='Output directory for results (optional)'
    )
    
    args = parser.parse_args()
    
    report = run_scenario(args.repo_path, args.output_dir)
    
    # Exit with appropriate code
    if report['summary']['successful_steps'] < report['summary']['total_steps']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

# Made with Bob
