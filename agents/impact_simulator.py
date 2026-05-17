"""
Impact Simulator Agent
Simulates "what if" scenarios for code changes
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent


class ImpactSimulatorAgent(BaseAgent):
    """
    Agent that simulates impact of hypothetical changes:
    - Direct dependencies affected
    - Transitive dependencies (up to 3 hops)
    - Services affected
    - Risk level estimation
    - Mitigation steps
    """
    
    @property
    def agent_name(self) -> str:
        return "impact_simulator"
    
    def process(self, **kwargs) -> Dict[str, Any]:
        """
        Process impact simulation scenario
        
        Args:
            **kwargs: Must contain:
                - user_scenario: Description of hypothetical change
                - dependency_graph: Graph of file dependencies
                - risk_scores: Risk scores per file
                - architecture_summary: Architecture overview
        
        Returns:
            Dict containing:
                - scenario: Paraphrased scenario
                - directly_affected: List of directly affected files
                - transitively_affected: List of transitively affected files
                - services_affected: List of affected services
                - estimated_risk_level: catastrophic|high|medium|low|negligible
                - mitigation_steps: List of mitigation steps
                - confidence: high|medium|low
        """
        user_scenario = kwargs.get('user_scenario')
        dependency_graph = kwargs.get('dependency_graph')
        risk_scores = kwargs.get('risk_scores')
        architecture_summary = kwargs.get('architecture_summary')
        
        if not all([user_scenario, dependency_graph, risk_scores, architecture_summary]):
            raise ValueError("All parameters are required: user_scenario, dependency_graph, risk_scores, architecture_summary")
        
        # Format prompt
        prompt = self._format_prompt(
            user_scenario=user_scenario,
            dependency_graph_json=json.dumps(dependency_graph, indent=2),
            risk_scores_json=json.dumps(risk_scores, indent=2),
            architecture_summary=architecture_summary
        )
        
        # Call LLM
        response = self._call_llm(prompt, temperature=0.2, max_tokens=4096)
        
        return response
    
    def simulate_impact(
        self,
        scenario: str,
        dependency_graph: Dict[str, List[str]],
        risk_scores: Dict[str, Dict[str, Any]],
        architecture_summary: str
    ) -> Dict[str, Any]:
        """
        Convenience method for impact simulation
        
        Args:
            scenario: Description of hypothetical change
            dependency_graph: Graph of file dependencies
            risk_scores: Risk scores per file
            architecture_summary: Architecture overview
        
        Returns:
            Impact simulation with validation
        """
        return self.execute(
            validate_output=True,
            user_scenario=scenario,
            dependency_graph=dependency_graph,
            risk_scores=risk_scores,
            architecture_summary=architecture_summary
        )
    
    def get_affected_files(
        self,
        scenario: str,
        dependency_graph: Dict[str, List[str]],
        risk_scores: Dict[str, Dict[str, Any]],
        architecture_summary: str
    ) -> List[str]:
        """
        Get all affected files (direct + transitive)
        
        Args:
            scenario: Description of hypothetical change
            dependency_graph: Graph of file dependencies
            risk_scores: Risk scores per file
            architecture_summary: Architecture overview
        
        Returns:
            List of all affected file paths
        """
        result = self.simulate_impact(
            scenario,
            dependency_graph,
            risk_scores,
            architecture_summary
        )
        
        directly = [item["file"] for item in result.get("directly_affected", [])]
        transitively = [item["file"] for item in result.get("transitively_affected", [])]
        
        return list(set(directly + transitively))
    
    def get_risk_level(
        self,
        scenario: str,
        dependency_graph: Dict[str, List[str]],
        risk_scores: Dict[str, Dict[str, Any]],
        architecture_summary: str
    ) -> str:
        """
        Get estimated risk level for the scenario
        
        Args:
            scenario: Description of hypothetical change
            dependency_graph: Graph of file dependencies
            risk_scores: Risk scores per file
            architecture_summary: Architecture overview
        
        Returns:
            Risk level: catastrophic|high|medium|low|negligible
        """
        result = self.simulate_impact(
            scenario,
            dependency_graph,
            risk_scores,
            architecture_summary
        )
        return result.get("estimated_risk_level", "unknown")
    
    def get_mitigation_steps(
        self,
        scenario: str,
        dependency_graph: Dict[str, List[str]],
        risk_scores: Dict[str, Dict[str, Any]],
        architecture_summary: str
    ) -> List[str]:
        """
        Get mitigation steps for the scenario
        
        Args:
            scenario: Description of hypothetical change
            dependency_graph: Graph of file dependencies
            risk_scores: Risk scores per file
            architecture_summary: Architecture overview
        
        Returns:
            List of mitigation step strings
        """
        result = self.simulate_impact(
            scenario,
            dependency_graph,
            risk_scores,
            architecture_summary
        )
        return result.get("mitigation_steps", [])
    
    def is_safe_change(
        self,
        scenario: str,
        dependency_graph: Dict[str, List[str]],
        risk_scores: Dict[str, Dict[str, Any]],
        architecture_summary: str
    ) -> bool:
        """
        Check if the change is relatively safe (low or negligible risk)
        
        Args:
            scenario: Description of hypothetical change
            dependency_graph: Graph of file dependencies
            risk_scores: Risk scores per file
            architecture_summary: Architecture overview
        
        Returns:
            True if risk level is low or negligible
        """
        risk_level = self.get_risk_level(
            scenario,
            dependency_graph,
            risk_scores,
            architecture_summary
        )
        return risk_level in ["low", "negligible"]


def create_impact_simulator() -> ImpactSimulatorAgent:
    """Factory function to create ImpactSimulatorAgent"""
    return ImpactSimulatorAgent()


# Example usage
if __name__ == "__main__":
    # Test with sample data
    sample_scenario = "What if I delete the config.py file?"
    sample_graph = {
        "main.py": ["utils.py", "config.py"],
        "utils.py": ["config.py"],
        "config.py": [],
        "tests/test_main.py": ["main.py"]
    }
    sample_risks = {
        "main.py": {"score": 0.6, "reasons": ["Medium coupling"], "category": "medium"},
        "config.py": {"score": 0.85, "reasons": ["High coupling", "Hub file"], "category": "critical"}
    }
    sample_arch = "This is a monolithic Python application with clear separation of concerns."
    
    agent = create_impact_simulator()
    print(f"Testing {agent.agent_name} agent...")
    
    try:
        result = agent.simulate_impact(
            sample_scenario,
            sample_graph,
            sample_risks,
            sample_arch
        )
        print("\n✅ Analysis complete!")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

# Made with Bob
