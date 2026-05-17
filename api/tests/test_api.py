"""
Tests for FastAPI endpoints.
"""
import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from api.server import app
from api.models import AgentType


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def sample_manifest_path(tmp_path):
    """Create a sample manifest file."""
    manifest = {
        "repository": "test_repo",
        "files": [
            {
                "path": "main.py",
                "type": "python",
                "functions": ["main"],
                "classes": []
            }
        ]
    }
    manifest_file = tmp_path / "test_manifest.json"
    manifest_file.write_text(json.dumps(manifest))
    return str(manifest_file)


@pytest.fixture
def mock_orchestrator():
    """Mock orchestrator for testing."""
    with patch('api.server.get_orchestrator') as mock:
        orchestrator = Mock()
        
        # Mock async methods
        orchestrator.analyze_repository = AsyncMock(return_value={
            'status': 'success',
            'repository_map': {'architecture_type': 'monolithic'},
            'dependencies': {'total': 5},
            'risks': {'overall_risk_score': 30},
            'summary': 'Test analysis complete',
            'execution_time': 1.5
        })
        
        orchestrator.analyze_dependencies = AsyncMock(return_value={
            'status': 'success',
            'dependencies': {'graph': {}},
            'vulnerabilities': [],
            'recommendations': ['Update dependencies'],
            'execution_time': 1.0
        })
        
        orchestrator.assess_risks = AsyncMock(return_value={
            'status': 'success',
            'risks': [],
            'overall_risk_score': 25.0,
            'critical_issues': [],
            'recommendations': ['Add tests'],
            'execution_time': 1.2
        })
        
        orchestrator.query_codebase = AsyncMock(return_value={
            'status': 'success',
            'answer': 'This is a test repository',
            'sources': [],
            'confidence': 0.9,
            'execution_time': 0.8
        })
        
        orchestrator.simulate_impact = AsyncMock(return_value={
            'status': 'success',
            'impact_analysis': {'affected_files': 3},
            'affected_components': [],
            'risk_level': 'low',
            'recommendations': ['Run tests'],
            'test_suggestions': ['test_main.py'],
            'execution_time': 1.1
        })
        
        orchestrator.orchestrate_task = AsyncMock(return_value={
            'status': 'success',
            'task_result': {'completed': True},
            'agents_used': ['repo_mapper'],
            'execution_plan': [],
            'total_execution_time': 2.0,
            'recommendations': ['Task completed']
        })
        
        orchestrator.get_system_status = Mock(return_value={
            'status': 'healthy',
            'agents': [],
            'cache_size': 0,
            'uptime': 100.0
        })
        
        orchestrator.clear_cache = Mock()
        
        mock.return_value = orchestrator
        yield orchestrator


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
    
    def test_health_check(self, client, mock_orchestrator):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert len(data["agents_available"]) > 0
    
    def test_system_status(self, client, mock_orchestrator):
        """Test system status endpoint."""
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "agents" in data
        assert "cache_size" in data
        assert "uptime" in data


