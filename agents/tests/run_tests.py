"""
Test Runner for CodeOracle Agents
Runs all test suites and generates comprehensive report
"""

import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import test modules
from test_llm_connection import TestLLMConnection
from test_agents import TestAgents
from test_integration import TestIntegration


class TestRunner:
    """Main test runner that orchestrates all test suites"""
    
    def __init__(self):
        self.results = {
            "llm_connection": None,
            "agents": None,
            "integration": None
        }
        self.start_time = None
        self.end_time = None
    
    def print_header(self):
        """Print test suite header"""
        print("\n" + "="*70)
        print(" " * 15 + "CODEORACLE AGENTS TEST SUITE")
        print("="*70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")
    
    def print_section(self, title: str):
        """Print section header"""
        print("\n" + "-"*70)
        print(f"  {title}")
        print("-"*70 + "\n")
    
    def run_llm_connection_tests(self):
        """Run LLM connection tests"""
        self.print_section("1. LLM CONNECTION TESTS")
        
        try:
            tester = TestLLMConnection()
            result = tester.run_all_tests()
            self.results["llm_connection"] = result
            return result["failed"] == 0
        except Exception as e:
            print(f"[X] LLM Connection tests failed with error: {str(e)}")
            self.results["llm_connection"] = {
                "total": 0,
                "passed": 0,
                "failed": 1,
                "error": str(e)
            }
            return False
    
    def run_agent_tests(self):
        """Run individual agent tests"""
        self.print_section("2. INDIVIDUAL AGENT TESTS")
        
        try:
            tester = TestAgents()
            result = tester.run_all_tests()
            self.results["agents"] = result
            return result["failed"] == 0
        except Exception as e:
            print(f"[X] Agent tests failed with error: {str(e)}")
            self.results["agents"] = {
                "total": 0,
                "passed": 0,
                "failed": 1,
                "error": str(e)
            }
            return False
    
    def run_integration_tests(self):
        """Run integration tests"""
        self.print_section("3. INTEGRATION TESTS")
        
        try:
            tester = TestIntegration()
            result = tester.run_all_tests()
            self.results["integration"] = result
            return result["failed"] == 0
        except Exception as e:
            print(f"[X] Integration tests failed with error: {str(e)}")
            self.results["integration"] = {
                "total": 0,
                "passed": 0,
                "failed": 1,
                "error": str(e)
            }
            return False
    
    def generate_summary_report(self):
        """Generate and print summary report"""
        self.print_section("TEST SUMMARY REPORT")
        
        # Calculate totals
        total_tests = 0
        total_passed = 0
        total_failed = 0
        
        for suite_name, result in self.results.items():
            if result:
                total_tests += result.get("total", 0)
                total_passed += result.get("passed", 0)
                total_failed += result.get("failed", 0)
        
        # Print summary table
        print("+" + "-"*68 + "+")
        print("|" + " "*20 + "TEST SUITE RESULTS" + " "*30 + "|")
        print("+" + "-"*30 + "+" + "-"*11 + "+" + "-"*11 + "+" + "-"*13 + "+")
        print("| Suite                        |   Total   |   Passed  |   Failed    |")
        print("+" + "-"*30 + "+" + "-"*11 + "+" + "-"*11 + "+" + "-"*13 + "+")
        
        # LLM Connection
        llm_result = self.results.get("llm_connection") or {}
        status = "[PASS]" if llm_result.get("failed", 1) == 0 else "[FAIL]"
        print(f"| {status} LLM Connection      |    {llm_result.get('total', 0):2d}     |    {llm_result.get('passed', 0):2d}     |     {llm_result.get('failed', 0):2d}      |")
        
        # Individual Agents
        agent_result = self.results.get("agents") or {}
        status = "[PASS]" if agent_result.get("failed", 1) == 0 else "[FAIL]"
        print(f"| {status} Individual Agents   |    {agent_result.get('total', 0):2d}     |    {agent_result.get('passed', 0):2d}     |     {agent_result.get('failed', 0):2d}      |")
        
        # Integration
        int_result = self.results.get("integration") or {}
        status = "[PASS]" if int_result.get("failed", 1) == 0 else "[FAIL]"
        print(f"| {status} Integration         |    {int_result.get('total', 0):2d}     |    {int_result.get('passed', 0):2d}     |     {int_result.get('failed', 0):2d}      |")
        
        print("+" + "-"*30 + "+" + "-"*11 + "+" + "-"*11 + "+" + "-"*13 + "+")
        print(f"| TOTAL                        |    {total_tests:2d}     |    {total_passed:2d}     |     {total_failed:2d}      |")
        print("+" + "-"*30 + "+" + "-"*11 + "+" + "-"*11 + "+" + "-"*13 + "+")
        
        # Calculate success rate
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n[*] Success Rate: {success_rate:.1f}%")
        
        # Execution time
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            print(f"[*] Total Execution Time: {duration:.2f} seconds")
        
        # Overall status
        print("\n" + "="*70)
        if total_failed == 0:
            print("*** ALL TESTS PASSED! ***")
            print("="*70 + "\n")
            return True
        else:
            print(f"[!] {total_failed} TEST(S) FAILED")
            print("="*70 + "\n")
            return False
    
    def save_report_to_file(self):
        """Save detailed report to JSON file"""
        try:
            report_path = Path(__file__).parent / "test_report.json"
            
            report = {
                "timestamp": datetime.now().isoformat(),
                "duration_seconds": self.end_time - self.start_time if self.start_time and self.end_time else 0,
                "results": self.results,
                "summary": {
                    "total_tests": sum(r.get("total", 0) for r in self.results.values() if r),
                    "total_passed": sum(r.get("passed", 0) for r in self.results.values() if r),
                    "total_failed": sum(r.get("failed", 0) for r in self.results.values() if r)
                }
            }
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
            
            print(f"[*] Detailed report saved to: {report_path}")
            return True
        except Exception as e:
            print(f"[!] Could not save report to file: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all test suites"""
        self.start_time = time.time()
        self.print_header()
        
        # Run test suites
        llm_passed = self.run_llm_connection_tests()
        
        # Only continue if LLM tests pass
        if llm_passed:
            agents_passed = self.run_agent_tests()
            integration_passed = self.run_integration_tests()
        else:
            print("\n[!] Skipping remaining tests due to LLM connection failure")
            agents_passed = False
            integration_passed = False
        
        self.end_time = time.time()
        
        # Generate reports
        all_passed = self.generate_summary_report()
        self.save_report_to_file()
        
        return all_passed


def main():
    """Main entry point"""
    runner = TestRunner()
    
    try:
        all_passed = runner.run_all_tests()
        
        # Exit with appropriate code
        sys.exit(0 if all_passed else 1)
    except KeyboardInterrupt:
        print("\n\n[!] Tests interrupted by user")
        sys.exit(2)
    except Exception as e:
        print(f"\n\n[X] Fatal error running tests: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(3)


if __name__ == "__main__":
    main()

# Made with Bob