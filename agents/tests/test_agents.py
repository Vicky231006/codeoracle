"""
Test Individual Agents
Tests each of the 5 CodeOracle agents with sample data
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
from jsonschema import validate, ValidationError


class TestAgents:
    """Test suite for individual agents"""
    
    def __init__(self):
        self.results = []
    
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
    
    def get_sample_manifest(self):
        """Get sample manifest for testing"""
        return {
            "files": [
                {
                    "path": "main.py",
                    "language": "python",
                    "lines": 26,
                    "size": 478,
                    "imports": ["utils", "config"],
                    "functions": ["main"],
                    "complexity_score": 10.0
                },
                {
                    "path": "utils.py",
                    "language": "python",
                    "lines": 45,
                    "size": 803,
                    "imports": [],
                    "functions": ["calculate_sum", "format_output"],
                    "complexity_score": 20.0
                },
                {
                    "path": "config.py",
                    "language": "python",
                    "lines": 18,
                    "size": 278,
                    "imports": [],
                    "functions": [],
                    "complexity_score": 5.0
                },
                {
                    "path": "tests/test_main.py",
                    "language": "python",
                    "lines": 39,
                    "size": 1029,
                    "imports": ["main", "utils"],
                    "functions": ["test_calculate_sum"],
                    "complexity_score": 10.0,
                    "is_test_file": True
                }
            ]
        }
    
    def test_repo_mapper_initialization(self):
        """Test 1: RepoMapper agent initialization"""
        try:
            agent = RepoMapperAgent()
            
            if agent.agent_name == "repo_mapper":
                self.log_result(
                    "RepoMapper - Initialization",
                    True,
                    f"Agent name: {agent.agent_name}"
                )
                return True, agent
            else:
                self.log_result(
                    "RepoMapper - Initialization",
                    False,
                    f"Wrong agent name: {agent.agent_name}"
                )
                return False, None
        except Exception as e:
            self.log_result(
                "RepoMapper - Initialization",
                False,
                f"Error: {str(e)}"
            )
            return False, None
    
    def test_repo_mapper_process(self, agent):
        """Test 2: RepoMapper processing with sample data"""
        if not agent:
            self.log_result("RepoMapper - Process", False, "Agent not initialized")
            return False, None
        
        try:
            manifest = self.get_sample_manifest()
            result = agent.process(manifest=manifest)
            
            # Check required fields
            required_fields = ["architecture_type", "layer_map", "service_boundaries", "summary_paragraph"]
            missing_fields = [f for f in required_fields if f not in result]
            
            if not missing_fields:
                self.log_result(
                    "RepoMapper - Process",
                    True,
                    f"Architecture: {result.get('architecture_type', 'N/A')}"
                )
                return True, result
            else:
                self.log_result(
                    "RepoMapper - Process",
                    False,
                    f"Missing fields: {missing_fields}"
                )
                return False, None
        except Exception as e:
            self.log_result(
                "RepoMapper - Process",
                False,
                f"Error: {str(e)}"
            )
            return False, None
    
    def test_repo_mapper_schema(self, result):
        """Test 3: RepoMapper output schema validation"""
        if not result:
            self.log_result("RepoMapper - Schema Validation", False, "No result to validate")
            return False
        
        try:
            agent = RepoMapperAgent()
            agent._validate_output(result)
            
            self.log_result(
                "RepoMapper - Schema Validation",
                True,
                "Output matches schema"
            )
            return True
        except ValidationError as e:
            self.log_result(
                "RepoMapper - Schema Validation",
                False,
                f"Schema validation failed: {str(e)}"
            )
            return False
        except Exception as e:
            self.log_result(
                "RepoMapper - Schema Validation",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_dependency_analyst_initialization(self):
        """Test 4: DependencyAnalyst agent initialization"""
        try:
            agent = DependencyAnalystAgent()
            
            if agent.agent_name == "dependency_analyst":
                self.log_result(
                    "DependencyAnalyst - Initialization",
                    True,
                    f"Agent name: {agent.agent_name}"
                )
                return True, agent
            else:
                self.log_result(
                    "DependencyAnalyst - Initialization",
                    False,
                    f"Wrong agent name: {agent.agent_name}"
                )
                return False, None
        except Exception as e:
            self.log_result(
                "DependencyAnalyst - Initialization",
                False,
                f"Error: {str(e)}"
            )
            return False, None
    
    def test_dependency_analyst_process(self, agent):
        """Test 5: DependencyAnalyst processing with sample data"""
        if not agent:
            self.log_result("DependencyAnalyst - Process", False, "Agent not initialized")
            return False, None
        
        try:
            dependency_graph = {
                "main.py": ["utils.py", "config.py"],
                "utils.py": ["config.py"],
                "config.py": [],
                "tests/test_main.py": ["main.py"]
            }
            
            files_imports = {
                "main.py": {"imports": ["utils", "config"], "imported_by": ["tests/test_main.py"]},
                "utils.py": {"imports": ["config"], "imported_by": ["main.py"]},
                "config.py": {"imports": [], "imported_by": ["main.py", "utils.py"]},
                "tests/test_main.py": {"imports": ["main"], "imported_by": []}
            }
            
            result = agent.process(
                dependency_graph=dependency_graph,
                files_imports=files_imports,
                total_files=4
            )
            
            # Check required fields
            required_fields = ["coupling_scores", "circular_dependencies", "orphan_files", "hub_files", "external_risk"]
            missing_fields = [f for f in required_fields if f not in result]
            
            if not missing_fields:
                self.log_result(
                    "DependencyAnalyst - Process",
                    True,
                    f"Hub files found: {len(result.get('hub_files', []))}"
                )
                return True, result
            else:
                self.log_result(
                    "DependencyAnalyst - Process",
                    False,
                    f"Missing fields: {missing_fields}"
                )
                return False, None
        except Exception as e:
            self.log_result(
                "DependencyAnalyst - Process",
                False,
                f"Error: {str(e)}"
            )
            return False, None
    
    def test_dependency_analyst_schema(self, result):
        """Test 6: DependencyAnalyst output schema validation"""
        if not result:
            self.log_result("DependencyAnalyst - Schema Validation", False, "No result to validate")
            return False
        
        try:
            agent = DependencyAnalystAgent()
            agent._validate_output(result)
            
            self.log_result(
                "DependencyAnalyst - Schema Validation",
                True,
                "Output matches schema"
            )
            return True
        except ValidationError as e:
            self.log_result(
                "DependencyAnalyst - Schema Validation",
                False,
                f"Schema validation failed: {str(e)}"
            )
            return False
        except Exception as e:
            self.log_result(
                "DependencyAnalyst - Schema Validation",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_risk_detector_initialization(self):
        """Test 7: RiskDetector agent initialization"""
        try:
            agent = RiskDetectorAgent()
            
            if agent.agent_name == "risk_detector":
                self.log_result(
                    "RiskDetector - Initialization",
                    True,
                    f"Agent name: {agent.agent_name}"
                )
                return True, agent
            else:
                self.log_result(
                    "RiskDetector - Initialization",
                    False,
                    f"Wrong agent name: {agent.agent_name}"
                )
                return False, None
        except Exception as e:
            self.log_result(
                "RiskDetector - Initialization",
                False,
                f"Error: {str(e)}"
            )
            return False, None
    
    def test_risk_detector_process(self, agent):
        """Test 8: RiskDetector processing with sample data"""
        if not agent:
            self.log_result("RiskDetector - Process", False, "Agent not initialized")
            return False, None
        
        try:
            result = agent.process(
                architecture_summary="This is a monolithic Python application with clear separation of concerns.",
                coupling_scores={"main.py": 0.75, "utils.py": 0.5, "config.py": 0.8},
                complexity_scores={"main.py": 45.0, "utils.py": 30.0, "config.py": 15.0},
                hub_files=[{"file": "config.py", "imported_by_count": 8, "explanation": "Central config"}],
                test_coverage={"main.py": 0.8, "utils.py": 0.6, "config.py": 0.0}
            )
            
            # Check required fields
            required_fields = ["risk_scores", "single_points_of_failure", "dead_code_candidates", 
                             "complexity_hotspots", "overall_repo_health"]
            missing_fields = [f for f in required_fields if f not in result]
            
            if not missing_fields:
                health = result.get("overall_repo_health", {})
                self.log_result(
                    "RiskDetector - Process",
                    True,
                    f"Repo health grade: {health.get('grade', 'N/A')}"
                )
                return True, result
            else:
                self.log_result(
                    "RiskDetector - Process",
                    False,
                    f"Missing fields: {missing_fields}"
                )
                return False, None
        except Exception as e:
            self.log_result(
                "RiskDetector - Process",
                False,
                f"Error: {str(e)}"
            )
            return False, None
    
    def test_risk_detector_schema(self, result):
        """Test 9: RiskDetector output schema validation"""
        if not result:
            self.log_result("RiskDetector - Schema Validation", False, "No result to validate")
            return False
        
        try:
            agent = RiskDetectorAgent()
            agent._validate_output(result)
            
            self.log_result(
                "RiskDetector - Schema Validation",
                True,
                "Output matches schema"
            )
            return True
        except ValidationError as e:
            self.log_result(
                "RiskDetector - Schema Validation",
                False,
                f"Schema validation failed: {str(e)}"
            )
            return False
        except Exception as e:
            self.log_result(
                "RiskDetector - Schema Validation",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_impact_simulator_initialization(self):
        """Test 10: ImpactSimulator agent initialization"""
        try:
            agent = ImpactSimulatorAgent()
            
            if agent.agent_name == "impact_simulator":
                self.log_result(
                    "ImpactSimulator - Initialization",
                    True,
                    f"Agent name: {agent.agent_name}"
                )
                return True, agent
            else:
                self.log_result(
                    "ImpactSimulator - Initialization",
                    False,
                    f"Wrong agent name: {agent.agent_name}"
                )
                return False, None
        except Exception as e:
            self.log_result(
                "ImpactSimulator - Initialization",
                False,
                f"Error: {str(e)}"
            )
            return False, None
    
    def test_impact_simulator_process(self, agent):
        """Test 11: ImpactSimulator processing with sample data"""
        if not agent:
            self.log_result("ImpactSimulator - Process", False, "Agent not initialized")
            return False, None
        
        try:
            result = agent.process(
                user_scenario="What if I delete the config.py file?",
                dependency_graph={
                    "main.py": ["utils.py", "config.py"],
                    "utils.py": ["config.py"],
                    "config.py": [],
                    "tests/test_main.py": ["main.py"]
                },
                risk_scores={
                    "main.py": {"score": 0.6, "reasons": ["Medium coupling"], "category": "medium"},
                    "config.py": {"score": 0.85, "reasons": ["High coupling"], "category": "critical"}
                },
                architecture_summary="This is a monolithic Python application."
            )
            
            # Check required fields
            required_fields = ["scenario", "directly_affected", "transitively_affected", 
                             "services_affected", "estimated_risk_level", "mitigation_steps", "confidence"]
            missing_fields = [f for f in required_fields if f not in result]
            
            if not missing_fields:
                self.log_result(
                    "ImpactSimulator - Process",
                    True,
                    f"Risk level: {result.get('estimated_risk_level', 'N/A')}"
                )
                return True, result
            else:
                self.log_result(
                    "ImpactSimulator - Process",
                    False,
                    f"Missing fields: {missing_fields}"
                )
                return False, None
        except Exception as e:
            self.log_result(
                "ImpactSimulator - Process",
                False,
                f"Error: {str(e)}"
            )
            return False, None
    
    def test_impact_simulator_schema(self, result):
        """Test 12: ImpactSimulator output schema validation"""
        if not result:
            self.log_result("ImpactSimulator - Schema Validation", False, "No result to validate")
            return False
        
        try:
            agent = ImpactSimulatorAgent()
            agent._validate_output(result)
            
            self.log_result(
                "ImpactSimulator - Schema Validation",
                True,
                "Output matches schema"
            )
            return True
        except ValidationError as e:
            self.log_result(
                "ImpactSimulator - Schema Validation",
                False,
                f"Schema validation failed: {str(e)}"
            )
            return False
        except Exception as e:
            self.log_result(
                "ImpactSimulator - Schema Validation",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_knowledge_synthesizer_initialization(self):
        """Test 13: KnowledgeSynthesizer agent initialization"""
        try:
            agent = KnowledgeSynthesizerAgent()
            
            if agent.agent_name == "knowledge_synthesizer":
                self.log_result(
                    "KnowledgeSynthesizer - Initialization",
                    True,
                    f"Agent name: {agent.agent_name}"
                )
                return True, agent
            else:
                self.log_result(
                    "KnowledgeSynthesizer - Initialization",
                    False,
                    f"Wrong agent name: {agent.agent_name}"
                )
                return False, None
        except Exception as e:
            self.log_result(
                "KnowledgeSynthesizer - Initialization",
                False,
                f"Error: {str(e)}"
            )
            return False, None
    
    def test_knowledge_synthesizer_process(self, agent):
        """Test 14: KnowledgeSynthesizer processing with sample data"""
        if not agent:
            self.log_result("KnowledgeSynthesizer - Process", False, "Agent not initialized")
            return False, None
        
        try:
            result = agent.process(
                user_question="How does the main.py file work?",
                architecture_summary="This is a monolithic Python application.",
                hub_files=[{"file": "config.py", "imported_by_count": 8}],
                risk_summary="The repository has medium risk.",
                relevant_files_content={
                    "main.py": "def main():\n    from config import settings\n    print(settings.app_name)",
                    "config.py": "class Settings:\n    app_name = 'MyApp'"
                }
            )
            
            # Check required fields
            required_fields = ["answer", "confidence", "relevant_files", "follow_up_questions", "impact_chain"]
            missing_fields = [f for f in required_fields if f not in result]
            
            if not missing_fields:
                self.log_result(
                    "KnowledgeSynthesizer - Process",
                    True,
                    f"Confidence: {result.get('confidence', 'N/A')}"
                )
                return True, result
            else:
                self.log_result(
                    "KnowledgeSynthesizer - Process",
                    False,
                    f"Missing fields: {missing_fields}"
                )
                return False, None
        except Exception as e:
            self.log_result(
                "KnowledgeSynthesizer - Process",
                False,
                f"Error: {str(e)}"
            )
            return False, None
    
    def test_knowledge_synthesizer_schema(self, result):
        """Test 15: KnowledgeSynthesizer output schema validation"""
        if not result:
            self.log_result("KnowledgeSynthesizer - Schema Validation", False, "No result to validate")
            return False
        
        try:
            agent = KnowledgeSynthesizerAgent()
            agent._validate_output(result)
            
            self.log_result(
                "KnowledgeSynthesizer - Schema Validation",
                True,
                "Output matches schema"
            )
            return True
        except ValidationError as e:
            self.log_result(
                "KnowledgeSynthesizer - Schema Validation",
                False,
                f"Schema validation failed: {str(e)}"
            )
            return False
        except Exception as e:
            self.log_result(
                "KnowledgeSynthesizer - Schema Validation",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_error_handling_missing_params(self):
        """Test 16: Error handling with missing parameters"""
        try:
            agent = RepoMapperAgent()
            
            try:
                # Try to process without required manifest parameter
                agent.process()
                self.log_result(
                    "Error Handling - Missing Parameters",
                    False,
                    "Expected error but got success"
                )
                return False
            except ValueError as e:
                # Expected to fail
                self.log_result(
                    "Error Handling - Missing Parameters",
                    True,
                    f"Correctly caught error: {type(e).__name__}"
                )
                return True
        except Exception as e:
            self.log_result(
                "Error Handling - Missing Parameters",
                False,
                f"Unexpected error: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Run all tests and return summary"""
        print("\n" + "="*60)
        print("INDIVIDUAL AGENTS TEST SUITE")
        print("="*60 + "\n")
        
        # RepoMapper tests
        print("--- RepoMapper Agent ---")
        passed, repo_agent = self.test_repo_mapper_initialization()
        print()
        
        if passed:
            passed, repo_result = self.test_repo_mapper_process(repo_agent)
            print()
            
            if passed:
                self.test_repo_mapper_schema(repo_result)
                print()
        
        # DependencyAnalyst tests
        print("--- DependencyAnalyst Agent ---")
        passed, dep_agent = self.test_dependency_analyst_initialization()
        print()
        
        if passed:
            passed, dep_result = self.test_dependency_analyst_process(dep_agent)
            print()
            
            if passed:
                self.test_dependency_analyst_schema(dep_result)
                print()
        
        # RiskDetector tests
        print("--- RiskDetector Agent ---")
        passed, risk_agent = self.test_risk_detector_initialization()
        print()
        
        if passed:
            passed, risk_result = self.test_risk_detector_process(risk_agent)
            print()
            
            if passed:
                self.test_risk_detector_schema(risk_result)
                print()
        
        # ImpactSimulator tests
        print("--- ImpactSimulator Agent ---")
        passed, impact_agent = self.test_impact_simulator_initialization()
        print()
        
        if passed:
            passed, impact_result = self.test_impact_simulator_process(impact_agent)
            print()
            
            if passed:
                self.test_impact_simulator_schema(impact_result)
                print()
        
        # KnowledgeSynthesizer tests
        print("--- KnowledgeSynthesizer Agent ---")
        passed, synth_agent = self.test_knowledge_synthesizer_initialization()
        print()
        
        if passed:
            passed, synth_result = self.test_knowledge_synthesizer_process(synth_agent)
            print()
            
            if passed:
                self.test_knowledge_synthesizer_schema(synth_result)
                print()
        
        # Error handling tests
        print("--- Error Handling Tests ---")
        self.test_error_handling_missing_params()
        print()
        
        # Summary
        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)
        
        print("="*60)
        print(f"RESULTS: {passed}/{total} tests passed")
        print("="*60)
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "results": self.results
        }


def main():
    """Main test runner"""
    tester = TestAgents()
    summary = tester.run_all_tests()
    
    # Exit with appropriate code
    if summary["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

# Made with Bob