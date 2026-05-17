#!/usr/bin/env python3
"""
Integration Test for CodeOracle

Tests the complete workflow: ingest → agents → API → results
Verifies data flows correctly through all layers and tests error handling.
"""

import sys
import json
import time
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ingest.ingest import RepositoryIngester
from agents.supervisor import AgentSupervisor
from api.orchestrator import AnalysisOrchestrator


class TestCodeOracleIntegration(unittest.TestCase):
    """Integration tests for CodeOracle system"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_repo_path = Path(__file__).parent / "test_repo"
        cls.output_dir = Path(__file__).parent / "test_output"
        cls.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Run ingestion once for all tests
        print("\nRunning repository ingestion...")
        ingester = RepositoryIngester(str(cls.test_repo_path))
        cls.manifest = ingester.ingest()
        
        # Save manifest
        cls.manifest_path = cls.output_dir / "test_manifest.json"
        with open(cls.manifest_path, 'w') as f:
            json.dump(cls.manifest, f, indent=2)
        
        print(f"Manifest created: {cls.manifest_path}")
        print(f"Files analyzed: {len(cls.manifest.get('files', []))}")
    
    def test_01_ingestion(self):
        """Test repository ingestion"""
        print("\n[TEST] Repository Ingestion")
        
        # Verify manifest structure
        self.assertIn('repository', self.manifest)
        self.assertIn('files', self.manifest)
        self.assertIn('metadata', self.manifest)
        
        # Verify files were parsed
        files = self.manifest.get('files', [])
        self.assertGreater(len(files), 0, "No files were ingested")
        
        # Verify file structure
        for file_data in files:
            self.assertIn('path', file_data)
            self.assertIn('language', file_data)
            self.assertIn('content', file_data)
        
        print(f"✓ Ingestion successful: {len(files)} files")
    
    def test_02_repo_mapper(self):
        """Test RepoMapper agent"""
        print("\n[TEST] RepoMapper Agent")
        
        supervisor = AgentSupervisor()
        result = supervisor.run_agent('repo_mapper', self.manifest)
        
        # Verify result structure
        self.assertEqual(result.get('status'), 'success', 
                        f"RepoMapper failed: {result.get('error')}")
        self.assertIn('result', result)
        
        analysis = result.get('result', {})
        
        # Verify analysis components
        self.assertIn('architecture_overview', analysis)
        self.assertIn('components', analysis)
        self.assertIn('layers', analysis)
        
        components = analysis.get('components', [])
        print(f"✓ RepoMapper successful: {len(components)} components identified")
    
    def test_03_dependency_analyst(self):
        """Test DependencyAnalyst agent"""
        print("\n[TEST] DependencyAnalyst Agent")
        
        supervisor = AgentSupervisor()
        result = supervisor.run_agent('dependency_analyst', self.manifest)
        
        # Verify result structure
        self.assertEqual(result.get('status'), 'success',
                        f"DependencyAnalyst failed: {result.get('error')}")
        self.assertIn('result', result)
        
        analysis = result.get('result', {})
        
        # Verify analysis components
        self.assertIn('dependencies', analysis)
        self.assertIn('dependency_graph', analysis)
        
        dependencies = analysis.get('dependencies', [])
        print(f"✓ DependencyAnalyst successful: {len(dependencies)} dependencies found")
    
    def test_04_risk_detector(self):
        """Test RiskDetector agent"""
        print("\n[TEST] RiskDetector Agent")
        
        supervisor = AgentSupervisor()
        result = supervisor.run_agent('risk_detector', self.manifest)
        
        # Verify result structure
        self.assertEqual(result.get('status'), 'success',
                        f"RiskDetector failed: {result.get('error')}")
        self.assertIn('result', result)
        
        analysis = result.get('result', {})
        
        # Verify analysis components
        self.assertIn('risks', analysis)
        self.assertIn('overall_risk_score', analysis)
        self.assertIn('risk_level', analysis)
        
        risks = analysis.get('risks', [])
        risk_score = analysis.get('overall_risk_score', 0)
        print(f"✓ RiskDetector successful: {len(risks)} risks, score: {risk_score}/100")
    
    def test_05_knowledge_synthesizer(self):
        """Test KnowledgeSynthesizer agent"""
        print("\n[TEST] KnowledgeSynthesizer Agent")
        
        supervisor = AgentSupervisor()
        query = "What is the main purpose of this repository?"
        result = supervisor.run_agent('knowledge_synthesizer', self.manifest, query=query)
        
        # Verify result structure
        self.assertEqual(result.get('status'), 'success',
                        f"KnowledgeSynthesizer failed: {result.get('error')}")
        self.assertIn('result', result)
        
        analysis = result.get('result', {})
        
        # Verify analysis components
        self.assertIn('answer', analysis)
        self.assertIn('confidence', analysis)
        
        answer = analysis.get('answer', '')
        confidence = analysis.get('confidence', 0)
        print(f"✓ KnowledgeSynthesizer successful: confidence {confidence * 100:.1f}%")
    
    def test_06_impact_simulator(self):
        """Test ImpactSimulator agent"""
        print("\n[TEST] ImpactSimulator Agent")
        
        supervisor = AgentSupervisor()
        change = {
            'file': 'main.py',
            'change_type': 'modify',
            'description': 'Test change'
        }
        result = supervisor.run_agent('impact_simulator', self.manifest, change=change)
        
        # Verify result structure
        self.assertEqual(result.get('status'), 'success',
                        f"ImpactSimulator failed: {result.get('error')}")
        self.assertIn('result', result)
        
        analysis = result.get('result', {})
        
        # Verify analysis components
        self.assertIn('impact_level', analysis)
        self.assertIn('affected_files', analysis)
        
        affected = analysis.get('affected_files', [])
        impact_level = analysis.get('impact_level', 'unknown')
        print(f"✓ ImpactSimulator successful: {len(affected)} files affected, level: {impact_level}")
    
    def test_07_api_orchestrator(self):
        """Test API orchestrator"""
        print("\n[TEST] API Orchestrator")
        
        orchestrator = AnalysisOrchestrator()
        result = orchestrator.run_full_analysis(self.manifest)
        
        # Verify result structure
        self.assertEqual(result.get('status'), 'success',
                        f"Orchestrator failed: {result.get('error')}")
        self.assertIn('results', result)
        
        results = result.get('results', {})
        
        # Verify all agents ran
        expected_agents = ['repo_mapper', 'dependency_analyst', 'risk_detector']
        for agent in expected_agents:
            self.assertIn(agent, results, f"Agent {agent} not in results")
        
        print(f"✓ Orchestrator successful: {len(results)} agents executed")
    
    def test_08_data_flow(self):
        """Test data flows correctly through all layers"""
        print("\n[TEST] Data Flow")
        
        # Test: Ingestion → Agent → API
        supervisor = AgentSupervisor()
        
        # Run through supervisor
        agent_result = supervisor.run_agent('repo_mapper', self.manifest)
        self.assertEqual(agent_result.get('status'), 'success')
        
        # Run through orchestrator
        orchestrator = AnalysisOrchestrator()
        api_result = orchestrator.run_full_analysis(self.manifest)
        self.assertEqual(api_result.get('status'), 'success')
        
        # Verify data consistency
        agent_analysis = agent_result.get('result', {})
        api_analysis = api_result.get('results', {}).get('repo_mapper', {}).get('result', {})
        
        # Both should have similar structure
        self.assertIn('components', agent_analysis)
        self.assertIn('components', api_analysis)
        
        print("✓ Data flow verified through all layers")
    
    def test_09_error_handling(self):
        """Test error handling at each layer"""
        print("\n[TEST] Error Handling")
        
        supervisor = AgentSupervisor()
        
        # Test with invalid manifest
        invalid_manifest = {'invalid': 'data'}
        result = supervisor.run_agent('repo_mapper', invalid_manifest)
        
        # Should handle error gracefully
        self.assertIn('status', result)
        # May succeed or fail, but should not crash
        
        print("✓ Error handling verified")
    
    def test_10_performance(self):
        """Test performance benchmarks"""
        print("\n[TEST] Performance Benchmarks")
        
        supervisor = AgentSupervisor()
        
        # Measure agent execution time
        start_time = time.time()
        result = supervisor.run_agent('repo_mapper', self.manifest)
        duration = time.time() - start_time
        
        # Should complete in reasonable time (< 30 seconds)
        self.assertLess(duration, 30, f"Agent took too long: {duration:.2f}s")
        
        print(f"✓ Performance acceptable: {duration:.2f}s")
    
    def test_11_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        print("\n[TEST] End-to-End Workflow")
        
        start_time = time.time()
        
        # Step 1: Ingestion (already done in setUpClass)
        self.assertIsNotNone(self.manifest)
        
        # Step 2: Run all agents
        supervisor = AgentSupervisor()
        agents = ['repo_mapper', 'dependency_analyst', 'risk_detector']
        
        results = {}
        for agent in agents:
            result = supervisor.run_agent(agent, self.manifest)
            results[agent] = result
            self.assertEqual(result.get('status'), 'success',
                           f"Agent {agent} failed in workflow")
        
        # Step 3: Run through orchestrator
        orchestrator = AnalysisOrchestrator()
        api_result = orchestrator.run_full_analysis(self.manifest)
        self.assertEqual(api_result.get('status'), 'success')
        
        duration = time.time() - start_time
        
        print(f"✓ End-to-end workflow successful in {duration:.2f}s")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        print("\n" + "=" * 80)
        print("Integration Tests Complete")
        print("=" * 80)


def run_tests():
    """Run all integration tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestCodeOracleIntegration)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate report
    report = {
        'total_tests': result.testsRun,
        'successful': result.testsRun - len(result.failures) - len(result.errors),
        'failures': len(result.failures),
        'errors': len(result.errors),
        'success_rate': ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    }
    
    # Save report
    output_dir = Path(__file__).parent / "test_output"
    report_file = output_dir / "integration_test_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nTest report saved to: {report_file}")
    print(f"Success rate: {report['success_rate']:.1f}%")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)

# Made with Bob
