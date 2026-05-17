"""
Startup script for CodeOracle API server.
"""
import sys
import os
from pathlib import Path

# Add the codeoracle directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from api.config import get_settings, validate_config


def main():
    """Start the API server."""
    print("=" * 60)
    print("CodeOracle API Server")
    print("=" * 60)
    
    # Validate configuration
    try:
        validate_config()
        print("[OK] Configuration validated")
    except ValueError as e:
        print(f"[ERROR] Configuration error: {e}")
        print("\nPlease ensure the following environment variables are set:")
        print("  - WATSONX_API_KEY")
        print("  - WATSONX_PROJECT_ID")
        print("\nYou can set them in a .env file in the codeoracle directory.")
        sys.exit(1)
    
    # Get settings
    settings = get_settings()
    
    # Display configuration
    print(f"\nServer Configuration:")
    print(f"  Host: {settings.HOST}")
    print(f"  Port: {settings.PORT}")
    print(f"  Reload: {settings.RELOAD}")
    print(f"  Log Level: {settings.LOG_LEVEL}")
    print(f"\nAPI Documentation:")
    print(f"  Swagger UI: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"  ReDoc: http://{settings.HOST}:{settings.PORT}/redoc")
    print(f"\nAvailable Endpoints:")
    print(f"  POST /api/analyze/repository - Full repository analysis")
    print(f"  POST /api/analyze/dependencies - Dependency analysis")
    print(f"  POST /api/analyze/risk - Risk assessment")
    print(f"  POST /api/query - Natural language Q&A")
    print(f"  POST /api/simulate/impact - Impact simulation")
    print(f"  POST /api/orchestrate - Supervisor orchestration")
    print(f"  GET  /api/health - Health check")
    print(f"  GET  /api/status - System status")
    print("=" * 60)
    print("\nStarting server...\n")
    
    # Start the server
    uvicorn.run(
        "api.server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()

# Made with Bob
