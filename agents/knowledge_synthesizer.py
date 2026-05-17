"""
Knowledge Synthesizer Agent
Answers natural language questions about the codebase
"""

import json
from typing import Dict, Any, List
from .base_agent import BaseAgent


class KnowledgeSynthesizerAgent(BaseAgent):
    """
    Agent that answers questions about the codebase by synthesizing:
    - Architecture summary
    - Dependency hub files
    - Risk assessment summary
    - Relevant source files
    """
    
    @property
    def agent_name(self) -> str:
        return "knowledge_synthesizer"
    
    def process(self, **kwargs) -> Dict[str, Any]:
        """
        Process question and context to provide answer
        
        Args:
            **kwargs: Must contain:
                - user_question: The question to answer
                - architecture_summary: Architecture overview (or summary_paragraph)
                - hub_files: Critical hub files
                - risk_summary: Risk assessment summary
                - relevant_files_content: Content of relevant source files
        
        Returns:
            Dict containing:
                - answer: Detailed explanation
                - confidence: high|medium|low
                - relevant_files: List of relevant files with reasons
                - follow_up_questions: List of suggested follow-up questions
                - impact_chain: List showing flow/dependencies
        """
        user_question = kwargs.get('user_question')
        # Accept both architecture_summary and summary_paragraph for compatibility
        architecture_summary = kwargs.get('architecture_summary') or kwargs.get('summary_paragraph')
        hub_files = kwargs.get('hub_files')
        risk_summary = kwargs.get('risk_summary')
        relevant_files_content = kwargs.get('relevant_files_content')
        
        if not all([user_question, architecture_summary, hub_files is not None, risk_summary, relevant_files_content is not None]):
            raise ValueError("All parameters are required: user_question, architecture_summary (or summary_paragraph), hub_files, risk_summary, relevant_files_content")
        
        # Format prompt
        prompt = self._format_prompt(
            user_question=user_question,
            architecture_summary=architecture_summary,
            hub_files=json.dumps(hub_files, indent=2),
            risk_summary=risk_summary,
            relevant_files_content=json.dumps(relevant_files_content, indent=2)
        )
        
        # Call LLM
        response = self._call_llm(prompt, temperature=0.2, max_tokens=4096)
        
        return response
    
    def answer_question(
        self,
        question: str,
        architecture_summary: str,
        hub_files: List[Dict[str, Any]],
        risk_summary: str,
        relevant_files_content: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Convenience method for answering questions
        
        Args:
            question: User's question about the codebase
            architecture_summary: Architecture overview
            hub_files: List of critical hub files
            risk_summary: Risk assessment summary
            relevant_files_content: Dict mapping file paths to their content
        
        Returns:
            Answer with validation
        """
        return self.execute(
            validate_output=True,
            user_question=question,
            architecture_summary=architecture_summary,
            hub_files=hub_files,
            risk_summary=risk_summary,
            relevant_files_content=relevant_files_content
        )
    
    def get_answer_text(
        self,
        question: str,
        architecture_summary: str,
        hub_files: List[Dict[str, Any]],
        risk_summary: str,
        relevant_files_content: Dict[str, str]
    ) -> str:
        """
        Get just the answer text
        
        Args:
            question: User's question
            architecture_summary: Architecture overview
            hub_files: List of critical hub files
            risk_summary: Risk assessment summary
            relevant_files_content: Dict mapping file paths to their content
        
        Returns:
            Answer text string
        """
        result = self.answer_question(
            question,
            architecture_summary,
            hub_files,
            risk_summary,
            relevant_files_content
        )
        return result.get("answer", "")
    
    def get_confidence_level(
        self,
        question: str,
        architecture_summary: str,
        hub_files: List[Dict[str, Any]],
        risk_summary: str,
        relevant_files_content: Dict[str, str]
    ) -> str:
        """
        Get confidence level for the answer
        
        Args:
            question: User's question
            architecture_summary: Architecture overview
            hub_files: List of critical hub files
            risk_summary: Risk assessment summary
            relevant_files_content: Dict mapping file paths to their content
        
        Returns:
            Confidence level: "high", "medium", or "low"
        """
        result = self.answer_question(
            question,
            architecture_summary,
            hub_files,
            risk_summary,
            relevant_files_content
        )
        return result.get("confidence", "low")
    
    def get_follow_up_questions(
        self,
        question: str,
        architecture_summary: str,
        hub_files: List[Dict[str, Any]],
        risk_summary: str,
        relevant_files_content: Dict[str, str]
    ) -> List[str]:
        """
        Get suggested follow-up questions
        
        Args:
            question: User's question
            architecture_summary: Architecture overview
            hub_files: List of critical hub files
            risk_summary: Risk assessment summary
            relevant_files_content: Dict mapping file paths to their content
        
        Returns:
            List of follow-up question strings
        """
        result = self.answer_question(
            question,
            architecture_summary,
            hub_files,
            risk_summary,
            relevant_files_content
        )
        return result.get("follow_up_questions", [])
    
    def get_impact_chain(
        self,
        question: str,
        architecture_summary: str,
        hub_files: List[Dict[str, Any]],
        risk_summary: str,
        relevant_files_content: Dict[str, str]
    ) -> List[str]:
        """
        Get impact chain showing file flow/dependencies
        
        Args:
            question: User's question
            architecture_summary: Architecture overview
            hub_files: List of critical hub files
            risk_summary: Risk assessment summary
            relevant_files_content: Dict mapping file paths to their content
        
        Returns:
            List of strings showing impact flow
        """
        result = self.answer_question(
            question,
            architecture_summary,
            hub_files,
            risk_summary,
            relevant_files_content
        )
        return result.get("impact_chain", [])


def create_knowledge_synthesizer() -> KnowledgeSynthesizerAgent:
    """Factory function to create KnowledgeSynthesizerAgent"""
    return KnowledgeSynthesizerAgent()


# Example usage
if __name__ == "__main__":
    # Test with sample data
    sample_question = "How does the main.py file work and what would break if I modify it?"
    sample_arch = "This is a monolithic Python application with clear separation of concerns."
    sample_hubs = [{"file": "config.py", "imported_by_count": 8, "explanation": "Central config"}]
    sample_risk = "The repository has medium risk with config.py being a critical file."
    sample_files = {
        "main.py": "def main():\n    from config import settings\n    print(settings.app_name)",
        "config.py": "class Settings:\n    app_name = 'MyApp'"
    }
    
    agent = create_knowledge_synthesizer()
    print(f"Testing {agent.agent_name} agent...")
    
    try:
        result = agent.answer_question(
            sample_question,
            sample_arch,
            sample_hubs,
            sample_risk,
            sample_files
        )
        print("\n✅ Analysis complete!")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

# Made with Bob
