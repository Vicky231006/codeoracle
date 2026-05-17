"""
Base Agent Class for CodeOracle
Provides common functionality for all specialized agents
"""

import json
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path
from jsonschema import validate, ValidationError

from .base_llm import get_llm, BaseLLM


class BaseAgent(ABC):
    """Abstract base class for all CodeOracle agents"""
    
    def __init__(self, llm: Optional[BaseLLM] = None):
        """
        Initialize agent with LLM
        
        Args:
            llm: LLM instance. If None, uses default from environment
        """
        self.llm = llm or get_llm()
        self.prompt_template = self._load_prompt_template()
        self.output_schema = self._load_output_schema()
    
    @property
    @abstractmethod
    def agent_name(self) -> str:
        """Return the agent's name (e.g., 'repo_mapper')"""
        pass
    
    @abstractmethod
    def process(self, **kwargs) -> Dict[str, Any]:
        """
        Process input and return structured output
        
        Args:
            **kwargs: Agent-specific input parameters
        
        Returns:
            Dict containing agent's analysis results
        """
        pass
    
    def _load_prompt_template(self) -> str:
        """Load prompt template from prompts directory"""
        prompt_path = Path(__file__).parent.parent / "prompts" / f"{self.agent_name}_prompt.txt"
        
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {prompt_path}")
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _load_output_schema(self) -> Dict[str, Any]:
        """Load JSON schema from prompts directory"""
        schema_path = Path(__file__).parent.parent / "prompts" / f"{self.agent_name}_schema.json"
        
        if not schema_path.exists():
            raise FileNotFoundError(f"Output schema not found: {schema_path}")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _format_prompt(self, **kwargs) -> str:
        """
        Format prompt template with provided variables
        
        Args:
            **kwargs: Variables to substitute in template
        
        Returns:
            Formatted prompt string
        """
        prompt = self.prompt_template
        
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            if placeholder in prompt:
                # Convert value to string if it's a dict or list
                if isinstance(value, (dict, list)):
                    value_str = json.dumps(value, indent=2)
                else:
                    value_str = str(value)
                prompt = prompt.replace(placeholder, value_str)
        
        return prompt
    
    def _validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Validate output against JSON schema
        
        Args:
            output: Agent output to validate
        
        Returns:
            True if valid
        
        Raises:
            ValidationError if invalid
        """
        try:
            validate(instance=output, schema=self.output_schema)
            return True
        except ValidationError as e:
            raise ValidationError(f"Output validation failed for {self.agent_name}: {str(e)}")
    
    def _call_llm(self, prompt: str, temperature: float = 0.1, max_tokens: int = 4096) -> Dict[str, Any]:
        """
        Call LLM and return parsed JSON response
        
        Args:
            prompt: Formatted prompt
            temperature: LLM temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
        
        Returns:
            Parsed JSON response
        """
        try:
            response = self.llm.generate_json(prompt, temperature, max_tokens)
            return response
        except Exception as e:
            raise Exception(f"LLM call failed for {self.agent_name}: {str(e)}")
    
    def execute(self, validate_output: bool = True, **kwargs) -> Dict[str, Any]:
        """
        Execute agent with validation
        
        Args:
            validate_output: Whether to validate output against schema
            **kwargs: Agent-specific input parameters
        
        Returns:
            Validated agent output
        """
        # Process input
        output = self.process(**kwargs)
        
        # Validate output if requested
        if validate_output:
            self._validate_output(output)
        
        return output
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(agent_name='{self.agent_name}')"


class AgentError(Exception):
    """Custom exception for agent errors"""
    pass


class AgentValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def load_agent_config() -> Dict[str, Any]:
    """Load agent configuration from environment or config file"""
    return {
        "llm_provider": os.getenv("LLM_PROVIDER", "groq"),
        "temperature": float(os.getenv("AGENT_TEMPERATURE", "0.1")),
        "max_tokens": int(os.getenv("AGENT_MAX_TOKENS", "4096")),
        "validate_output": os.getenv("AGENT_VALIDATE_OUTPUT", "true").lower() == "true"
    }


if __name__ == "__main__":
    # Test base agent functionality
    print("BaseAgent class loaded successfully")
    print(f"Agent config: {json.dumps(load_agent_config(), indent=2)}")

# Made with Bob
