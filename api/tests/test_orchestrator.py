"""
Tests for orchestrator service.
"""
import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from api.orchestrator import OrchestratorService, get_orchestrator


@pytest.fixture
def sample_manifest(tmp_path):
    """Create a sample manifest file."""
    manifest = {
        "repository": "test_repo",
        "files": [
            {
                "path": "main.py",
                "type": "python",
                "functions": ["main", "helper"],
                "classes": ["App"],
                "imports": ["os", "sys"]
            },
            {
                "path": "utils.py",
                "type": "python",
                "functions": ["util_func"],
                "classes": [],
                "imports": ["json"]
            }
        ],
        "dependencies": {
            "main.py": ["utils.py"],
            "utils.py": []
        }
    }
    manifest_file = tmp_path / "test_manifest.json"
    manifest_file.write_text(json.dumps(manifest))
    return str(manifest_file)


@pytest.fixture
def mock_agents():
    """Mock all agents."""
    with patch('api.orchestrator.RepoMapperAgent') as repo_mapper, \
         patch('api.orchestrator.DependencyAnalystAgent') as dep_analyst, \
         patch('api.orchestrator.RiskDetectorAgent') as risk_detector, \
         patch('api.orchestrator.KnowledgeSynthesizerAgent') as synthesizer, \
         patch('api.orchestrator.ImpactSimulatorAgent') as simulator, \
         patch('api.orchestrator.SupervisorAgent') as supervisor:
        
        # Mock repo mapper
        repo_mapper_instance = Mock()
        repo_mapper_instance.analyze.return_value = {
            'architecture_type': 'monolithic',
            'components': ['main', 'utils'],
            'summary_paragraph': 'Test repository'
        }
        repo_mapper.return_value = repo_mapper_instance
        
        # Mock dependency analyst
        dep_analyst_instance = Mock()
        dep_analyst_instance.analyze.return_value = {
            'dependencies': {'main.py': ['utils.py']},
            'vulnerabilities': [],
            'recommendations': ['Update dependencies'],
            'coupling_scores': {'main.py': 0.5},
            'hub_files': ['main.py']
        }
        dep_analyst.return_value = dep_analyst_instance
        
        # Mock risk detector
        risk_detector_instance = Mock()
        risk_detector_instance.analyze.return_value = {
            'risks': [],
            'overall_risk_score': 25.0,
            'critical_issues': [],
            'recommendations': ['Add tests'],
            'risk_scores': {'main.py': 0.3}
        }
        risk_detector.return_value = risk_detector_instance
        
        # Mock knowledge synthesizer
        synthesizer_instance = Mock()
        synthesizer_instance.query.return_value = 'This is a test repository'
        synthesizer.return_value = synthesizer_instance
        
        # Mock impact simulator
        simulator_instance = Mock()
        simulator_instance.simulate.return_value = {
            'impact_analysis': {'affected_files': 2},
            'affected_components': ['main', 'utils'],
            'risk_level': 'low',
            'recommendations': ['Run tests'],
            'test_suggestions': ['test_main.py']
        }
        simulator.return_value = simulator_instance
        
        # Mock supervisor
        supervisor_instance = Mock()
        supervisor_instance.process.return_value = {
            'intent': 'analyze',
            'agents_invoked': ['repo_mapper', 'risk_detector'],
            'results': {},
            'summary': 'Analysis complete',
            'is_multi_intent': False
        }
        supervisor.return_value = supervisor_instance
        
        yield {
            'repo_mapper': repo_mapper_instance,
            'dep_analyst': dep_analyst_instance,
            'risk_detector': risk_detector_instance,
            'synthesizer': synthesizer_instance,
            'simulator': simulator_instance,
            'supervisor': supervisor_instance
        }


