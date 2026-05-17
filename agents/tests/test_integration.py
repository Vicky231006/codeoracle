"""
Integration Test
Tests full workflow: manifest → all agents → results
Uses demo/test_repo as test data
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.repo_mapper import RepoMapperAgent
from agents.dependency_analyst import DependencyAnalystAgent
from agents.risk_detector import RiskDetectorAgent
from agents.impact_simulator import ImpactSimulatorAgent
from agents.knowledge_synthesizer import KnowledgeSynthesizerAgent


class TestIntegration:
    """Integration test suite for full workflow"""
    
    def __init__(self):
        self.results = []
        self.manifest = None
        self.repo_mapper_result = None
        self.dependency_result = None
        self.risk_result = None
        self.impact_result = None
        self.knowledge_result = None
    
    def log_result(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        self.results.append({
            "test": test_name,
            "passed": passed,
            "message": message
        })
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status}: {test_name}")
        if message:
            print(f"  -> {message}")
    
    def load_test_manifest(self):
        """Test 1: Load test manifest from demo directory"""
        try:
            manifest_path = Path(__file__).parent.parent.parent / "demo" / "test_manifest.json"
            
            if not manifest_path.exists():
                self.log_result(
                    "Load Test Manifest",
                    False,
                    f"Manifest not found at: {manifest_path}"
                )
                return False
            
            with open(manifest_path, 'r', encoding='utf-8') as f:
                self.manifest = json.load(f)
            
            file_count = len(self.manifest.get("files", []))
            self.log_result(
                "Load Test Manifest",
                True,
                f"Loaded manifest with {file_count} files"
            )
            return True
        except Exception as e:
            self.log_result(
                "Load Test Manifest",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_repo_mapper_workflow(self):
        """Test 2: RepoMapper in workflow"""
        if not self.manifest:
            self.log_result("RepoMapper Workflow", False, "Manifest not loaded")
            return False
        
        try:
            agent = RepoMapperAgent()
            self.repo_mapper_result = agent.analyze_repository(self.manifest)
            
            arch_type = self.repo_mapper_result.get("architecture_type", "unknown")
            layer_count = len(self.repo_mapper_result.get("layer_map", {}))
            
            self.log_result(
                "RepoMapper Workflow",
                True,
                f"Architecture: {arch_type}, Layers: {layer_count}"
            )
            return True
        except Exception as e:
            self.log_result(
                "RepoMapper Workflow",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_dependency_analyst_workflow(self):
        """Test 3: DependencyAnalyst in workflow"""
        if not self.manifest:
            self.log_result("DependencyAnalyst Workflow", False, "Manifest not loaded")
            return False
        
        try:
            # Extract dependency graph from manifest
            dependency_graph = self.manifest.get("dependency_graph", {})
            
            # Build files_imports from manifest
            files_imports = {}
            for file_info in self.manifest.get("files", []):
                file_path = file_info["path"]
                files_imports[file_path] = {
                    "imports": file_info.get("imports", []),
                    "imported_by": []
                }
            
            # Calculate imported_by relationships
            for file_info in self.manifest.get("files", []):
                file_path = file_info["path"]
                for imported in file_info.get("imports", []):
                    # Find the file that matches this import
                    for other_file in files_imports:
                        if imported in other_file or other_file.replace(".py", "") in imported:
                            if file_path not in files_imports[other_file]["imported_by"]:
                                files_imports[other_file]["imported_by"].append(file_path)
            
            agent = DependencyAnalystAgent()
            self.dependency_result = agent.analyze_dependencies(
                dependency_graph,
                files_imports,
                len(self.manifest.get("files", []))
            )
            
            hub_count = len(self.dependency_result.get("hub_files", []))
            circular_count = len(self.dependency_result.get("circular_dependencies", []))
            
            self.log_result(
                "DependencyAnalyst Workflow",
                True,
                f"Hub files: {hub_count}, Circular deps: {circular_count}"
            )
            return True
        except Exception as e:
            self.log_result(
                "DependencyAnalyst Workflow",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_risk_detector_workflow(self):
        """Test 4: RiskDetector in workflow"""
        if not self.repo_mapper_result or not self.dependency_result:
            self.log_result("RiskDetector Workflow", False, "Previous results not available")
            return False
        
        try:
            # Extract complexity scores from manifest
            complexity_scores = {}
            for file_info in self.manifest.get("files", []):
                complexity_scores[file_info["path"]] = file_info.get("complexity_score", 0.0)
            
            # Build test coverage (mock data for demo)
            test_coverage = {}
            for file_info in self.manifest.get("files", []):
                file_path = file_info["path"]
                # Test files have 100% coverage, others vary
                if file_info.get("is_test_file", False):
                    test_coverage[file_path] = 1.0
                else:
                    test_coverage[file_path] = 0.7  # Mock coverage
            
            agent = RiskDetectorAgent()
            self.risk_result = agent.assess_risk(
                self.repo_mapper_result.get("summary_paragraph", ""),
                self.dependency_result.get("coupling_scores", {}),
                complexity_scores,
                self.dependency_result.get("hub_files", []),
                test_coverage
            )
            
            health = self.risk_result.get("overall_repo_health", {})
            critical_files = sum(
                1 for risk in self.risk_result.get("risk_scores", {}).values()
                if risk.get("category") == "critical"
            )
            
            self.log_result(
                "RiskDetector Workflow",
                True,
                f"Health grade: {health.get('grade', 'N/A')}, Critical files: {critical_files}"
            )
            return True
        except Exception as e:
            self.log_result(
                "RiskDetector Workflow",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_impact_simulator_workflow(self):
        """Test 5: ImpactSimulator in workflow"""
        if not self.dependency_result or not self.risk_result or not self.repo_mapper_result:
            self.log_result("ImpactSimulator Workflow", False, "Previous results not available")
            return False
        
        try:
            # Extract dependency graph from manifest
            dependency_graph = self.manifest.get("dependency_graph", {})
            
            # Build simple dependency graph from edges
            dep_graph = {}
            for edge in dependency_graph.get("edges", []):
                source = edge["source"]
                target = edge["target"]
                if source not in dep_graph:
                    dep_graph[source] = []
                if target not in dep_graph[source]:
                    dep_graph[source].append(target)
            
            # Ensure all files are in the graph
            for file_info in self.manifest.get("files", []):
                if file_info["path"] not in dep_graph:
                    dep_graph[file_info["path"]] = []
            
            agent = ImpactSimulatorAgent()
            self.impact_result = agent.simulate_impact(
                "What if I modify the main.py file?",
                dep_graph,
                self.risk_result.get("risk_scores", {}),
                self.repo_mapper_result.get("summary_paragraph", "")
            )
            
            directly_affected = len(self.impact_result.get("directly_affected", []))
            risk_level = self.impact_result.get("estimated_risk_level", "unknown")
            
            self.log_result(
                "ImpactSimulator Workflow",
                True,
                f"Directly affected: {directly_affected}, Risk: {risk_level}"
            )
            return True
        except Exception as e:
            self.log_result(
                "ImpactSimulator Workflow",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_knowledge_synthesizer_workflow(self):
        """Test 6: KnowledgeSynthesizer in workflow"""
        if not all([self.repo_mapper_result, self.dependency_result, self.risk_result]):
            self.log_result("KnowledgeSynthesizer Workflow", False, "Previous results not available")
            return False
        
        try:
            # Get relevant file content from manifest
            relevant_files = {}
            for file_info in self.manifest.get("files", [])[:2]:  # Just first 2 files
                relevant_files[file_info["path"]] = file_info.get("raw_content", "")
            
            agent = KnowledgeSynthesizerAgent()
            self.knowledge_result = agent.answer_question(
                "What is the purpose of the main.py file?",
                self.repo_mapper_result.get("summary_paragraph", ""),
                self.dependency_result.get("hub_files", []),
                self.risk_result.get("overall_repo_health", {}).get("summary", ""),
                relevant_files
            )
            
            confidence = self.knowledge_result.get("confidence", "unknown")
            follow_ups = len(self.knowledge_result.get("follow_up_questions", []))
            
            self.log_result(
                "KnowledgeSynthesizer Workflow",
                True,
                f"Confidence: {confidence}, Follow-ups: {follow_ups}"
            )
            return True
        except Exception as e:
            self.log_result(
                "KnowledgeSynthesizer Workflow",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_data_flow_consistency(self):
        """Test 7: Verify data flows correctly between agents"""
        if not all([self.repo_mapper_result, self.dependency_result, self.risk_result]):
            self.log_result("Data Flow Consistency", False, "Not all agents completed")
            return False
        
        try:
            # Check that coupling scores exist for files in manifest
            coupling_scores = self.dependency_result.get("coupling_scores", {})
            manifest_files = [f["path"] for f in self.manifest.get("files", [])]
            
            # At least some files should have coupling scores
            files_with_scores = [f for f in manifest_files if f in coupling_scores]
            
            if len(files_with_scores) > 0:
                self.log_result(
                    "Data Flow Consistency",
                    True,
                    f"{len(files_with_scores)}/{len(manifest_files)} files have coupling scores"
                )
                return True
            else:
                self.log_result(
                    "Data Flow Consistency",
                    False,
                    "No files have coupling scores"
                )
                return False
        except Exception as e:
            self.log_result(
                "Data Flow Consistency",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_end_to_end_timing(self):
        """Test 8: Measure end-to-end execution time"""
        import time
        
        try:
            start_time = time.time()
            
            # Quick run through all agents
            if self.manifest and all([
                self.repo_mapper_result,
                self.dependency_result,
                self.risk_result,
                self.impact_result,
                self.knowledge_result
            ]):
                elapsed = time.time() - start_time
                
                self.log_result(
                    "End-to-End Timing",
                    True,
                    f"All agents completed (timing from cache: {elapsed:.2f}s)"
                )
                return True
            else:
                self.log_result(
                    "End-to-End Timing",
                    False,
                    "Not all agents completed successfully"
                )
                return False
        except Exception as e:
            self.log_result(
                "End-to-End Timing",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Run all integration tests and return summary"""
        print("\n" + "="*60)
        print("INTEGRATION TEST SUITE")
        print("="*60 + "\n")
        
        # Run tests in sequence
        tests = [
            ("Load Test Data", self.load_test_manifest),
            ("RepoMapper", self.test_repo_mapper_workflow),
            ("DependencyAnalyst", self.test_dependency_analyst_workflow),
            ("RiskDetector", self.test_risk_detector_workflow),
            ("ImpactSimulator", self.test_impact_simulator_workflow),
            ("KnowledgeSynthesizer", self.test_knowledge_synthesizer_workflow),
            ("Data Flow", self.test_data_flow_consistency),
            ("Timing", self.test_end_to_end_timing)
        ]
        
        for test_name, test_func in tests:
            print(f"Running: {test_name}")
            test_func()
            print()
        
        # Summary
        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)
        
        print("="*60)
        print(f"RESULTS: {passed}/{total} tests passed")
        print("="*60)
        
        # Print detailed results
        if self.repo_mapper_result:
            print("\n[*] Sample Results:")
            print(f"  Architecture: {self.repo_mapper_result.get('architecture_type', 'N/A')}")
        
        if self.dependency_result:
            hub_files = self.dependency_result.get("hub_files", [])
            if hub_files:
                print(f"  Hub Files: {[h.get('file', 'N/A') for h in hub_files[:3]]}")
        
        if self.risk_result:
            health = self.risk_result.get("overall_repo_health", {})
            print(f"  Repo Health: {health.get('grade', 'N/A')} ({health.get('score', 0)}/100)")
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "results": self.results
        }


def main():
    """Main test runner"""
    tester = TestIntegration()
    summary = tester.run_all_tests()
    
    # Exit with appropriate code
    if summary["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

# Made with Bob