"""
Dependency Analyst Agent
Analyzes code dependencies and coupling
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent


class DependencyAnalystAgent(BaseAgent):
    """
    Agent that analyzes dependencies to identify:
    - Coupling scores for each file
    - Circular dependency chains
    - Orphaned files
    - Hub files (critical infrastructure)
    - External dependency risks
    """
    
    @property
    def agent_name(self) -> str:
        return "dependency_analyst"
    
    def process(self, **kwargs) -> Dict[str, Any]:
        """
        Process dependency graph and return analysis
        
        Args:
            **kwargs: Must contain:
                - dependency_graph: Dict mapping files to their dependencies
                - files_imports: Dict with import information per file
                - total_files: Total number of files in repository
        
        Returns:
            Dict containing:
                - coupling_scores: Dict[str, float]
                - circular_dependencies: List[List[str]]
                - orphan_files: List[str]
                - hub_files: List[Dict]
                - external_risk: List[Dict]
        """
        dependency_graph = kwargs.get('dependency_graph')
        files_imports = kwargs.get('files_imports')
        total_files = kwargs.get('total_files')
        
        if not dependency_graph or not files_imports or total_files is None:
            raise ValueError("'dependency_graph', 'files_imports', and 'total_files' are required")
        
        # Format prompt
        prompt = self._format_prompt(
            dependency_graph_json=json.dumps(dependency_graph, indent=2),
            files_imports_json=json.dumps(files_imports, indent=2),
            total_files=total_files
        )
        
        # Call LLM
        response = self._call_llm(prompt, temperature=0.1, max_tokens=4096)
        
        return response
    
    def analyze_dependencies(
        self,
        dependency_graph: Dict[str, List[str]],
        files_imports: Dict[str, Any],
        total_files: int
    ) -> Dict[str, Any]:
        """
        Convenience method for dependency analysis
        
        Args:
            dependency_graph: Graph of file dependencies
            files_imports: Import information per file
            total_files: Total number of files
        
        Returns:
            Dependency analysis with validation
        """
        return self.execute(
            validate_output=True,
            dependency_graph=dependency_graph,
            files_imports=files_imports,
            total_files=total_files
        )
    
    def get_coupling_score(
        self,
        file_path: str,
        dependency_graph: Dict[str, List[str]],
        files_imports: Dict[str, Any],
        total_files: int
    ) -> float:
        """
        Get coupling score for a specific file
        
        Args:
            file_path: Path to file
            dependency_graph: Graph of file dependencies
            files_imports: Import information per file
            total_files: Total number of files
        
        Returns:
            Coupling score (0.0 to 1.0)
        """
        result = self.analyze_dependencies(dependency_graph, files_imports, total_files)
        coupling_scores = result.get("coupling_scores", {})
        return coupling_scores.get(file_path, 0.0)
    
    def get_hub_files(
        self,
        dependency_graph: Dict[str, List[str]],
        files_imports: Dict[str, Any],
        total_files: int
    ) -> List[Dict[str, Any]]:
        """
        Get list of hub files (critical infrastructure)
        
        Args:
            dependency_graph: Graph of file dependencies
            files_imports: Import information per file
            total_files: Total number of files
        
        Returns:
            List of hub file information
        """
        result = self.analyze_dependencies(dependency_graph, files_imports, total_files)
        return result.get("hub_files", [])
    
    def has_circular_dependencies(
        self,
        dependency_graph: Dict[str, List[str]],
        files_imports: Dict[str, Any],
        total_files: int
    ) -> bool:
        """
        Check if repository has circular dependencies
        
        Args:
            dependency_graph: Graph of file dependencies
            files_imports: Import information per file
            total_files: Total number of files
        
        Returns:
            True if circular dependencies exist
        """
        result = self.analyze_dependencies(dependency_graph, files_imports, total_files)
        circular = result.get("circular_dependencies", [])
        return len(circular) > 0


def create_dependency_analyst() -> DependencyAnalystAgent:
    """Factory function to create DependencyAnalystAgent"""
    return DependencyAnalystAgent()


# Example usage
if __name__ == "__main__":
    # Test with sample data
    sample_graph = {
        "main.py": ["utils.py", "config.py"],
        "utils.py": ["config.py"],
        "config.py": [],
        "tests/test_main.py": ["main.py"]
    }
    
    sample_imports = {
        "main.py": {"imports": ["utils", "config"], "imported_by": ["tests/test_main.py"]},
        "utils.py": {"imports": ["config"], "imported_by": ["main.py"]},
        "config.py": {"imports": [], "imported_by": ["main.py", "utils.py"]},
        "tests/test_main.py": {"imports": ["main"], "imported_by": []}
    }
    
    agent = create_dependency_analyst()
    print(f"Testing {agent.agent_name} agent...")
    
    try:
        result = agent.analyze_dependencies(sample_graph, sample_imports, 4)
        print("\n✅ Analysis complete!")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

# Made with Bob
