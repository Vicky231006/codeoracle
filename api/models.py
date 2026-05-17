"""
Pydantic models for API request/response validation.
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator, model_validator
from enum import Enum


class AgentType(str, Enum):
    """Available agent types."""
    REPO_MAPPER = "repo_mapper"
    DEPENDENCY_ANALYST = "dependency_analyst"
    RISK_DETECTOR = "risk_detector"
    KNOWLEDGE_SYNTHESIZER = "knowledge_synthesizer"
    IMPACT_SIMULATOR = "impact_simulator"


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    agents_available: List[str] = Field(..., description="Available agents")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Detailed error information")
    code: Optional[str] = Field(default=None, description="Error code")


class RepositoryAnalysisRequest(BaseModel):
    """Request for full repository analysis."""
    manifest_path: Optional[str] = Field(default=None, description="Path to the repository manifest JSON file")
    manifest: Optional[Dict[str, Any]] = Field(default=None, description="Repository manifest JSON data")
    analysis_depth: Optional[str] = Field(default="standard", description="Analysis depth: quick, standard, or deep")
    
    @validator('analysis_depth')
    def validate_depth(cls, v):
        if v not in ['quick', 'standard', 'deep']:
            raise ValueError('analysis_depth must be quick, standard, or deep')
        return v
    
    @model_validator(mode='after')
    def validate_manifest_or_path(self):
        if not self.manifest and not self.manifest_path:
            raise ValueError('Either manifest or manifest_path must be provided')
        return self


class RepositoryAnalysisResponse(BaseModel):
    """Response from repository analysis."""
    status: str = Field(..., description="Analysis status")
    repository_map: Dict[str, Any] = Field(..., description="Repository structure and components")
    dependencies: Dict[str, Any] = Field(..., description="Dependency analysis results")
    risks: Dict[str, Any] = Field(..., description="Risk assessment results")
    summary: str = Field(..., description="Overall analysis summary")
    execution_time: float = Field(..., description="Analysis execution time in seconds")


class DependencyAnalysisRequest(BaseModel):
    """Request for dependency analysis."""
    manifest_path: Optional[str] = Field(default=None, description="Path to the repository manifest JSON file")
    manifest: Optional[Dict[str, Any]] = Field(default=None, description="Repository manifest JSON data")
    focus_areas: Optional[List[str]] = Field(default=None, description="Specific areas to focus on")


class DependencyAnalysisResponse(BaseModel):
    """Response from dependency analysis."""
    status: str = Field(..., description="Analysis status")
    dependencies: Dict[str, Any] = Field(..., description="Dependency graph and analysis")
    vulnerabilities: List[Dict[str, Any]] = Field(..., description="Identified vulnerabilities")
    recommendations: List[str] = Field(..., description="Recommendations for improvement")
    execution_time: float = Field(..., description="Analysis execution time in seconds")


class RiskAssessmentRequest(BaseModel):
    """Request for risk assessment."""
    manifest_path: Optional[str] = Field(default=None, description="Path to the repository manifest JSON file")
    manifest: Optional[Dict[str, Any]] = Field(default=None, description="Repository manifest JSON data")
    risk_categories: Optional[List[str]] = Field(default=None, description="Specific risk categories to assess")


class RiskAssessmentResponse(BaseModel):
    """Response from risk assessment."""
    status: str = Field(..., description="Assessment status")
    risks: List[Dict[str, Any]] = Field(..., description="Identified risks with severity")
    overall_risk_score: float = Field(..., description="Overall risk score (0-100)")
    critical_issues: List[Dict[str, Any]] = Field(..., description="Critical issues requiring immediate attention")
    recommendations: List[str] = Field(..., description="Risk mitigation recommendations")
    execution_time: float = Field(..., description="Assessment execution time in seconds")


class QueryRequest(BaseModel):
    """Request for natural language query."""
    manifest_path: Optional[str] = Field(default=None, description="Path to the repository manifest JSON file")
    manifest: Optional[Dict[str, Any]] = Field(default=None, description="Repository manifest JSON data")
    query: str = Field(..., description="Natural language question about the codebase")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context for the query")


class QueryResponse(BaseModel):
    """Response from natural language query."""
    status: str = Field(..., description="Query status")
    answer: str = Field(..., description="Answer to the query")
    sources: List[Dict[str, Any]] = Field(..., description="Source files and components referenced")
    confidence: float = Field(..., description="Confidence score (0-1)")
    execution_time: float = Field(..., description="Query execution time in seconds")


class ImpactSimulationRequest(BaseModel):
    """Request for impact simulation."""
    manifest_path: Optional[str] = Field(default=None, description="Path to the repository manifest JSON file")
    manifest: Optional[Dict[str, Any]] = Field(default=None, description="Repository manifest JSON data")
    change_description: str = Field(..., description="Description of the proposed change")
    affected_files: Optional[List[str]] = Field(default=None, description="Files that will be modified")
    change_type: Optional[str] = Field(default="modification", description="Type of change: addition, modification, or deletion")
    
    @validator('change_type')
    def validate_change_type(cls, v):
        if v not in ['addition', 'modification', 'deletion']:
            raise ValueError('change_type must be addition, modification, or deletion')
        return v
    
    @validator('manifest')
    def validate_manifest_or_path(cls, v, values):
        if not v and not values.get('manifest_path'):
            raise ValueError('Either manifest or manifest_path must be provided')
        return v


class ImpactSimulationResponse(BaseModel):
    """Response from impact simulation."""
    status: str = Field(..., description="Simulation status")
    impact_analysis: Dict[str, Any] = Field(..., description="Detailed impact analysis")
    affected_components: List[Dict[str, Any]] = Field(..., description="Components affected by the change")
    risk_level: str = Field(..., description="Risk level: low, medium, high, or critical")
    recommendations: List[str] = Field(..., description="Recommendations for safe implementation")
    test_suggestions: List[str] = Field(..., description="Suggested tests to validate the change")
    execution_time: float = Field(..., description="Simulation execution time in seconds")


class OrchestrationRequest(BaseModel):
    """Request for supervisor orchestration."""
    manifest_path: Optional[str] = Field(default=None, description="Path to the repository manifest JSON file")
    manifest: Optional[Dict[str, Any]] = Field(default=None, description="Repository manifest JSON data")
    task: str = Field(..., description="High-level task description")
    agents_to_use: Optional[List[AgentType]] = Field(default=None, description="Specific agents to use (if None, supervisor decides)")
    max_iterations: Optional[int] = Field(default=5, description="Maximum number of agent iterations")
    
    @validator('max_iterations')
    def validate_iterations(cls, v):
        if v < 1 or v > 20:
            raise ValueError('max_iterations must be between 1 and 20')
        return v
    
    @validator('manifest')
    def validate_manifest_or_path(cls, v, values):
        if not v and not values.get('manifest_path'):
            raise ValueError('Either manifest or manifest_path must be provided')
        return v


class OrchestrationResponse(BaseModel):
    """Response from supervisor orchestration."""
    status: str = Field(..., description="Orchestration status")
    task_result: Dict[str, Any] = Field(..., description="Final task result")
    agents_used: List[str] = Field(..., description="Agents that were invoked")
    execution_plan: List[Dict[str, Any]] = Field(..., description="Execution plan and steps taken")
    total_execution_time: float = Field(..., description="Total execution time in seconds")
    recommendations: List[str] = Field(..., description="Overall recommendations")


class AgentStatus(BaseModel):
    """Status of an individual agent."""
    name: str = Field(..., description="Agent name")
    type: str = Field(..., description="Agent type")
    status: str = Field(..., description="Current status")
    last_execution: Optional[float] = Field(default=None, description="Last execution timestamp")


class SystemStatusResponse(BaseModel):
    """System status response."""
    status: str = Field(..., description="Overall system status")
    agents: List[AgentStatus] = Field(..., description="Status of all agents")
    cache_size: int = Field(..., description="Current cache size")
    uptime: float = Field(..., description="System uptime in seconds")

# Made with Bob
