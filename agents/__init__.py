"""
CodeOracle Agents Module
Specialized AI agents for code analysis
"""

from .base_llm import get_llm, BaseLLM, GroqLLM, OllamaLLM, WatsonxLLM
from .base_agent import BaseAgent, AgentError, AgentValidationError, load_agent_config
from .repo_mapper import RepoMapperAgent, create_repo_mapper
from .dependency_analyst import DependencyAnalystAgent, create_dependency_analyst
from .risk_detector import RiskDetectorAgent, create_risk_detector
from .knowledge_synthesizer import KnowledgeSynthesizerAgent, create_knowledge_synthesizer
from .impact_simulator import ImpactSimulatorAgent, create_impact_simulator
from .supervisor import SupervisorAgent, create_supervisor

__all__ = [
    # LLM
    "get_llm",
    "BaseLLM",
    "GroqLLM",
    "OllamaLLM",
    "WatsonxLLM",
    # Base
    "BaseAgent",
    "AgentError",
    "AgentValidationError",
    "load_agent_config",
    # Agents
    "RepoMapperAgent",
    "DependencyAnalystAgent",
    "RiskDetectorAgent",
    "KnowledgeSynthesizerAgent",
    "ImpactSimulatorAgent",
    "SupervisorAgent",
    # Factory functions
    "create_repo_mapper",
    "create_dependency_analyst",
    "create_risk_detector",
    "create_knowledge_synthesizer",
    "create_impact_simulator",
    "create_supervisor",
]

__version__ = "0.1.0"

# Made with Bob
