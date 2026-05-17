"""
Risk Detector Agent
Assesses change risk for files in the repository
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent


class RiskDetectorAgent(BaseAgent):
    """
    Agent that assesses change risk using:
    - Coupling scores
    - Complexity scores
    - Critical path analysis
    - Test coverage
    - Overall repository health
    """
    
    @property
    def agent_name(self) -> str:
        return "risk_detector"
    
    def process(self, **kwargs) -> Dict[str, Any]:
        """
        Process risk assessment inputs and return analysis
        
        Args:
            **kwargs: Must contain:
                - architecture_summary: Summary from repo mapper (or summary_paragraph)
                - coupling_scores: Coupling scores from dependency analyst
                - complexity_scores: Complexity metrics per file
                - hub_files: Hub files from dependency analyst
                - test_coverage: Test coverage information
        
        Returns:
            Dict containing:
                - risk_scores: Dict[str, Dict] with score, reasons, category
                - single_points_of_failure: List[Dict]
                - dead_code_candidates: List[str]
                - complexity_hotspots: List[Dict]
                - overall_repo_health: Dict with score, grade, summary
        """
        # Accept both architecture_summary and summary_paragraph for compatibility
        architecture_summary = kwargs.get('architecture_summary') or kwargs.get('summary_paragraph')
        coupling_scores = kwargs.get('coupling_scores')
        complexity_scores = kwargs.get('complexity_scores')
        hub_files = kwargs.get('hub_files')
        test_coverage = kwargs.get('test_coverage')
        
        if not all([architecture_summary, coupling_scores is not None, complexity_scores is not None, hub_files is not None, test_coverage is not None]):
            raise ValueError("All parameters are required: architecture_summary (or summary_paragraph), coupling_scores, complexity_scores, hub_files, test_coverage")
        
        # Format prompt
        prompt = self._format_prompt(
            architecture_summary=architecture_summary,
            coupling_scores_json=json.dumps(coupling_scores, indent=2),
            complexity_scores_json=json.dumps(complexity_scores, indent=2),
            hub_files_json=json.dumps(hub_files, indent=2),
            test_coverage_json=json.dumps(test_coverage, indent=2)
        )
        
        # Call LLM
        response = self._call_llm(prompt, temperature=0.1, max_tokens=4096)
        
        return response
    
    def assess_risk(
        self,
        architecture_summary: str,
        coupling_scores: Dict[str, float],
        complexity_scores: Dict[str, float],
        hub_files: List[Dict[str, Any]],
        test_coverage: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Convenience method for risk assessment
        
        Args:
            architecture_summary: Architecture summary from repo mapper
            coupling_scores: Coupling scores per file
            complexity_scores: Complexity scores per file
            hub_files: List of hub files
            test_coverage: Test coverage data
        
        Returns:
            Risk assessment with validation
        """
        return self.execute(
            validate_output=True,
            architecture_summary=architecture_summary,
            coupling_scores=coupling_scores,
            complexity_scores=complexity_scores,
            hub_files=hub_files,
            test_coverage=test_coverage
        )
    
    def get_file_risk(
        self,
        file_path: str,
        architecture_summary: str,
        coupling_scores: Dict[str, float],
        complexity_scores: Dict[str, float],
        hub_files: List[Dict[str, Any]],
        test_coverage: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get risk assessment for a specific file
        
        Args:
            file_path: Path to file
            architecture_summary: Architecture summary
            coupling_scores: Coupling scores per file
            complexity_scores: Complexity scores per file
            hub_files: List of hub files
            test_coverage: Test coverage data
        
        Returns:
            Risk information for the file (score, reasons, category)
        """
        result = self.assess_risk(
            architecture_summary,
            coupling_scores,
            complexity_scores,
            hub_files,
            test_coverage
        )
        risk_scores = result.get("risk_scores", {})
        return risk_scores.get(file_path, {"score": 0.0, "reasons": [], "category": "low"})
    
    def get_critical_files(
        self,
        architecture_summary: str,
        coupling_scores: Dict[str, float],
        complexity_scores: Dict[str, float],
        hub_files: List[Dict[str, Any]],
        test_coverage: Dict[str, Any]
    ) -> List[str]:
        """
        Get list of critical risk files (score >= 0.75)
        
        Args:
            architecture_summary: Architecture summary
            coupling_scores: Coupling scores per file
            complexity_scores: Complexity scores per file
            hub_files: List of hub files
            test_coverage: Test coverage data
        
        Returns:
            List of file paths with critical risk
        """
        result = self.assess_risk(
            architecture_summary,
            coupling_scores,
            complexity_scores,
            hub_files,
            test_coverage
        )
        risk_scores = result.get("risk_scores", {})
        return [
            file_path
            for file_path, risk_info in risk_scores.items()
            if risk_info.get("category") == "critical"
        ]
    
    def get_repo_health(
        self,
        architecture_summary: str,
        coupling_scores: Dict[str, float],
        complexity_scores: Dict[str, float],
        hub_files: List[Dict[str, Any]],
        test_coverage: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Get overall repository health assessment
        
        Args:
            architecture_summary: Architecture summary
            coupling_scores: Coupling scores per file
            complexity_scores: Complexity scores per file
            hub_files: List of hub files
            test_coverage: Test coverage data
        
        Returns:
            Health information (score, grade, summary)
        """
        result = self.assess_risk(
            architecture_summary,
            coupling_scores,
            complexity_scores,
            hub_files,
            test_coverage
        )
        return result.get("overall_repo_health", {"score": 0, "grade": "F", "summary": ""})


def create_risk_detector() -> RiskDetectorAgent:
    """Factory function to create RiskDetectorAgent"""
    return RiskDetectorAgent()


# Example usage
if __name__ == "__main__":
    # Test with sample data
    sample_arch = "This is a monolithic Python application with clear separation of concerns."
    sample_coupling = {"main.py": 0.75, "utils.py": 0.5, "config.py": 0.8}
    sample_complexity = {"main.py": 45.0, "utils.py": 30.0, "config.py": 15.0}
    sample_hubs = [{"file": "config.py", "imported_by_count": 8, "explanation": "Central config"}]
    sample_coverage = {"main.py": 0.8, "utils.py": 0.6, "config.py": 0.0}
    
    agent = create_risk_detector()
    print(f"Testing {agent.agent_name} agent...")
    
    try:
        result = agent.assess_risk(
            sample_arch,
            sample_coupling,
            sample_complexity,
            sample_hubs,
            sample_coverage
        )
        print("\n✅ Analysis complete!")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

# Made with Bob
