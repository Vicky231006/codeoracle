"""
Tests for Supervisor Agent
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from agents.supervisor import SupervisorAgent, create_supervisor
from agents.base_llm import BaseLLM


class MockLLM(BaseLLM):
    """Mock LLM for testing"""
    
    def __init__(self, responses=None):
        self.responses = responses or {}
        self.call_count = 0
    
    def generate(self, prompt, temperature=0.1, max_tokens=4096):
        """Implement abstract generate method"""
        return "Mock response"
    
    def generate_json(self, prompt, temperature=0.1, max_tokens=4096):
        self.call_count += 1
        
        # Return appropriate response based on prompt content
        prompt_lower = prompt.lower()
        
        if "supervisor" in prompt_lower or "orchestration" in prompt_lower:
            # Supervisor routing response - check in order of specificity
            # Check single intents first (more specific)
            if "what if" in prompt_lower and "delete" in prompt_lower:
                return {
                    "intent": "Simulate impact of change",
                    "agents_to_invoke": ["impact_simulator"],
                    "reasoning": "User wants to simulate a hypothetical change",
                    "is_multi_intent": False
                }
            elif "how does" in prompt_lower and "work" in prompt_lower:
                return {
                    "intent": "Answer question about codebase",
                    "agents_to_invoke": ["knowledge_synthesizer"],
                    "reasoning": "User has a specific question about the code",
                    "is_multi_intent": False
                }
            # Check multi-intent (must have both analyze AND assess/risk keywords)
            elif ("analyze" in prompt_lower and "assess" in prompt_lower) or ("architecture" in prompt_lower and "risk" in prompt_lower):
                return {
                    "intent": "Analyze architecture and assess risks",
                    "agents_to_invoke": ["repo_mapper", "dependency_analyst", "risk_detector"],
                    "reasoning": "Multi-intent query requires architecture analysis and risk assessment",
                    "is_multi_intent": True
                }
            elif "architecture" in prompt_lower or "structure" in prompt_lower:
                return {
                    "intent": "Analyze repository architecture",
                    "agents_to_invoke": ["repo_mapper"],
                    "reasoning": "User wants to understand the architecture",
                    "is_multi_intent": False
                }
            elif "dependencies" in prompt_lower or "coupling" in prompt_lower:
                return {
                    "intent": "Analyze dependencies",
                    "agents_to_invoke": ["dependency_analyst"],
                    "reasoning": "User wants dependency analysis",
                    "is_multi_intent": False
                }
            elif "risk" in prompt_lower or "safe" in prompt_lower:
                return {
                    "intent": "Assess change risk",
                    "agents_to_invoke": ["risk_detector"],
                    "reasoning": "User wants risk assessment",
                    "is_multi_intent": False
                }
        
        # Default repo_mapper response
        if "repo_mapper" in str(self.responses):
            return self.responses.get("repo_mapper", {})
        
        return {
            "intent": "General query",
            "agents_to_invoke": ["repo_mapper"],
            "reasoning": "Default routing",
            "is_multi_intent": False
        }


@pytest.fixture
def mock_llm():
    """Create mock LLM"""
    return MockLLM()


@pytest.fixture
def supervisor_agent(mock_llm):
    """Create supervisor agent with mock LLM"""
    return SupervisorAgent(llm=mock_llm)


@pytest.fixture
def sample_manifest():
    """Sample repository manifest"""
    return {
        "files": [
            {"path": "main.py", "language": "python", "size": 1024},
            {"path": "utils.py", "language": "python", "size": 512},
            {"path": "config.py", "language": "python", "size": 256}
        ]
    }


@pytest.fixture
def sample_dependency_graph():
    """Sample dependency graph"""
    return {
        "main.py": ["utils.py", "config.py"],
        "utils.py": ["config.py"],
        "config.py": []
    }


@pytest.fixture
def sample_files_imports():
    """Sample import information"""
    return {
        "main.py": {"imports": ["utils", "config"], "imported_by": []},
        "utils.py": {"imports": ["config"], "imported_by": ["main.py"]},
        "config.py": {"imports": [], "imported_by": ["main.py", "utils.py"]}
    }


@pytest.fixture
def sample_complexity_scores():
    """Sample complexity scores"""
    return {
        "main.py": 45.0,
        "utils.py": 30.0,
        "config.py": 15.0
    }


@pytest.fixture
def sample_test_coverage():
    """Sample test coverage"""
    return {
        "main.py": 0.8,
        "utils.py": 0.6,
        "config.py": 0.0
    }


class TestSupervisorAgent:
    """Test suite for SupervisorAgent"""
    
    def test_agent_initialization(self, supervisor_agent):
        """Test agent initializes correctly"""
        assert supervisor_agent.agent_name == "supervisor"
        assert supervisor_agent.repo_mapper is not None
        assert supervisor_agent.dependency_analyst is not None
        assert supervisor_agent.risk_detector is not None
        assert supervisor_agent.knowledge_synthesizer is not None
        assert supervisor_agent.impact_simulator is not None
        assert isinstance(supervisor_agent.context_cache, dict)
    
    def test_factory_function(self):
        """Test factory function creates agent"""
        agent = create_supervisor()
        assert isinstance(agent, SupervisorAgent)
        assert agent.agent_name == "supervisor"
    
    def test_route_query_single_intent(self, supervisor_agent):
        """Test routing for single-intent query"""
        query = "What is the architecture of this repository?"
        available_context = {"manifest": True}
        
        result = supervisor_agent.route_query(query, available_context)
        
        assert "intent" in result
        assert "agents_to_invoke" in result
        assert "reasoning" in result
        assert "is_multi_intent" in result
        assert isinstance(result["agents_to_invoke"], list)
    
    def test_route_query_multi_intent(self, supervisor_agent):
        """Test routing for multi-intent query"""
        query = "Analyze the architecture and assess the risks"
        available_context = {"manifest": True, "dependency_graph": True}
        
        result = supervisor_agent.route_query(query, available_context)
        
        assert result["is_multi_intent"] == True
        assert len(result["agents_to_invoke"]) > 1
    
    def test_route_query_impact_simulation(self, supervisor_agent):
        """Test routing for impact simulation query"""
        query = "What if I delete the config.py file?"
        available_context = {"dependency_graph": True}
        
        result = supervisor_agent.route_query(query, available_context)
        
        assert "impact_simulator" in result["agents_to_invoke"]
    
    def test_route_query_knowledge_synthesis(self, supervisor_agent):
        """Test routing for Q&A query"""
        query = "How does the main.py file work?"
        available_context = {"architecture_summary": True}
        
        result = supervisor_agent.route_query(query, available_context)
        
        assert "knowledge_synthesizer" in result["agents_to_invoke"]
    
    def test_get_available_context(self, supervisor_agent, sample_manifest):
        """Test context availability checking"""
        kwargs = {
            "manifest": sample_manifest,
            "dependency_graph": {"main.py": []},
            "total_files": 3
        }
        
        available = supervisor_agent._get_available_context(kwargs)
        
        assert available["manifest"] == True
        assert available["dependency_graph"] == True
        assert "architecture_summary" in available
    
    def test_context_caching(self, supervisor_agent):
        """Test context caching functionality"""
        # Initially empty
        assert len(supervisor_agent.context_cache) == 0
        
        # Add to cache
        supervisor_agent.context_cache["repo_mapper_result"] = {"test": "data"}
        
        # Check cache
        cached = supervisor_agent.get_cached_context()
        assert "repo_mapper_result" in cached
        assert cached["repo_mapper_result"]["test"] == "data"
        
        # Clear cache
        supervisor_agent.clear_cache()
        assert len(supervisor_agent.context_cache) == 0
    
    @patch.object(SupervisorAgent, '_invoke_repo_mapper')
    def test_execute_workflow_single_agent(self, mock_invoke, supervisor_agent):
        """Test workflow execution with single agent"""
        mock_invoke.return_value = {
            "architecture_type": "monolith",
            "summary_paragraph": "Test summary"
        }
        
        routing_decision = {
            "intent": "Analyze architecture",
            "agents_to_invoke": ["repo_mapper"],
            "reasoning": "Test",
            "is_multi_intent": False
        }
        
        context = {"manifest": {"files": []}}
        
        results = supervisor_agent.execute_workflow("test query", routing_decision, context)
        
        assert "repo_mapper" in results
        assert mock_invoke.called
    
    @patch.object(SupervisorAgent, '_invoke_repo_mapper')
    @patch.object(SupervisorAgent, '_invoke_dependency_analyst')
    def test_execute_workflow_multiple_agents(
        self,
        mock_dep,
        mock_repo,
        supervisor_agent
    ):
        """Test workflow execution with multiple agents"""
        mock_repo.return_value = {
            "architecture_type": "monolith",
            "summary_paragraph": "Test summary"
        }
        mock_dep.return_value = {
            "coupling_scores": {"main.py": 0.5},
            "hub_files": []
        }
        
        routing_decision = {
            "intent": "Analyze architecture and dependencies",
            "agents_to_invoke": ["repo_mapper", "dependency_analyst"],
            "reasoning": "Test",
            "is_multi_intent": True
        }
        
        context = {
            "manifest": {"files": []},
            "dependency_graph": {},
            "files_imports": {},
            "total_files": 3
        }
        
        results = supervisor_agent.execute_workflow("test query", routing_decision, context)
        
        assert "repo_mapper" in results
        assert "dependency_analyst" in results
        assert mock_repo.called
        assert mock_dep.called
    
    def test_execute_workflow_error_handling(self, supervisor_agent):
        """Test workflow handles agent errors gracefully"""
        routing_decision = {
            "intent": "Test",
            "agents_to_invoke": ["repo_mapper"],
            "reasoning": "Test",
            "is_multi_intent": False
        }
        
        # Missing required context will cause error
        context = {}
        
        results = supervisor_agent.execute_workflow("test query", routing_decision, context)
        
        assert "repo_mapper" in results
        assert "error" in results["repo_mapper"]
        assert results["repo_mapper"]["status"] == "failed"
    
    def test_aggregate_results_single_agent(self, supervisor_agent):
        """Test result aggregation for single agent"""
        agent_results = {
            "repo_mapper": {
                "architecture_type": "monolith",
                "summary_paragraph": "Test summary"
            }
        }
        
        routing_decision = {
            "intent": "Analyze architecture",
            "agents_to_invoke": ["repo_mapper"],
            "reasoning": "Test",
            "is_multi_intent": False
        }
        
        aggregated = supervisor_agent.aggregate_results(agent_results, routing_decision)
        
        assert "intent" in aggregated
        assert "agents_invoked" in aggregated
        assert "results" in aggregated
        assert "summary" in aggregated
        assert "is_multi_intent" in aggregated
        assert "repo_mapper" in aggregated["agents_invoked"]
        assert "Architecture: monolith" in aggregated["summary"]
    
    def test_aggregate_results_multiple_agents(self, supervisor_agent):
        """Test result aggregation for multiple agents"""
        agent_results = {
            "repo_mapper": {
                "architecture_type": "microservices",
                "summary_paragraph": "Test"
            },
            "dependency_analyst": {
                "coupling_scores": {},
                "circular_dependencies": [["a.py", "b.py"]],
                "hub_files": [{"file": "config.py"}]
            },
            "risk_detector": {
                "overall_repo_health": {
                    "score": 75,
                    "grade": "B",
                    "summary": "Good health"
                }
            }
        }
        
        routing_decision = {
            "intent": "Full analysis",
            "agents_to_invoke": ["repo_mapper", "dependency_analyst", "risk_detector"],
            "reasoning": "Test",
            "is_multi_intent": True
        }
        
        aggregated = supervisor_agent.aggregate_results(agent_results, routing_decision)
        
        assert len(aggregated["agents_invoked"]) == 3
        assert "Architecture: microservices" in aggregated["summary"]
        assert "1 hub files, 1 circular dependencies" in aggregated["summary"]
        assert "Health: Grade B" in aggregated["summary"]
    
    def test_aggregate_results_with_errors(self, supervisor_agent):
        """Test aggregation handles agent errors"""
        agent_results = {
            "repo_mapper": {
                "error": "Test error",
                "status": "failed"
            },
            "dependency_analyst": {
                "coupling_scores": {},
                "hub_files": []
            }
        }
        
        routing_decision = {
            "intent": "Test",
            "agents_to_invoke": ["repo_mapper", "dependency_analyst"],
            "reasoning": "Test",
            "is_multi_intent": True
        }
        
        aggregated = supervisor_agent.aggregate_results(agent_results, routing_decision)
        
        # Should still aggregate successfully
        assert "summary" in aggregated
        assert len(aggregated["agents_invoked"]) == 2
    
    @patch.object(SupervisorAgent, 'route_query')
    @patch.object(SupervisorAgent, 'execute_workflow')
    @patch.object(SupervisorAgent, 'aggregate_results')
    def test_process_full_workflow(
        self,
        mock_aggregate,
        mock_execute,
        mock_route,
        supervisor_agent
    ):
        """Test full process workflow"""
        mock_route.return_value = {
            "intent": "Test",
            "agents_to_invoke": ["repo_mapper"],
            "reasoning": "Test",
            "is_multi_intent": False
        }
        mock_execute.return_value = {"repo_mapper": {"test": "result"}}
        mock_aggregate.return_value = {
            "intent": "Test",
            "agents_invoked": ["repo_mapper"],
            "results": {"repo_mapper": {"test": "result"}},
            "summary": "Test summary",
            "is_multi_intent": False
        }
        
        result = supervisor_agent.process(
            user_query="Test query",
            manifest={"files": []}
        )
        
        assert mock_route.called
        assert mock_execute.called
        assert mock_aggregate.called
        assert "intent" in result
        assert "summary" in result
    
    def test_process_missing_query(self, supervisor_agent):
        """Test process raises error without query"""
        with pytest.raises(ValueError, match="user_query"):
            supervisor_agent.process()
    
    def test_invoke_repo_mapper_with_cache(self, supervisor_agent):
        """Test repo_mapper uses cache when available"""
        cached_result = {"architecture_type": "cached"}
        supervisor_agent.context_cache["repo_mapper_result"] = cached_result
        
        result = supervisor_agent._invoke_repo_mapper({})
        
        assert result == cached_result
    
    def test_invoke_dependency_analyst_with_cache(self, supervisor_agent):
        """Test dependency_analyst uses cache when available"""
        cached_result = {"coupling_scores": {"cached": 1.0}}
        supervisor_agent.context_cache["dependency_analyst_result"] = cached_result
        
        result = supervisor_agent._invoke_dependency_analyst({})
        
        assert result == cached_result
    
    def test_invoke_risk_detector_with_cache(self, supervisor_agent):
        """Test risk_detector uses cache when available"""
        cached_result = {"risk_scores": {"cached": {"score": 0.5}}}
        supervisor_agent.context_cache["risk_detector_result"] = cached_result
        
        result = supervisor_agent._invoke_risk_detector({}, {})
        
        assert result == cached_result


class TestSupervisorIntegration:
    """Integration tests for supervisor with real agent interactions"""
    
    @pytest.mark.integration
    def test_supervisor_with_mock_agents(self, mock_llm):
        """Test supervisor orchestrates mock agents correctly"""
        # Create supervisor with mock LLM
        supervisor = SupervisorAgent(llm=mock_llm)
        
        # Mock all sub-agent methods
        supervisor.repo_mapper.analyze_repository = Mock(return_value={
            "architecture_type": "monolith",
            "layer_map": {"backend": ["main.py"]},
            "service_boundaries": [],
            "summary_paragraph": "Simple monolithic application"
        })
        
        supervisor.dependency_analyst.analyze_dependencies = Mock(return_value={
            "coupling_scores": {"main.py": 0.5},
            "circular_dependencies": [],
            "orphan_files": [],
            "hub_files": [{"file": "config.py", "imported_by_count": 2}],
            "external_risk": []
        })
        
        supervisor.risk_detector.assess_risk = Mock(return_value={
            "risk_scores": {"main.py": {"score": 0.4, "reasons": [], "category": "low"}},
            "single_points_of_failure": [],
            "dead_code_candidates": [],
            "complexity_hotspots": [],
            "overall_repo_health": {"score": 80, "grade": "B", "summary": "Good"}
        })
        
        # Execute query
        result = supervisor.process(
            user_query="Analyze the architecture and assess risks",
            manifest={"files": []},
            dependency_graph={"main.py": []},
            files_imports={"main.py": {"imports": []}},
            total_files=1,
            complexity_scores={"main.py": 20.0},
            test_coverage={"main.py": 0.8}
        )
        
        # Verify orchestration
        assert "intent" in result
        assert "agents_invoked" in result
        assert "results" in result
        assert "summary" in result
        
        # Verify agents were called
        assert supervisor.repo_mapper.analyze_repository.called
        assert supervisor.dependency_analyst.analyze_dependencies.called
        assert supervisor.risk_detector.assess_risk.called


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob