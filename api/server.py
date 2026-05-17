"""
FastAPI server for CodeOracle API.
"""
import time
import logging
from typing import Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings, setup_logging, validate_config
from .models import (
    HealthResponse,
    ErrorResponse,
    RepositoryAnalysisRequest,
    RepositoryAnalysisResponse,
    DependencyAnalysisRequest,
    DependencyAnalysisResponse,
    RiskAssessmentRequest,
    RiskAssessmentResponse,
    QueryRequest,
    QueryResponse,
    ImpactSimulationRequest,
    ImpactSimulationResponse,
    OrchestrationRequest,
    OrchestrationResponse,
    SystemStatusResponse,
    AgentStatus
)
from .orchestrator import get_orchestrator

# Setup logging
logger = setup_logging()

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle all unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc),
            code="INTERNAL_ERROR"
        ).dict()
    )


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting CodeOracle API...")
    try:
        validate_config()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down CodeOracle API...")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "CodeOracle API",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }


@app.get(
    "/api/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check endpoint"
)
async def health_check():
    """
    Check API health status.
    
    Returns:
        HealthResponse with status and available agents
    """
    try:
        orchestrator = get_orchestrator()
        return HealthResponse(
            status="healthy",
            version=settings.API_VERSION,
            agents_available=[
                "repo_mapper",
                "dependency_analyst",
                "risk_detector",
                "knowledge_synthesizer",
                "impact_simulator",
                "supervisor"
            ]
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unhealthy: {str(e)}"
        )


@app.get(
    "/api/status",
    response_model=SystemStatusResponse,
    tags=["Health"],
    summary="Get system status"
)
async def system_status():
    """
    Get detailed system status.
    
    Returns:
        SystemStatusResponse with agent statuses and metrics
    """
    try:
        orchestrator = get_orchestrator()
        status_info = orchestrator.get_system_status()
        
        return SystemStatusResponse(
            status=status_info['status'],
            agents=[AgentStatus(**agent) for agent in status_info['agents']],
            cache_size=status_info['cache_size'],
            uptime=status_info['uptime']
        )
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get status: {str(e)}"
        )


@app.post(
    "/api/analyze/repository",
    response_model=RepositoryAnalysisResponse,
    tags=["Analysis"],
    summary="Perform full repository analysis"
)
async def analyze_repository(request: RepositoryAnalysisRequest):
    """
    Analyze a complete repository.
    
    Args:
        request: Repository analysis request with manifest path or manifest JSON
        
    Returns:
        Complete analysis results including structure, dependencies, and risks
    """
    try:
        # Get manifest data - either from path or direct JSON
        manifest_data = None
        if request.manifest:
            manifest_data = request.manifest
        elif request.manifest_path:
            manifest_path = Path(request.manifest_path)
            if not manifest_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Manifest file not found: {request.manifest_path}"
                )
            import json
            with open(manifest_path, 'r') as f:
                manifest_data = json.load(f)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either manifest or manifest_path must be provided"
            )
        
        orchestrator = get_orchestrator()
        result = await orchestrator.analyze_repository(
            manifest_data,
            request.analysis_depth or "standard"
        )
        
        return RepositoryAnalysisResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Repository analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@app.post(
    "/api/analyze/dependencies",
    response_model=DependencyAnalysisResponse,
    tags=["Analysis"],
    summary="Analyze repository dependencies"
)
async def analyze_dependencies(request: DependencyAnalysisRequest):
    """
    Analyze repository dependencies.
    
    Args:
        request: Dependency analysis request
        
    Returns:
        Dependency analysis with vulnerabilities and recommendations
    """
    try:
        # Get manifest data - either from path or direct JSON
        manifest_data = None
        if request.manifest:
            manifest_data = request.manifest
        elif request.manifest_path:
            manifest_path = Path(request.manifest_path)
            if not manifest_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Manifest file not found: {request.manifest_path}"
                )
            import json
            with open(manifest_path, 'r') as f:
                manifest_data = json.load(f)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either manifest or manifest_path must be provided"
            )
        
        orchestrator = get_orchestrator()
        result = await orchestrator.analyze_dependencies(
            manifest_data,
            request.focus_areas
        )
        
        return DependencyAnalysisResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dependency analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@app.post(
    "/api/analyze/risk",
    response_model=RiskAssessmentResponse,
    tags=["Analysis"],
    summary="Assess repository risks"
)
async def assess_risks(request: RiskAssessmentRequest):
    """
    Assess risks in the repository.
    
    Args:
        request: Risk assessment request
        
    Returns:
        Risk assessment with severity scores and recommendations
    """
    try:
        # Get manifest data - either from path or direct JSON
        manifest_data = None
        if request.manifest:
            manifest_data = request.manifest
        elif request.manifest_path:
            manifest_path = Path(request.manifest_path)
            if not manifest_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Manifest file not found: {request.manifest_path}"
                )
            import json
            with open(manifest_path, 'r') as f:
                manifest_data = json.load(f)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either manifest or manifest_path must be provided"
            )
        
        orchestrator = get_orchestrator()
        result = await orchestrator.assess_risks(
            manifest_data,
            request.risk_categories
        )
        
        return RiskAssessmentResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Risk assessment failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assessment failed: {str(e)}"
        )


@app.post(
    "/api/query",
    response_model=QueryResponse,
    tags=["Query"],
    summary="Answer natural language questions"
)
async def query_codebase(request: QueryRequest):
    """
    Answer natural language questions about the codebase.
    
    Args:
        request: Query request with question
        
    Returns:
        Answer with sources and confidence score
    """
    try:
        # Get manifest data - either from path or direct JSON
        manifest_data = None
        if request.manifest:
            manifest_data = request.manifest
        elif request.manifest_path:
            manifest_path = Path(request.manifest_path)
            if not manifest_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Manifest file not found: {request.manifest_path}"
                )
            import json
            with open(manifest_path, 'r') as f:
                manifest_data = json.load(f)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either manifest or manifest_path must be provided"
            )
        
        orchestrator = get_orchestrator()
        result = await orchestrator.query_codebase(
            manifest_data,
            request.query,
            request.context
        )
        
        return QueryResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Query processing failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query failed: {str(e)}"
        )


@app.post(
    "/api/simulate/impact",
    response_model=ImpactSimulationResponse,
    tags=["Simulation"],
    summary="Simulate impact of changes"
)
async def simulate_impact(request: ImpactSimulationRequest):
    """
    Simulate the impact of proposed changes.
    
    Args:
        request: Impact simulation request
        
    Returns:
        Impact analysis with affected components and risk level
    """
    try:
        # Get manifest data - either from path or direct JSON
        manifest_data = None
        if hasattr(request, 'manifest') and request.manifest:
            manifest_data = request.manifest
        elif request.manifest_path:
            manifest_path = Path(request.manifest_path)
            if not manifest_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Manifest file not found: {request.manifest_path}"
                )
            import json
            with open(manifest_path, 'r') as f:
                manifest_data = json.load(f)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either manifest or manifest_path must be provided"
            )
        
        orchestrator = get_orchestrator()
        result = await orchestrator.simulate_impact(
            manifest_data,
            request.change_description,
            request.affected_files,
            request.change_type or "modification"
        )
        
        return ImpactSimulationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Impact simulation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation failed: {str(e)}"
        )


@app.post(
    "/api/orchestrate",
    response_model=OrchestrationResponse,
    tags=["Orchestration"],
    summary="Orchestrate complex tasks"
)
async def orchestrate_task(request: OrchestrationRequest):
    """
    Orchestrate complex tasks using the supervisor agent.
    
    Args:
        request: Orchestration request with task description
        
    Returns:
        Orchestration results with execution plan and recommendations
    """
    try:
        # Get manifest data - either from path or direct JSON
        manifest_data = None
        if hasattr(request, 'manifest') and request.manifest:
            manifest_data = request.manifest
        elif request.manifest_path:
            manifest_path = Path(request.manifest_path)
            if not manifest_path.exists():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Manifest file not found: {request.manifest_path}"
                )
            import json
            with open(manifest_path, 'r') as f:
                manifest_data = json.load(f)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either manifest or manifest_path must be provided"
            )
        
        orchestrator = get_orchestrator()
        result = await orchestrator.orchestrate_task(
            manifest_data,
            request.task,
            [agent.value for agent in request.agents_to_use] if request.agents_to_use else None,
            request.max_iterations or 5
        )
        
        return OrchestrationResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Task orchestration failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Orchestration failed: {str(e)}"
        )


@app.delete(
    "/api/cache",
    tags=["Cache"],
    summary="Clear cache"
)
async def clear_cache():
    """
    Clear the orchestrator cache.
    
    Returns:
        Success message
    """
    try:
        orchestrator = get_orchestrator()
        orchestrator.clear_cache()
        return {"status": "success", "message": "Cache cleared"}
    except Exception as e:
        logger.error(f"Cache clear failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )

# Made with Bob
