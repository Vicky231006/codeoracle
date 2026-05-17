"""
Supervisor Agent
Orchestrates all other agents based on user queries
"""

import json
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from .repo_mapper import RepoMapperAgent
from .dependency_analyst import DependencyAnalystAgent
from .risk_detector import RiskDetectorAgent
from .knowledge_synthesizer import KnowledgeSynthesizerAgent
from .impact_simulator import ImpactSimulatorAgent


class SupervisorAgent(BaseAgent):
    """
    Agent that orchestrates other agents:
    - Analyzes user queries to determine intent
    - Routes queries to appropriate agents
    - Handles multi-intent queries
    - Aggregates results from multiple agents
    - Manages context caching
    """
    
    def __init__(self, llm=None):
        """Initialize supervisor with all sub-agents"""
        super().__init__(llm)
        
        # Initialize all sub-agents
        self.repo_mapper = RepoMapperAgent(llm)
        self.dependency_analyst = DependencyAnalystAgent(llm)
        self.risk_detector = RiskDetectorAgent(llm)
        self.knowledge_synthesizer = KnowledgeSynthesizerAgent(llm)
        self.impact_simulator = ImpactSimulatorAgent(llm)
        
        # Context cache for agent results
        self.context_cache: Dict[str, Any] = {}
    
    @property
    def agent_name(self) -> str:
        return "supervisor"
    
    def process(self, **kwargs) -> Dict[str, Any]:
        """
        Process user query and orchestrate agents
        
        Args:
            **kwargs: Must contain:
                - user_query: The user's question or request
                - manifest: Repository manifest (optional if cached)
                - dependency_graph: Dependency graph (optional if cached)
                - files_imports: Import information (optional if cached)
                - total_files: Total file count (optional if cached)
                - complexity_scores: Complexity metrics (optional if cached)
                - test_coverage: Test coverage data (optional if cached)
                - relevant_files_content: File contents for Q&A (optional)
        
        Returns:
            Dict containing:
                - intent: Detected intent
                - agents_invoked: List of agents that were called
                - results: Dict mapping agent names to their results
                - summary: High-level summary of findings
        """
        user_query = kwargs.get('user_query')
        if not user_query:
            raise ValueError("'user_query' parameter is required")
        
        # Get available context
        available_context = self._get_available_context(kwargs)
        
        # Route query to determine which agents to invoke
        routing_decision = self.route_query(user_query, available_context)
        
        # Execute workflow
        results = self.execute_workflow(user_query, routing_decision, kwargs)
        
        # Aggregate results
        aggregated = self.aggregate_results(results, routing_decision)
        
        return aggregated
    
    def route_query(self, query: str, available_context: Dict[str, bool]) -> Dict[str, Any]:
        """
        Determine which agents to invoke based on query
        
        Args:
            query: User's query
            available_context: Dict of available context keys
        
        Returns:
            Dict with intent, agents_to_invoke, reasoning, is_multi_intent
        """
        # Format prompt with query and available context
        context_keys = ", ".join([k for k, v in available_context.items() if v])
        
        prompt = self._format_prompt(
            user_query=query,
            available_context_keys=context_keys if context_keys else "None"
        )
        
        # Call LLM to determine routing
        response = self._call_llm(prompt, temperature=0.1, max_tokens=1024)
        
        return response
    
    def execute_workflow(
        self,
        query: str,
        routing_decision: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute agents in sequence based on routing decision
        
        Args:
            query: User's query
            routing_decision: Routing decision from route_query
            context: Available context data
        
        Returns:
            Dict mapping agent names to their results
        """
        agents_to_invoke = routing_decision.get('agents_to_invoke', [])
        results = {}
        
        for agent_name in agents_to_invoke:
            try:
                if agent_name == "repo_mapper":
                    result = self._invoke_repo_mapper(context)
                    results[agent_name] = result
                    # Cache result
                    self.context_cache['repo_mapper_result'] = result
                    
                elif agent_name == "dependency_analyst":
                    result = self._invoke_dependency_analyst(context)
                    results[agent_name] = result
                    # Cache result
                    self.context_cache['dependency_analyst_result'] = result
                    
                elif agent_name == "risk_detector":
                    result = self._invoke_risk_detector(context, results)
                    results[agent_name] = result
                    # Cache result
                    self.context_cache['risk_detector_result'] = result
                    
                elif agent_name == "knowledge_synthesizer":
                    result = self._invoke_knowledge_synthesizer(query, context, results)
                    results[agent_name] = result
                    
                elif agent_name == "impact_simulator":
                    result = self._invoke_impact_simulator(query, context, results)
                    results[agent_name] = result
                    
            except Exception as e:
                results[agent_name] = {
                    "error": str(e),
                    "status": "failed"
                }
        
        return results
    
    def aggregate_results(
        self,
        agent_results: Dict[str, Any],
        routing_decision: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Aggregate results from multiple agents into cohesive response
        
        Args:
            agent_results: Results from each agent
            routing_decision: Original routing decision
        
        Returns:
            Aggregated response with summary
        """
        # Build summary based on which agents were invoked
        summary_parts = []
        
        if "repo_mapper" in agent_results:
            rm_result = agent_results["repo_mapper"]
            if "error" not in rm_result:
                summary_parts.append(f"Architecture: {rm_result.get('architecture_type', 'unknown')}")
        
        if "dependency_analyst" in agent_results:
            da_result = agent_results["dependency_analyst"]
            if "error" not in da_result:
                circular = len(da_result.get('circular_dependencies', []))
                hubs = len(da_result.get('hub_files', []))
                summary_parts.append(f"Dependencies: {hubs} hub files, {circular} circular dependencies")
        
        if "risk_detector" in agent_results:
            rd_result = agent_results["risk_detector"]
            if "error" not in rd_result:
                health = rd_result.get('overall_repo_health', {})
                grade = health.get('grade', 'N/A')
                summary_parts.append(f"Health: Grade {grade}")
        
        if "knowledge_synthesizer" in agent_results:
            ks_result = agent_results["knowledge_synthesizer"]
            if "error" not in ks_result:
                confidence = ks_result.get('confidence', 'unknown')
                summary_parts.append(f"Answer confidence: {confidence}")
        
        if "impact_simulator" in agent_results:
            is_result = agent_results["impact_simulator"]
            if "error" not in is_result:
                risk_level = is_result.get('estimated_risk_level', 'unknown')
                summary_parts.append(f"Impact risk: {risk_level}")
        
        summary = " | ".join(summary_parts) if summary_parts else "Analysis complete"
        
        return {
            "intent": routing_decision.get('intent', ''),
            "agents_invoked": list(agent_results.keys()),
            "results": agent_results,
            "summary": summary,
            "is_multi_intent": routing_decision.get('is_multi_intent', False)
        }
    
    def _get_available_context(self, kwargs: Dict[str, Any]) -> Dict[str, bool]:
        """Check what context is available"""
        return {
            "manifest": kwargs.get('manifest') is not None or 'repo_mapper_result' in self.context_cache,
            "dependency_graph": kwargs.get('dependency_graph') is not None or 'dependency_analyst_result' in self.context_cache,
            "risk_assessment": 'risk_detector_result' in self.context_cache,
            "architecture_summary": 'repo_mapper_result' in self.context_cache
        }
    
    def _invoke_repo_mapper(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke repo mapper agent"""
        # Check cache first
        if 'repo_mapper_result' in self.context_cache:
            return self.context_cache['repo_mapper_result']
        
        manifest = context.get('manifest')
        if not manifest:
            raise ValueError("manifest required for repo_mapper")
        
        return self.repo_mapper.analyze_repository(manifest)
    
    def _invoke_dependency_analyst(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke dependency analyst agent"""
        # Check cache first
        if 'dependency_analyst_result' in self.context_cache:
            return self.context_cache['dependency_analyst_result']
        
        dependency_graph = context.get('dependency_graph')
        files_imports = context.get('files_imports')
        total_files = context.get('total_files')
        
        if not all([dependency_graph, files_imports, total_files is not None]):
            raise ValueError("dependency_graph, files_imports, and total_files required for dependency_analyst")
        
        return self.dependency_analyst.analyze_dependencies(
            dependency_graph,
            files_imports,
            total_files
        )
    
    def _invoke_risk_detector(
        self,
        context: Dict[str, Any],
        current_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invoke risk detector agent"""
        # Check cache first
        if 'risk_detector_result' in self.context_cache:
            return self.context_cache['risk_detector_result']
        
        # Get architecture summary from repo_mapper result or cache
        architecture_summary = None
        if 'repo_mapper' in current_results:
            architecture_summary = current_results['repo_mapper'].get('summary_paragraph')
        elif 'repo_mapper_result' in self.context_cache:
            architecture_summary = self.context_cache['repo_mapper_result'].get('summary_paragraph')
        
        # Get coupling scores from dependency_analyst result or cache
        coupling_scores = None
        hub_files = None
        if 'dependency_analyst' in current_results:
            coupling_scores = current_results['dependency_analyst'].get('coupling_scores')
            hub_files = current_results['dependency_analyst'].get('hub_files')
        elif 'dependency_analyst_result' in self.context_cache:
            coupling_scores = self.context_cache['dependency_analyst_result'].get('coupling_scores')
            hub_files = self.context_cache['dependency_analyst_result'].get('hub_files')
        
        complexity_scores = context.get('complexity_scores')
        test_coverage = context.get('test_coverage')
        
        if not all([architecture_summary, coupling_scores, complexity_scores, hub_files, test_coverage]):
            raise ValueError("architecture_summary, coupling_scores, complexity_scores, hub_files, and test_coverage required for risk_detector")
        
        return self.risk_detector.assess_risk(
            architecture_summary,
            coupling_scores,
            complexity_scores,
            hub_files,
            test_coverage
        )
    
    def _invoke_knowledge_synthesizer(
        self,
        query: str,
        context: Dict[str, Any],
        current_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invoke knowledge synthesizer agent"""
        # Get architecture summary
        architecture_summary = None
        if 'repo_mapper' in current_results:
            architecture_summary = current_results['repo_mapper'].get('summary_paragraph')
        elif 'repo_mapper_result' in self.context_cache:
            architecture_summary = self.context_cache['repo_mapper_result'].get('summary_paragraph')
        
        # Get hub files
        hub_files = None
        if 'dependency_analyst' in current_results:
            hub_files = current_results['dependency_analyst'].get('hub_files')
        elif 'dependency_analyst_result' in self.context_cache:
            hub_files = self.context_cache['dependency_analyst_result'].get('hub_files')
        
        # Get risk summary
        risk_summary = "No risk assessment available"
        if 'risk_detector' in current_results:
            health = current_results['risk_detector'].get('overall_repo_health', {})
            risk_summary = health.get('summary', risk_summary)
        elif 'risk_detector_result' in self.context_cache:
            health = self.context_cache['risk_detector_result'].get('overall_repo_health', {})
            risk_summary = health.get('summary', risk_summary)
        
        relevant_files_content = context.get('relevant_files_content', {})
        
        if not all([architecture_summary, hub_files is not None]):
            raise ValueError("architecture_summary and hub_files required for knowledge_synthesizer")
        
        return self.knowledge_synthesizer.answer_question(
            query,
            architecture_summary,
            hub_files,
            risk_summary,
            relevant_files_content
        )
    
    def _invoke_impact_simulator(
        self,
        query: str,
        context: Dict[str, Any],
        current_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invoke impact simulator agent"""
        dependency_graph = context.get('dependency_graph')
        
        # Get risk scores
        risk_scores = None
        if 'risk_detector' in current_results:
            risk_scores = current_results['risk_detector'].get('risk_scores')
        elif 'risk_detector_result' in self.context_cache:
            risk_scores = self.context_cache['risk_detector_result'].get('risk_scores')
        
        # Get architecture summary
        architecture_summary = None
        if 'repo_mapper' in current_results:
            architecture_summary = current_results['repo_mapper'].get('summary_paragraph')
        elif 'repo_mapper_result' in self.context_cache:
            architecture_summary = self.context_cache['repo_mapper_result'].get('summary_paragraph')
        
        if not all([dependency_graph, risk_scores, architecture_summary]):
            raise ValueError("dependency_graph, risk_scores, and architecture_summary required for impact_simulator")
        
        return self.impact_simulator.simulate_impact(
            query,
            dependency_graph,
            risk_scores,
            architecture_summary
        )
    
    def clear_cache(self):
        """Clear the context cache"""
        self.context_cache.clear()
    
    def get_cached_context(self) -> Dict[str, Any]:
        """Get current cached context"""
        return self.context_cache.copy()


def create_supervisor() -> SupervisorAgent:
    """Factory function to create SupervisorAgent"""
    return SupervisorAgent()


# Example usage
if __name__ == "__main__":
    # Test with sample query
    sample_query = "What is the architecture of this repository and what are the risks?"
    
    agent = create_supervisor()
    print(f"Testing {agent.agent_name} agent...")
    print(f"Query: {sample_query}")
    
    # This would require actual manifest and other data
    print("\n✅ Supervisor agent created successfully!")
    print(f"Available sub-agents: {len([agent.repo_mapper, agent.dependency_analyst, agent.risk_detector, agent.knowledge_synthesizer, agent.impact_simulator])}")

# Made with Bob