class TestOrchestratorService:
    """Test orchestrator service."""
    
    def test_initialization(self):
        """Test orchestrator initialization."""
        orchestrator = OrchestratorService()
        assert orchestrator.supervisor is None
        assert len(orchestrator.agents) == 0
        assert len(orchestrator.cache) == 0
    
    @pytest.mark.asyncio
    async def test_analyze_repository(self, sample_manifest, mock_agents):
        """Test repository analysis."""
        orchestrator = OrchestratorService()
        result = await orchestrator.analyze_repository(sample_manifest, "standard")
        
        assert result['status'] == 'success'
        assert 'repository_map' in result
        assert 'dependencies' in result
        assert 'risks' in result
        assert 'summary' in result
        assert 'execution_time' in result
        assert result['execution_time'] > 0
    
    @pytest.mark.asyncio
    async def test_analyze_repository_quick(self, sample_manifest, mock_agents):
        """Test quick repository analysis."""
        orchestrator = OrchestratorService()
        result = await orchestrator.analyze_repository(sample_manifest, "quick")
        
        assert result['status'] == 'success'
        assert 'repository_map' in result
        # Quick analysis should not include dependencies and risks
        assert result['dependencies'] == {}
        assert result['risks'] == {}
    
    @pytest.mark.asyncio
    async def test_analyze_repository_deep(self, sample_manifest, mock_agents):
        """Test deep repository analysis."""
        orchestrator = OrchestratorService()
        result = await orchestrator.analyze_repository(sample_manifest, "deep")
        
        assert result['status'] == 'success'
        assert 'repository_map' in result
        assert 'dependencies' in result
        assert 'risks' in result
        assert result['summary'] != ''
    
    @pytest.mark.asyncio
    async def test_analyze_dependencies(self, sample_manifest, mock_agents):
        """Test dependency analysis."""
        orchestrator = OrchestratorService()
        result = await orchestrator.analyze_dependencies(sample_manifest)
        
        assert result['status'] == 'success'
        assert 'dependencies' in result
        assert 'vulnerabilities' in result
        assert 'recommendations' in result
        assert 'execution_time' in result
    
    @pytest.mark.asyncio
    async def test_assess_risks(self, sample_manifest, mock_agents):
        """Test risk assessment."""
        orchestrator = OrchestratorService()
        result = await orchestrator.assess_risks(sample_manifest)
        
        assert result['status'] == 'success'
        assert 'risks' in result
        assert 'overall_risk_score' in result
        assert 'critical_issues' in result
        assert 'recommendations' in result
        assert result['overall_risk_score'] >= 0
        assert result['overall_risk_score'] <= 100
    
    @pytest.mark.asyncio
    async def test_query_codebase(self, sample_manifest, mock_agents):
        """Test codebase query."""
        orchestrator = OrchestratorService()
        result = await orchestrator.query_codebase(
            sample_manifest,
            "What is the main function?"
        )
        
        assert result['status'] == 'success'
        assert 'answer' in result
        assert 'sources' in result
        assert 'confidence' in result
        assert result['confidence'] >= 0
        assert result['confidence'] <= 1
    
    @pytest.mark.asyncio
    async def test_simulate_impact(self, sample_manifest, mock_agents):
        """Test impact simulation."""
        orchestrator = OrchestratorService()
        result = await orchestrator.simulate_impact(
            sample_manifest,
            "Refactor main function",
            ["main.py"],
            "modification"
        )
        
        assert result['status'] == 'success'
        assert 'impact_analysis' in result
        assert 'affected_components' in result
        assert 'risk_level' in result
        assert result['risk_level'] in ['low', 'medium', 'high', 'critical']
    
    @pytest.mark.asyncio
    async def test_orchestrate_task(self, sample_manifest, mock_agents):
        """Test task orchestration."""
        orchestrator = OrchestratorService()
        result = await orchestrator.orchestrate_task(
            sample_manifest,
            "Analyze the repository"
        )
        
        assert result['status'] == 'success'
        assert 'task_result' in result
        assert 'agents_used' in result
        assert 'execution_plan' in result
        assert 'total_execution_time' in result
    
    def test_get_system_status(self, mock_agents):
        """Test system status."""
        orchestrator = OrchestratorService()
        orchestrator._initialize_agents()
        
        status = orchestrator.get_system_status()
        
        assert status['status'] == 'healthy'
        assert 'agents' in status
        assert 'cache_size' in status
        assert 'uptime' in status
        assert status['uptime'] > 0
    
    def test_clear_cache(self):
        """Test cache clearing."""
        orchestrator = OrchestratorService()
        orchestrator.cache['test'] = 'value'
        
        assert len(orchestrator.cache) == 1
        orchestrator.clear_cache()
        assert len(orchestrator.cache) == 0


class TestGetOrchestrator:
    """Test get_orchestrator function."""
    
    def test_get_orchestrator_singleton(self):
        """Test that get_orchestrator returns singleton."""
        orchestrator1 = get_orchestrator()
        orchestrator2 = get_orchestrator()
        
        assert orchestrator1 is orchestrator2


class TestErrorHandling:
    """Test error handling in orchestrator."""
    
    @pytest.mark.asyncio
    async def test_invalid_manifest_path(self):
        """Test with invalid manifest path."""
        orchestrator = OrchestratorService()
        
        with pytest.raises(FileNotFoundError):
            await orchestrator.analyze_repository("/nonexistent/path.json")
    
    @pytest.mark.asyncio
    async def test_agent_initialization_failure(self):
        """Test handling of agent initialization failure."""
        with patch('api.orchestrator.RepoMapperAgent', side_effect=Exception("Init failed")):
            orchestrator = OrchestratorService()
            
            with pytest.raises(Exception):
                orchestrator._initialize_agents()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
