#!/usr/bin/env python3
"""
Scenario 4: Natural Language Q&A

This scenario demonstrates the KnowledgeSynthesizer agent answering questions
about the repository using natural language understanding.
"""

import sys
import json
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.supervisor import AgentSupervisor


def run_scenario(manifest_path: str, custom_questions: list = None):
    """
    Run Q&A scenario
    
    Args:
        manifest_path: Path to repository manifest JSON file
        custom_questions: Optional list of custom questions to ask
    """
    print("=" * 80)
    print("SCENARIO 4: Natural Language Q&A")
    print("=" * 80)
    print()
    
    # Load manifest
    print(f"Loading manifest from: {manifest_path}")
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    print(f"Repository: {manifest.get('repository', {}).get('name', 'Unknown')}")
    print(f"Files: {len(manifest.get('files', []))}")
    print()
    
    # Default questions if none provided
    if not custom_questions:
        custom_questions = [
            "What is the main purpose of this repository?",
            "What are the key components and their responsibilities?",
            "How is the code organized? What is the architecture?",
            "Are there any security concerns in the codebase?",
            "What external dependencies does this project use?",
            "What are the entry points of the application?",
            "Is there any technical debt or code quality issues?",
            "How well is the code documented?",
            "What testing infrastructure exists?",
            "What would be the impact of modifying the main.py file?"
        ]
    
    print(f"Asking {len(custom_questions)} questions...")
    print()
    
    supervisor = AgentSupervisor()
    results = []
    
    for i, question in enumerate(custom_questions, 1):
        print("-" * 80)
        print(f"Question {i}/{len(custom_questions)}:")
        print(f"Q: {question}")
        print()
        
        # Run KnowledgeSynthesizer
        result = supervisor.run_agent('knowledge_synthesizer', manifest, query=question)
        results.append({
            'question': question,
            'result': result
        })
        
        if result.get('status') == 'success':
            answer_data = result.get('result', {})
            answer = answer_data.get('answer', 'No answer provided')
            confidence = answer_data.get('confidence', 0)
            sources = answer_data.get('sources', [])
            
            print(f"A: {answer}")
            print()
            print(f"Confidence: {confidence * 100:.1f}%")
            
            if sources:
                print(f"Sources: {', '.join(sources[:3])}")
                if len(sources) > 3:
                    print(f"         ... and {len(sources) - 3} more")
            print()
        else:
            print(f"✗ Failed to get answer: {result.get('error', 'Unknown error')}")
            print()
    
    # Summary
    print("=" * 80)
    print("Q&A SESSION SUMMARY")
    print("=" * 80)
    
    successful = sum(1 for r in results if r['result'].get('status') == 'success')
    failed = len(results) - successful
    
    print(f"Total questions: {len(results)}")
    print(f"Successful answers: {successful}")
    print(f"Failed answers: {failed}")
    print()
    
    if successful > 0:
        # Calculate average confidence
        confidences = [
            r['result'].get('result', {}).get('confidence', 0)
            for r in results
            if r['result'].get('status') == 'success'
        ]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        print(f"Average confidence: {avg_confidence * 100:.1f}%")
        print()
    
    # Save results
    output_file = Path(manifest_path).parent / "qa_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Full results saved to: {output_file}")
    print()
    
    return failed == 0


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Q&A scenario')
    parser.add_argument(
        'manifest_path',
        help='Path to repository manifest JSON file'
    )
    parser.add_argument(
        '--questions',
        nargs='+',
        help='Custom questions to ask (optional)'
    )
    
    args = parser.parse_args()
    
    success = run_scenario(args.manifest_path, args.questions)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

# Made with Bob
