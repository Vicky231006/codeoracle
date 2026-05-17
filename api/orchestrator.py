"""
Orchestration service for managing CodeOracle agents.
"""
import time
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from agents.supervisor import SupervisorAgent
from agents.repo_mapper import RepoMapperAgent
from agents.dependency_analyst import DependencyAnalystAgent
from agents.risk_detector import RiskDetectorAgent
from agents.knowledge_synthesizer import KnowledgeSynthesizerAgent
from agents.impact_simulator import ImpactSimulatorAgent

logger = logging.getLogger(__name__)


class OrchestratorService:
    """
    Service layer for orchestrating CodeOracle agents.
    Manages agent lifecycle, caching, and high-level operations.
    """
    
    def __init__(self):
        """Initialize the orchestrator service."""
        self.supervisor: Optional[SupervisorAgent] = None
        self.agents: Dict[str, Any] = {}
        self.cache: Dict[str, Any] = {}
        self.start_time = time.time()
        logger.info("OrchestratorService initialized")
    
    def _initialize_agents(self):
        """Initialize all agents if not already initialized."""
        if not self.agents:
            try:
                self.agents = {
                    'repo_mapper': RepoMapperAgent(),
                    'dependency_analyst': DependencyAnalystAgent(),
                    'risk_detector': RiskDetectorAgent(),
                    'knowledge_synthesizer': KnowledgeSynthesizerAgent(),
                    'impact_simulator': ImpactSimulatorAgent()
                }
                logger.info("All agents initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize agents: {e}")
                raise
    
    def _initialize_supervisor(self):
        """Initialize supervisor agent if not already initialized."""
        if not self.supervisor:
            try:
                self.supervisor = SupervisorAgent()
                logger.info("Supervisor agent initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize supervisor: {e}")
                raise
    
    async def analyze_repository(
        self,
        manifest_data: Dict[str, Any],
        analysis_depth: str = "standard"
    ) -> Dict[str, Any]:
        """Perform full repository analysis."""
        start_time = time.time()
        logger.info(f"Starting repository analysis")
        
        try:
            self._initialize_agents()
            manifest = manifest_data
            
            results = {
                'status': 'success',
                'repository_map': {},
                'dependencies': {},
                'risks': {},
                'summary': ''
            }
            
            # Repository mapping
            repo_mapper = self.agents['repo_mapper']
            repo_result = repo_mapper.analyze_repository(manifest)
            results['repository_map'] = repo_result
            
            if analysis_depth in ['standard', 'deep']:
                # Dependency analysis
                dep_analyst = self.agents['dependency_analyst']
                dep_graph, files_imports, total_files = self._prepare_dependency_data(manifest)
                dep_result = dep_analyst.analyze_dependencies(dep_graph, files_imports, total_files)
                results['dependencies'] = dep_result
                
                # Risk detection
                risk_detector = self.agents['risk_detector']
                complexity_scores, test_coverage = self._prepare_risk_data(manifest)
                risk_result = risk_detector.assess_risk(
                    architecture_summary=repo_result.get("summary_paragraph", ""),
                    coupling_scores=dep_result.get("coupling_scores", {}),
                    complexity_scores=complexity_scores,
                    hub_files=dep_result.get("hub_files", []),
                    test_coverage=test_coverage
                )
                results['risks'] = risk_result
            
            if analysis_depth == 'deep':
                # Generate comprehensive summary
                synthesizer = self.agents['knowledge_synthesizer']
                query = "Provide a comprehensive analysis summary of this repository"
                relevant_files = self._prepare_synthesizer_data(manifest)
                answer_result = synthesizer.answer_question(
                    question=query,
                    architecture_summary=repo_result.get("summary_paragraph", ""),
                    hub_files=dep_result.get("hub_files", []),
                    risk_summary=risk_result.get("overall_repo_health", {}).get("summary", ""),
                    relevant_files_content=relevant_files
                )
                results['summary'] = answer_result.get("answer", "")
            else:
                results['summary'] = "Repository analysis completed successfully"
            
            execution_time = time.time() - start_time
            results['execution_time'] = execution_time
            
            logger.info(f"Repository analysis completed in {execution_time:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Repository analysis failed: {e}")
            raise
    
    async def analyze_dependencies(
        self,
        manifest_data: Dict[str, Any],
        focus_areas: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Perform dependency analysis."""
        start_time = time.time()
        logger.info(f"Starting dependency analysis")
        
        try:
            self._initialize_agents()
            manifest = manifest_data
            
            dep_analyst = self.agents['dependency_analyst']
            dep_graph, files_imports, total_files = self._prepare_dependency_data(manifest)
            analysis = dep_analyst.analyze_dependencies(dep_graph, files_imports, total_files)
            
            results = {
                'status': 'success',
                'dependencies': analysis,
                'vulnerabilities': analysis.get('vulnerabilities', []),
                'recommendations': analysis.get('recommendations', []),
                'execution_time': time.time() - start_time
            }
            
            logger.info(f"Dependency analysis completed in {results['execution_time']:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Dependency analysis failed: {e}")
            raise
    
    async def assess_risks(
        self,
        manifest_data: Dict[str, Any],
        risk_categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Perform risk assessment."""
        start_time = time.time()
        logger.info(f"Starting risk assessment")
        
        try:
            self._initialize_agents()
            manifest = manifest_data
            
            repo_mapper = self.agents['repo_mapper']
            repo_result = repo_mapper.analyze_repository(manifest)
            
            dep_analyst = self.agents['dependency_analyst']
            dep_graph, files_imports, total_files = self._prepare_dependency_data(manifest)
            dep_result = dep_analyst.analyze_dependencies(dep_graph, files_imports, total_files)
            
            risk_detector = self.agents['risk_detector']
            complexity_scores, test_coverage = self._prepare_risk_data(manifest)
            assessment = risk_detector.assess_risk(
                architecture_summary=repo_result.get("summary_paragraph", ""),
                coupling_scores=dep_result.get("coupling_scores", {}),
                complexity_scores=complexity_scores,
                hub_files=dep_result.get("hub_files", []),
                test_coverage=test_coverage
            )
            
            results = {
                'status': 'success',
                'risks': assessment.get('risks', []),
                'overall_risk_score': assessment.get('overall_risk_score', 0),
                'critical_issues': assessment.get('critical_issues', []),
                'recommendations': assessment.get('recommendations', []),
                'execution_time': time.time() - start_time
            }
            
            logger.info(f"Risk assessment completed in {results['execution_time']:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            raise
    
    async def query_codebase(
        self,
        manifest_data: Dict[str, Any],
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Answer natural language query about codebase."""
        start_time = time.time()
        logger.info(f"Processing query: {query}")
        
        try:
            self._initialize_agents()
            manifest = manifest_data
            
            repo_mapper = self.agents['repo_mapper']
            repo_result = repo_mapper.analyze_repository(manifest)
            
            dep_analyst = self.agents['dependency_analyst']
            dep_graph, files_imports, total_files = self._prepare_dependency_data(manifest)
            dep_result = dep_analyst.analyze_dependencies(dep_graph, files_imports, total_files)
            
            risk_detector = self.agents['risk_detector']
            complexity_scores, test_coverage = self._prepare_risk_data(manifest)
            risk_result = risk_detector.assess_risk(
                architecture_summary=repo_result.get("summary_paragraph", ""),
                coupling_scores=dep_result.get("coupling_scores", {}),
                complexity_scores=complexity_scores,
                hub_files=dep_result.get("hub_files", []),
                test_coverage=test_coverage
            )
            
            synthesizer = self.agents['knowledge_synthesizer']
            relevant_files = self._prepare_synthesizer_data(manifest)
            answer_result = synthesizer.answer_question(
                question=query,
                architecture_summary=repo_result.get("summary_paragraph", "N/A"),
                hub_files=dep_result.get("hub_files", []),
                risk_summary=risk_result.get("overall_repo_health", {}).get("summary", "N/A"),
                relevant_files_content=relevant_files
            )
            
            results = {
                'status': 'success',
                'answer': answer_result.get("answer", ""),
                'sources': [],  
                'confidence': 0.85,  
                'execution_time': time.time() - start_time
            }
            
            logger.info(f"Query processed in {results['execution_time']:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Query processing failed: {e}")
            raise
    
    async def simulate_impact(
        self,
        manifest_data: Dict[str, Any],
        change_description: str,
        affected_files: Optional[List[str]] = None,
        change_type: str = "modification"
    ) -> Dict[str, Any]:
        """Simulate impact of proposed changes."""
        start_time = time.time()
        logger.info(f"Simulating impact: {change_description}")
        
        try:
            self._initialize_agents()
            manifest = manifest_data
            
            repo_mapper = self.agents['repo_mapper']
            repo_result = repo_mapper.analyze_repository(manifest)
            
            dep_analyst = self.agents['dependency_analyst']
            dep_graph_raw, files_imports, total_files = self._prepare_dependency_data(manifest)
            dep_result = dep_analyst.analyze_dependencies(dep_graph_raw, files_imports, total_files)
            
            risk_detector = self.agents['risk_detector']
            complexity_scores, test_coverage = self._prepare_risk_data(manifest)
            risk_result = risk_detector.assess_risk(
                architecture_summary=repo_result.get("summary_paragraph", ""),
                coupling_scores=dep_result.get("coupling_scores", {}),
                complexity_scores=complexity_scores,
                hub_files=dep_result.get("hub_files", []),
                test_coverage=test_coverage
            )
            
            simulator = self.agents['impact_simulator']
            dep_graph = self._prepare_impact_data(manifest)
            simulation = simulator.simulate_impact(
                scenario=change_description,
                dependency_graph=dep_graph,
                risk_scores=risk_result.get("risk_scores", {}),
                architecture_summary=repo_result.get("summary_paragraph", "")
            )
            
            affected_components = []
            for item in simulation.get('directly_affected', []):
                affected_components.append({"name": item.get("file", "unknown"), "impact": item.get("reason", ""), "type": "direct"})
            for item in simulation.get('transitively_affected', []):
                affected_components.append({"name": item.get("file", "unknown"), "impact": item.get("reason", ""), "type": "transitive", "hops": item.get("hops", 1)})
            results = {
                'status': 'success',
                'impact_analysis': simulation,
                'affected_components': affected_components,
                'risk_level': simulation.get('estimated_risk_level', 'medium'),
                'recommendations': simulation.get('mitigation_steps', []),
                'test_suggestions': [],
                'execution_time': time.time() - start_time
            }
            
            logger.info(f"Impact simulation completed in {results['execution_time']:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Impact simulation failed: {e}")
            raise
    
    async def orchestrate_task(
        self,
        manifest_data: Dict[str, Any],
        task: str,
        agents_to_use: Optional[List[str]] = None,
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """Orchestrate complex task using supervisor."""
        start_time = time.time()
        logger.info(f"Orchestrating task: {task}")
        
        try:
            self._initialize_supervisor()
            manifest = manifest_data
            
            result = self.supervisor.process(
                user_query=task,
                manifest=manifest
            )
            
            results = {
                'status': 'success',
                'task_result': result,
                'agents_used': result.get('agents_invoked', []),
                'execution_plan': [{'agent': agent, 'status': 'completed'} for agent in result.get('agents_invoked', [])],
                'total_execution_time': time.time() - start_time,
                'recommendations': [result.get('summary', '')]
            }
            
            logger.info(f"Task orchestration completed in {results['total_execution_time']:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Task orchestration failed: {e}")
            raise
    
    def _prepare_dependency_data(self, manifest: Dict[str, Any]) -> tuple:
        raw_graph = manifest.get("dependency_graph", {})
        dependency_graph = {}
        # Convert edges format (source/target) to dict format (file -> [deps])
        for edge in raw_graph.get("edges", []):
            source = edge["source"]
            target = edge["target"]
            if source not in dependency_graph:
                dependency_graph[source] = []
            if target not in dependency_graph[source]:
                dependency_graph[source].append(target)
        for file_info in manifest.get("files", []):
            if file_info["path"] not in dependency_graph:
                dependency_graph[file_info["path"]] = []
        files_imports = {}
        for file_info in manifest.get("files", []):
            file_path = file_info["path"]
            files_imports[file_path] = {
                "imports": file_info.get("imports", []),
                "imported_by": []
            }
        for file_info in manifest.get("files", []):
            file_path = file_info["path"]
            for imported in file_info.get("imports", []):
                for other_file in files_imports:
                    if imported in other_file or other_file.replace(".py", "") in imported:
                        if file_path not in files_imports[other_file]["imported_by"]:
                            files_imports[other_file]["imported_by"].append(file_path)
        total_files = len(manifest.get("files", []))
        return dependency_graph, files_imports, total_files

    def _prepare_risk_data(self, manifest: Dict[str, Any]) -> tuple:
        complexity_scores = {}
        for file_info in manifest.get("files", []):
            score = file_info.get("complexity_score", 0.0)
            if score is None:
                score = 0.0
            complexity_scores[file_info["path"]] = score
        
        test_coverage = {}
        for file_info in manifest.get("files", []):
            file_path = file_info["path"]
            if file_info.get("is_test_file", False):
                test_coverage[file_path] = 1.0
            else:
                test_coverage[file_path] = 0.7
        return complexity_scores, test_coverage

    def _prepare_impact_data(self, manifest: Dict[str, Any]) -> Dict[str, List[str]]:
        dependency_graph = manifest.get("dependency_graph", {})
        dep_graph = {}
        for edge in dependency_graph.get("edges", []):
            source = edge["source"]
            target = edge["target"]
            if source not in dep_graph:
                dep_graph[source] = []
            if target not in dep_graph[source]:
                dep_graph[source].append(target)
        for file_info in manifest.get("files", []):
            if file_info["path"] not in dep_graph:
                dep_graph[file_info["path"]] = []
        return dep_graph

    def _prepare_synthesizer_data(self, manifest: Dict[str, Any]) -> Dict[str, str]:
        relevant_files = {}
        for file_info in manifest.get("files", [])[:5]:
            relevant_files[file_info["path"]] = file_info.get("raw_content", "")
        return relevant_files

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        agent_statuses = []
        for name, agent in self.agents.items():
            agent_statuses.append({
                'name': name,
                'type': agent.__class__.__name__,
                'status': 'active',
                'last_execution': None
            })
        
        return {
            'status': 'healthy',
            'agents': agent_statuses,
            'cache_size': len(self.cache),
            'uptime': time.time() - self.start_time
        }
    
    def clear_cache(self):
        """Clear the orchestrator cache."""
        self.cache.clear()
        logger.info("Cache cleared")


# Global orchestrator instance
_orchestrator: Optional[OrchestratorService] = None


def get_orchestrator() -> OrchestratorService:
    """
    Get or create the global orchestrator instance.
    """
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = OrchestratorService()
    return _orchestrator

# Made with Bob
