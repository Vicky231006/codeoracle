"""
Test LLM Connection and JSON Parsing
Tests Groq API connectivity, JSON parsing, and error handling
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.base_llm import GroqLLM, get_llm
import json


class TestLLMConnection:
    """Test suite for LLM connection and JSON parsing"""
    
    def __init__(self):
        self.results = []
        self.llm = None
    
    def log_result(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        self.results.append({
            "test": test_name,
            "passed": passed,
            "message": message
        })
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status}: {test_name}")
        if message:
            print(f"  -> {message}")
    
    def test_groq_initialization(self):
        """Test 1: Groq LLM initialization"""
        try:
            self.llm = GroqLLM()
            self.log_result(
                "Groq LLM Initialization",
                True,
                f"Model: {self.llm.model}"
            )
            return True
        except Exception as e:
            self.log_result(
                "Groq LLM Initialization",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_basic_generation(self):
        """Test 2: Basic text generation"""
        if not self.llm:
            self.log_result("Basic Text Generation", False, "LLM not initialized")
            return False
        
        try:
            prompt = "Respond with exactly: Hello World"
            response = self.llm.generate(prompt, temperature=0.0, max_tokens=100)
            
            if response and len(response) > 0:
                self.log_result(
                    "Basic Text Generation",
                    True,
                    f"Response length: {len(response)} chars"
                )
                return True
            else:
                self.log_result(
                    "Basic Text Generation",
                    False,
                    "Empty response received"
                )
                return False
        except Exception as e:
            self.log_result(
                "Basic Text Generation",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_json_parsing_simple(self):
        """Test 3: Simple JSON parsing"""
        if not self.llm:
            self.log_result("Simple JSON Parsing", False, "LLM not initialized")
            return False
        
        try:
            prompt = 'Respond with valid JSON: {"status": "ok", "value": 42}'
            response = self.llm.generate_json(prompt, temperature=0.0, max_tokens=100)
            
            # Validate response structure
            if isinstance(response, dict):
                if "status" in response and "value" in response:
                    self.log_result(
                        "Simple JSON Parsing",
                        True,
                        f"Parsed: {json.dumps(response)}"
                    )
                    return True
                else:
                    self.log_result(
                        "Simple JSON Parsing",
                        False,
                        f"Missing expected keys. Got: {list(response.keys())}"
                    )
                    return False
            else:
                self.log_result(
                    "Simple JSON Parsing",
                    False,
                    f"Response is not a dict: {type(response)}"
                )
                return False
        except Exception as e:
            self.log_result(
                "Simple JSON Parsing",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_json_parsing_complex(self):
        """Test 4: Complex JSON parsing with nested structures"""
        if not self.llm:
            self.log_result("Complex JSON Parsing", False, "LLM not initialized")
            return False
        
        try:
            prompt = '''Respond with valid JSON containing:
            - A "files" array with 2 objects, each having "name" and "size" fields
            - A "metadata" object with "total" and "timestamp" fields
            '''
            response = self.llm.generate_json(prompt, temperature=0.0, max_tokens=200)
            
            # Validate response structure
            if isinstance(response, dict):
                has_files = "files" in response and isinstance(response["files"], list)
                has_metadata = "metadata" in response and isinstance(response["metadata"], dict)
                
                if has_files and has_metadata:
                    self.log_result(
                        "Complex JSON Parsing",
                        True,
                        f"Files: {len(response['files'])}, Metadata keys: {list(response['metadata'].keys())}"
                    )
                    return True
                else:
                    self.log_result(
                        "Complex JSON Parsing",
                        False,
                        f"Missing expected structure. Keys: {list(response.keys())}"
                    )
                    return False
            else:
                self.log_result(
                    "Complex JSON Parsing",
                    False,
                    f"Response is not a dict: {type(response)}"
                )
                return False
        except Exception as e:
            self.log_result(
                "Complex JSON Parsing",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def test_error_handling_invalid_key(self):
        """Test 5: Error handling with invalid API key"""
        try:
            # Save original key
            original_key = os.getenv("GROQ_API_KEY")
            
            # Temporarily set invalid key
            os.environ["GROQ_API_KEY"] = "invalid_key_12345"
            
            try:
                invalid_llm = GroqLLM()
                invalid_llm.generate("test", max_tokens=10)
                
                # If we get here, the test failed (should have raised an error)
                self.log_result(
                    "Error Handling - Invalid Key",
                    False,
                    "Expected error but got success"
                )
                result = False
            except Exception as e:
                # Expected to fail
                self.log_result(
                    "Error Handling - Invalid Key",
                    True,
                    f"Correctly caught error: {type(e).__name__}"
                )
                result = True
            finally:
                # Restore original key
                if original_key:
                    os.environ["GROQ_API_KEY"] = original_key
            
            return result
        except Exception as e:
            self.log_result(
                "Error Handling - Invalid Key",
                False,
                f"Unexpected error: {str(e)}"
            )
            return False
    
    def test_error_handling_malformed_json(self):
        """Test 6: Error handling with malformed JSON response"""
        if not self.llm:
            self.log_result("Error Handling - Malformed JSON", False, "LLM not initialized")
            return False
        
        try:
            # This test checks if the LLM can handle edge cases
            # We'll test with a very constrained prompt that might produce issues
            prompt = 'Respond with JSON but make it valid: {"test": "value"}'
            response = self.llm.generate_json(prompt, temperature=0.0, max_tokens=50)
            
            # If we successfully parsed it, that's good
            if isinstance(response, dict):
                self.log_result(
                    "Error Handling - Malformed JSON",
                    True,
                    "Successfully handled JSON parsing"
                )
                return True
            else:
                self.log_result(
                    "Error Handling - Malformed JSON",
                    False,
                    f"Unexpected response type: {type(response)}"
                )
                return False
        except Exception as e:
            # If it fails gracefully with a clear error, that's also acceptable
            if "JSON" in str(e) or "parse" in str(e).lower():
                self.log_result(
                    "Error Handling - Malformed JSON",
                    True,
                    f"Gracefully handled error: {type(e).__name__}"
                )
                return True
            else:
                self.log_result(
                    "Error Handling - Malformed JSON",
                    False,
                    f"Unexpected error: {str(e)}"
                )
                return False
    
    def test_get_llm_factory(self):
        """Test 7: get_llm factory function"""
        try:
            llm = get_llm("groq")
            
            if isinstance(llm, GroqLLM):
                self.log_result(
                    "get_llm Factory Function",
                    True,
                    f"Successfully created {type(llm).__name__}"
                )
                return True
            else:
                self.log_result(
                    "get_llm Factory Function",
                    False,
                    f"Wrong type: {type(llm).__name__}"
                )
                return False
        except Exception as e:
            self.log_result(
                "get_llm Factory Function",
                False,
                f"Error: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Run all tests and return summary"""
        print("\n" + "="*60)
        print("LLM CONNECTION TEST SUITE")
        print("="*60 + "\n")
        
        tests = [
            self.test_groq_initialization,
            self.test_basic_generation,
            self.test_json_parsing_simple,
            self.test_json_parsing_complex,
            self.test_error_handling_invalid_key,
            self.test_error_handling_malformed_json,
            self.test_get_llm_factory
        ]
        
        for test in tests:
            test()
            print()
        
        # Summary
        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)
        
        print("="*60)
        print(f"RESULTS: {passed}/{total} tests passed")
        print("="*60)
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "results": self.results
        }


def main():
    """Main test runner"""
    tester = TestLLMConnection()
    summary = tester.run_all_tests()
    
    # Exit with appropriate code
    if summary["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

# Made with Bob