class TestAnalysisEndpoints:
    """Test analysis endpoints."""
    
    def test_analyze_repository(self, client, mock_orchestrator, sample_manifest_path):
        """Test repository analysis endpoint."""
        response = client.post(
            "/api/analyze/repository",
            json={
                "manifest_path": sample_manifest_path,
                "analysis_depth": "standard"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "repository_map" in data
        assert "dependencies" in data
        assert "risks" in data
        assert "summary" in data
        assert "execution_time" in data
    
    def test_analyze_repository_invalid_path(self, client, mock_orchestrator):
        """Test repository analysis with invalid path."""
        response = client.post(
            "/api/analyze/repository",
            json={
                "manifest_path": "/nonexistent/path.json",
                "analysis_depth": "standard"
            }
        )
        assert response.status_code == 404
    
    def test_analyze_repository_invalid_depth(self, client, mock_orchestrator, sample_manifest_path):
        """Test repository analysis with invalid depth."""
        response = client.post(
            "/api/analyze/repository",
            json={
                "manifest_path": sample_manifest_path,
                "analysis_depth": "invalid"
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_analyze_dependencies(self, client, mock_orchestrator, sample_manifest_path):
        """Test dependency analysis endpoint."""
        response = client.post(
            "/api/analyze/dependencies",
            json={
                "manifest_path": sample_manifest_path,
                "focus_areas": ["security"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "dependencies" in data
        assert "vulnerabilities" in data
        assert "recommendations" in data
    
    def test_assess_risks(self, client, mock_orchestrator, sample_manifest_path):
        """Test risk assessment endpoint."""
        response = client.post(
            "/api/analyze/risk",
            json={
                "manifest_path": sample_manifest_path,
                "risk_categories": ["security", "maintainability"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "risks" in data
        assert "overall_risk_score" in data
        assert "critical_issues" in data
        assert "recommendations" in data


class TestQueryEndpoint:
    """Test query endpoint."""
    
    def test_query_codebase(self, client, mock_orchestrator, sample_manifest_path):
        """Test natural language query endpoint."""
        response = client.post(
            "/api/query",
            json={
                "manifest_path": sample_manifest_path,
                "query": "What is the main function?",
                "context": {"focus": "main.py"}
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "answer" in data
        assert "sources" in data
        assert "confidence" in data
        assert data["confidence"] >= 0 and data["confidence"] <= 1


class TestSimulationEndpoint:
    """Test impact simulation endpoint."""
    
    def test_simulate_impact(self, client, mock_orchestrator, sample_manifest_path):
        """Test impact simulation endpoint."""
        response = client.post(
            "/api/simulate/impact",
            json={
                "manifest_path": sample_manifest_path,
                "change_description": "Refactor main function",
                "affected_files": ["main.py"],
                "change_type": "modification"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "impact_analysis" in data
        assert "affected_components" in data
        assert "risk_level" in data
        assert data["risk_level"] in ["low", "medium", "high", "critical"]
    
    def test_simulate_impact_invalid_change_type(self, client, mock_orchestrator, sample_manifest_path):
        """Test impact simulation with invalid change type."""
        response = client.post(
            "/api/simulate/impact",
            json={
                "manifest_path": sample_manifest_path,
                "change_description": "Test change",
                "change_type": "invalid"
            }
        )
        assert response.status_code == 422  # Validation error


class TestOrchestrationEndpoint:
    """Test orchestration endpoint."""
    
    def test_orchestrate_task(self, client, mock_orchestrator, sample_manifest_path):
        """Test task orchestration endpoint."""
        response = client.post(
            "/api/orchestrate",
            json={
                "manifest_path": sample_manifest_path,
                "task": "Analyze the repository and identify risks",
                "agents_to_use": ["repo_mapper", "risk_detector"],
                "max_iterations": 3
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "task_result" in data
        assert "agents_used" in data
        assert "execution_plan" in data
        assert "total_execution_time" in data
    
    def test_orchestrate_task_invalid_iterations(self, client, mock_orchestrator, sample_manifest_path):
        """Test orchestration with invalid max_iterations."""
        response = client.post(
            "/api/orchestrate",
            json={
                "manifest_path": sample_manifest_path,
                "task": "Test task",
                "max_iterations": 25  # Too high
            }
        )
        assert response.status_code == 422  # Validation error


class TestCacheEndpoint:
    """Test cache management endpoint."""
    
    def test_clear_cache(self, client, mock_orchestrator):
        """Test cache clearing endpoint."""
        response = client.delete("/api/cache")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "message" in data
        mock_orchestrator.clear_cache.assert_called_once()


class TestErrorHandling:
    """Test error handling."""
    
    def test_missing_manifest_path(self, client, mock_orchestrator):
        """Test request with missing manifest path."""
        response = client.post(
            "/api/analyze/repository",
            json={
                "analysis_depth": "standard"
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_invalid_json(self, client):
        """Test request with invalid JSON."""
        response = client.post(
            "/api/analyze/repository",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
