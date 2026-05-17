"""
Repo Mapper Agent
Analyzes repository structure and classifies architecture
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent


class RepoMapperAgent(BaseAgent):
    """
    Agent that analyzes repository manifest and identifies:
    - Architecture type (monolith, microservices, etc.)
    - Logical layers (frontend, backend, data, config, tests)
    - Service boundaries
    - High-level summary
    """
    
    @property
    def agent_name(self) -> str:
        return "repo_mapper"
    
    def process(self, **kwargs) -> Dict[str, Any]:
        """
        Process repository manifest and return architecture analysis
        
        Args:
            **kwargs: Must contain 'manifest' key with repository manifest
                Expected format: {
                    "files": [
                        {"path": "src/main.py", "language": "python", ...},
                        ...
                    ]
                }
        
        Returns:
            Dict containing:
                - architecture_type: str
                - layer_map: Dict[str, List[str]]
                - service_boundaries: List[Dict]
                - summary_paragraph: str
        """
        manifest = kwargs.get('manifest')
        if not manifest:
            raise ValueError("'manifest' parameter is required")
        
        # Format prompt with manifest
        prompt = self._format_prompt(
            manifest_json=json.dumps(manifest, indent=2)
        )
        
        # Call LLM
        response = self._call_llm(prompt, temperature=0.1, max_tokens=4096)
        
        return response
    
    def analyze_repository(self, manifest: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convenience method for repository analysis
        
        Args:
            manifest: Repository manifest
        
        Returns:
            Architecture analysis with validation
        """
        return self.execute(validate_output=True, manifest=manifest)
    
    def get_architecture_summary(self, manifest: Dict[str, Any]) -> str:
        """
        Get just the summary paragraph
        
        Args:
            manifest: Repository manifest
        
        Returns:
            Summary paragraph string
        """
        result = self.analyze_repository(manifest)
        return result.get("summary_paragraph", "")
    
    def get_layer_files(self, manifest: Dict[str, Any], layer: str) -> List[str]:
        """
        Get files in a specific layer
        
        Args:
            manifest: Repository manifest
            layer: Layer name (frontend, backend, data, config, tests)
        
        Returns:
            List of file paths in that layer
        """
        result = self.analyze_repository(manifest)
        layer_map = result.get("layer_map", {})
        return layer_map.get(layer, [])
    
    def is_microservices(self, manifest: Dict[str, Any]) -> bool:
        """
        Check if repository is microservices architecture
        
        Args:
            manifest: Repository manifest
        
        Returns:
            True if microservices architecture
        """
        result = self.analyze_repository(manifest)
        return result.get("architecture_type") == "microservices"


def create_repo_mapper() -> RepoMapperAgent:
    """Factory function to create RepoMapperAgent"""
    return RepoMapperAgent()


# Example usage
if __name__ == "__main__":
    # Test with sample manifest
    sample_manifest = {
        "files": [
            {"path": "src/main.py", "language": "python", "size": 1024},
            {"path": "src/utils.py", "language": "python", "size": 512},
            {"path": "src/config.py", "language": "python", "size": 256},
            {"path": "tests/test_main.py", "language": "python", "size": 768},
            {"path": "requirements.txt", "language": "text", "size": 128}
        ]
    }
    
    agent = create_repo_mapper()
    print(f"Testing {agent.agent_name} agent...")
    
    try:
        result = agent.analyze_repository(sample_manifest)
        print("\n✅ Analysis complete!")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

# Made with Bob
