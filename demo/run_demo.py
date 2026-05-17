#!/usr/bin/env python3
"""
CodeOracle End-to-End Demo Script

This script demonstrates the complete CodeOracle system workflow:
1. Repository ingestion
2. All 5 agents in action
3. API integration
4. Report generation

Usage:
    python run_demo.py [--repo-path PATH] [--output-dir DIR] [--skip-ingestion]
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ingest.ingest import RepositoryIngester
from agents.supervisor import AgentSupervisor
from api.orchestrator import AnalysisOrchestrator


class DemoRunner:
    """Runs the complete CodeOracle demo"""
    
    def __init__(self, repo_path: str, output_dir: str, skip_ingestion: bool = False):
        self.repo_path = Path(repo_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.skip_ingestion = skip_ingestion
        
        self.manifest_path = self.output_dir / "manifest.json"
        self.results = {}
        self.start_time = None
        
    def print_header(self, text: str):
        """Print a formatted header"""
        print("\n" + "=" * 80)
        print(f"  {text}")
        print("=" * 80 + "\n")
        
    def print_step(self, step: int, text: str):
        """Print a step indicator"""
        print(f"\n[Step {step}] {text}")
        print("-" * 80)
        
    def print_success(self, text: str):
        """Print success message"""
        print(f"✓ {text}")
        
    def print_error(self, text: str):
        """Print error message"""
        print(f"✗ ERROR: {text}")
        
    def run_ingestion(self) -> bool:
        """Step 1: Run repository ingestion"""
        self.print_step(1, "Repository Ingestion")
        
        if self.skip_ingestion and self.manifest_path.exists():
            self.print_success(f"Skipping ingestion, using existing manifest: {self.manifest_path}")
            return True
            
        try:
            print(f"Ingesting repository: {self.repo_path}")
            ingester = RepositoryIngester(str(self.repo_path))
            manifest = ingester.ingest()
            
            # Save manifest
            with open(self.manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
                
            self.print_success(f"Manifest created: {self.manifest_path}")
            self.print_success(f"Files analyzed: {len(manifest.get('files', []))}")
            
            self.results['ingestion'] = {
                'status': 'success',
                'files_count': len(manifest.get('files', [])),
                'manifest_path': str(self.manifest_path)
            }
            return True
            
        except Exception as e:
            self.print_error(f"Ingestion failed: {str(e)}")
            self.results['ingestion'] = {'status': 'failed', 'error': str(e)}
            return False
            
    def run_repo_mapper(self) -> bool:
        """Step 2: Run RepoMapper agent"""
        self.print_step(2, "Architecture Analysis (RepoMapper)")
        
        try:
            with open(self.manifest_path, 'r') as f:
                manifest = json.load(f)
                
            supervisor = AgentSupervisor()
            result = supervisor.run_agent('repo_mapper', manifest)
            
            # Save result
            output_file = self.output_dir / "repo_mapper_result.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
                
            self.print_success(f"Architecture analysis complete: {output_file}")
            
            if result.get('status') == 'success':
                analysis = result.get('result', {})
                self.print_success(f"Components identified: {len(analysis.get('components', []))}")
                self.print_success(f"Layers identified: {len(analysis.get('layers', []))}")
                
            self.results['repo_mapper'] = result
            return result.get('status') == 'success'
            
        except Exception as e:
            self.print_error(f"RepoMapper failed: {str(e)}")
            self.results['repo_mapper'] = {'status': 'failed', 'error': str(e)}
            return False
            
    def run_dependency_analyst(self) -> bool:
        """Step 3: Run DependencyAnalyst agent"""
        self.print_step(3, "Dependency Analysis (DependencyAnalyst)")
        
        try:
            with open(self.manifest_path, 'r') as f:
                manifest = json.load(f)
                
            supervisor = AgentSupervisor()
            result = supervisor.run_agent('dependency_analyst', manifest)
            
            # Save result
            output_file = self.output_dir / "dependency_analyst_result.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
                
            self.print_success(f"Dependency analysis complete: {output_file}")
            
            if result.get('status') == 'success':
                analysis = result.get('result', {})
                self.print_success(f"Dependencies found: {len(analysis.get('dependencies', []))}")
                self.print_success(f"Dependency graph nodes: {len(analysis.get('dependency_graph', {}).get('nodes', []))}")
                
            self.results['dependency_analyst'] = result
            return result.get('status') == 'success'
            
        except Exception as e:
            self.print_error(f"DependencyAnalyst failed: {str(e)}")
            self.results['dependency_analyst'] = {'status': 'failed', 'error': str(e)}
            return False
            
    def run_risk_detector(self) -> bool:
        """Step 4: Run RiskDetector agent"""
        self.print_step(4, "Risk Assessment (RiskDetector)")
        
        try:
            with open(self.manifest_path, 'r') as f:
                manifest = json.load(f)
                
            supervisor = AgentSupervisor()
            result = supervisor.run_agent('risk_detector', manifest)
            
            # Save result
            output_file = self.output_dir / "risk_detector_result.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
                
            self.print_success(f"Risk assessment complete: {output_file}")
            
            if result.get('status') == 'success':
                analysis = result.get('result', {})
                risks = analysis.get('risks', [])
                self.print_success(f"Risks identified: {len(risks)}")
                
                # Count by severity
                severity_counts = {}
                for risk in risks:
                    severity = risk.get('severity', 'unknown')
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1
                    
                for severity, count in severity_counts.items():
                    print(f"  - {severity}: {count}")
                    
            self.results['risk_detector'] = result
            return result.get('status') == 'success'
            
        except Exception as e:
            self.print_error(f"RiskDetector failed: {str(e)}")
            self.results['risk_detector'] = {'status': 'failed', 'error': str(e)}
            return False
            
    def run_knowledge_synthesizer(self) -> bool:
        """Step 5: Run KnowledgeSynthesizer agent"""
        self.print_step(5, "Q&A Demo (KnowledgeSynthesizer)")
        
        try:
            with open(self.manifest_path, 'r') as f:
                manifest = json.load(f)
                
            # Demo questions
            questions = [
                "What is the main purpose of this repository?",
                "What are the key components and their responsibilities?",
                "Are there any security concerns in the codebase?"
            ]
            
            supervisor = AgentSupervisor()
            results = []
            
            for i, question in enumerate(questions, 1):
                print(f"\nQuestion {i}: {question}")
                
                result = supervisor.run_agent('knowledge_synthesizer', manifest, query=question)
                results.append(result)
                
                if result.get('status') == 'success':
                    answer = result.get('result', {}).get('answer', 'No answer provided')
                    print(f"Answer: {answer[:200]}...")
                    
            # Save results
            output_file = self.output_dir / "knowledge_synthesizer_result.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
                
            self.print_success(f"Q&A demo complete: {output_file}")
            
            self.results['knowledge_synthesizer'] = results
            return all(r.get('status') == 'success' for r in results)
            
        except Exception as e:
            self.print_error(f"KnowledgeSynthesizer failed: {str(e)}")
            self.results['knowledge_synthesizer'] = {'status': 'failed', 'error': str(e)}
            return False
            
    def run_impact_simulator(self) -> bool:
        """Step 6: Run ImpactSimulator agent"""
        self.print_step(6, "Impact Simulation (ImpactSimulator)")
        
        try:
            with open(self.manifest_path, 'r') as f:
                manifest = json.load(f)
                
            # Demo change scenarios
            scenarios = [
                {
                    'file': 'main.py',
                    'change_type': 'modify',
                    'description': 'Update main application logic'
                },
                {
                    'file': 'utils.py',
                    'change_type': 'modify',
                    'description': 'Refactor utility functions'
                }
            ]
            
            supervisor = AgentSupervisor()
            results = []
            
            for i, scenario in enumerate(scenarios, 1):
                print(f"\nScenario {i}: {scenario['description']}")
                
                result = supervisor.run_agent('impact_simulator', manifest, change=scenario)
                results.append(result)
                
                if result.get('status') == 'success':
                    impact = result.get('result', {})
                    affected = impact.get('affected_files', [])
                    self.print_success(f"Affected files: {len(affected)}")
                    
            # Save results
            output_file = self.output_dir / "impact_simulator_result.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
                
            self.print_success(f"Impact simulation complete: {output_file}")
            
            self.results['impact_simulator'] = results
            return all(r.get('status') == 'success' for r in results)
            
        except Exception as e:
            self.print_error(f"ImpactSimulator failed: {str(e)}")
            self.results['impact_simulator'] = {'status': 'failed', 'error': str(e)}
            return False
            
    def test_api_integration(self) -> bool:
        """Step 7: Test API integration"""
        self.print_step(7, "API Integration Test")
        
        try:
            with open(self.manifest_path, 'r') as f:
                manifest = json.load(f)
                
            orchestrator = AnalysisOrchestrator()
            
            # Test full analysis
            print("Running full analysis through orchestrator...")
            result = orchestrator.run_full_analysis(manifest)
            
            # Save result
            output_file = self.output_dir / "api_integration_result.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
                
            self.print_success(f"API integration test complete: {output_file}")
            
            if result.get('status') == 'success':
                self.print_success("All agents executed successfully through API")
                
            self.results['api_integration'] = result
            return result.get('status') == 'success'
            
        except Exception as e:
            self.print_error(f"API integration failed: {str(e)}")
            self.results['api_integration'] = {'status': 'failed', 'error': str(e)}
            return False
            
    def generate_report(self):
        """Step 8: Generate demo report"""
        self.print_step(8, "Generating Demo Report")
        
        end_time = time.time()
        duration = end_time - self.start_time
        
        report = {
            'demo_info': {
                'timestamp': datetime.now().isoformat(),
                'duration_seconds': round(duration, 2),
                'repository': str(self.repo_path),
                'output_directory': str(self.output_dir)
            },
            'results': self.results,
            'summary': {
                'total_steps': 8,
                'successful_steps': sum(1 for r in self.results.values() 
                                       if isinstance(r, dict) and r.get('status') == 'success'),
                'failed_steps': sum(1 for r in self.results.values() 
                                   if isinstance(r, dict) and r.get('status') == 'failed')
            }
        }
        
        # Save report
        report_file = self.output_dir / "demo_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        self.print_header("Demo Summary")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Successful steps: {report['summary']['successful_steps']}/{report['summary']['total_steps']}")
        print(f"Failed steps: {report['summary']['failed_steps']}/{report['summary']['total_steps']}")
        print(f"\nFull report saved to: {report_file}")
        
        return report
        
    def run(self):
        """Run the complete demo"""
        self.start_time = time.time()
        
        self.print_header("CodeOracle End-to-End Demo")
        print(f"Repository: {self.repo_path}")
        print(f"Output Directory: {self.output_dir}")
        
        # Run all steps
        steps = [
            self.run_ingestion,
            self.run_repo_mapper,
            self.run_dependency_analyst,
            self.run_risk_detector,
            self.run_knowledge_synthesizer,
            self.run_impact_simulator,
            self.test_api_integration
        ]
        
        for step in steps:
            success = step()
            if not success:
                print(f"\n⚠ Warning: {step.__name__} failed, continuing with demo...")
                
        # Generate final report
        report = self.generate_report()
        
        self.print_header("Demo Complete!")
        
        return report


def main():
    parser = argparse.ArgumentParser(description='Run CodeOracle end-to-end demo')
    parser.add_argument(
        '--repo-path',
        default='demo/test_repo',
        help='Path to repository to analyze (default: demo/test_repo)'
    )
    parser.add_argument(
        '--output-dir',
        default='demo/demo_output',
        help='Output directory for results (default: demo/demo_output)'
    )
    parser.add_argument(
        '--skip-ingestion',
        action='store_true',
        help='Skip ingestion if manifest already exists'
    )
    
    args = parser.parse_args()
    
    # Run demo
    runner = DemoRunner(args.repo_path, args.output_dir, args.skip_ingestion)
    report = runner.run()
    
    # Exit with appropriate code
    if report['summary']['failed_steps'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()

# Made with Bob
