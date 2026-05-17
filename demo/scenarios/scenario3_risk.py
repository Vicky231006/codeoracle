#!/usr/bin/env python3
"""
Scenario 3: Risk Assessment

This scenario demonstrates the RiskDetector agent identifying security vulnerabilities,
code quality issues, and technical debt in the repository.
"""

import sys
import json
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.supervisor import AgentSupervisor


def run_scenario(manifest_path: str):
    """
    Run risk assessment scenario
    
    Args:
        manifest_path: Path to repository manifest JSON file
    """
    print("=" * 80)
    print("SCENARIO 3: Risk Assessment")
    print("=" * 80)
    print()
    
    # Load manifest
    print(f"Loading manifest from: {manifest_path}")
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    
    print(f"Repository: {manifest.get('repository', {}).get('name', 'Unknown')}")
    print(f"Files: {len(manifest.get('files', []))}")
    print()
    
    # Run RiskDetector
    print("Running RiskDetector agent...")
    print("-" * 80)
    
    supervisor = AgentSupervisor()
    result = supervisor.run_agent('risk_detector', manifest)
    
    # Display results
    if result.get('status') == 'success':
        print("\n✓ Analysis Complete!")
        print()
        
        analysis = result.get('result', {})
        
        # Overall risk score
        risk_score = analysis.get('overall_risk_score', 0)
        risk_level = analysis.get('risk_level', 'Unknown')
        
        print(f"OVERALL RISK ASSESSMENT:")
        print("-" * 80)
        print(f"Risk Score: {risk_score}/100")
        print(f"Risk Level: {risk_level}")
        print()
        
        # Risks by severity
        risks = analysis.get('risks', [])
        severity_counts = {}
        for risk in risks:
            severity = risk.get('severity', 'unknown')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        print(f"RISKS IDENTIFIED ({len(risks)}):")
        print("-" * 80)
        for severity in ['critical', 'high', 'medium', 'low']:
            count = severity_counts.get(severity, 0)
            if count > 0:
                print(f"• {severity.upper()}: {count}")
        print()
        
        # Critical and high risks
        critical_high = [r for r in risks if r.get('severity') in ['critical', 'high']]
        if critical_high:
            print(f"CRITICAL & HIGH SEVERITY RISKS:")
            print("-" * 80)
            for risk in critical_high[:5]:  # Show first 5
                print(f"• [{risk.get('severity', 'unknown').upper()}] {risk.get('title', 'Unknown')}")
                print(f"  Category: {risk.get('category', 'Unknown')}")
                print(f"  File: {risk.get('file', 'Unknown')}")
                if risk.get('line_number'):
                    print(f"  Line: {risk.get('line_number')}")
                print(f"  Description: {risk.get('description', 'N/A')}")
                if risk.get('recommendation'):
                    print(f"  Recommendation: {risk.get('recommendation')}")
                print()
            
            if len(critical_high) > 5:
                print(f"... and {len(critical_high) - 5} more critical/high risks")
                print()
        
        # Security vulnerabilities
        security_risks = [r for r in risks if r.get('category') == 'security']
        if security_risks:
            print(f"⚠ SECURITY VULNERABILITIES ({len(security_risks)}):")
            print("-" * 80)
            for risk in security_risks[:3]:
                print(f"• {risk.get('title', 'Unknown')}")
                print(f"  Severity: {risk.get('severity', 'Unknown')}")
                print(f"  File: {risk.get('file', 'Unknown')}")
                print()
        
        # Code quality issues
        quality_risks = [r for r in risks if r.get('category') == 'code_quality']
        if quality_risks:
            print(f"CODE QUALITY ISSUES ({len(quality_risks)}):")
            print("-" * 80)
            for risk in quality_risks[:3]:
                print(f"• {risk.get('title', 'Unknown')}")
                print(f"  File: {risk.get('file', 'Unknown')}")
                print()
        
        # Technical debt
        debt_risks = [r for r in risks if r.get('category') == 'technical_debt']
        if debt_risks:
            print(f"TECHNICAL DEBT ({len(debt_risks)}):")
            print("-" * 80)
            for risk in debt_risks[:3]:
                print(f"• {risk.get('title', 'Unknown')}")
                print(f"  File: {risk.get('file', 'Unknown')}")
                print()
        
        # Risk metrics
        metrics = analysis.get('metrics', {})
        if metrics:
            print(f"RISK METRICS:")
            print("-" * 80)
            print(f"Files with risks: {metrics.get('files_with_risks', 0)}")
            print(f"Average risks per file: {metrics.get('avg_risks_per_file', 0):.2f}")
            print(f"Most risky files: {', '.join(metrics.get('most_risky_files', [])[:3])}")
            print()
        
        # Recommendations
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            print(f"TOP RECOMMENDATIONS:")
            print("-" * 80)
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"{i}. {rec}")
            print()
        
        # Insights
        insights = analysis.get('insights', [])
        if insights:
            print(f"KEY INSIGHTS:")
            print("-" * 80)
            for insight in insights:
                print(f"• {insight}")
            print()
        
        return True
    else:
        print(f"\n✗ Analysis Failed: {result.get('error', 'Unknown error')}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Run risk assessment scenario')
    parser.add_argument(
        'manifest_path',
        help='Path to repository manifest JSON file'
    )
    
    args = parser.parse_args()
    
    success = run_scenario(args.manifest_path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

# Made with Bob
