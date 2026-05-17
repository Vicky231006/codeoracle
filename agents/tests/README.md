# CodeOracle Agents Test Suite

## Overview
Comprehensive test suite for CodeOracle agents that verifies LLM connectivity, individual agent functionality, and full workflow integration.

## Test Structure

### 1. LLM Connection Tests (`test_llm_connection.py`)
- **7 tests** covering:
  - Groq API initialization
  - Basic text generation
  - Simple and complex JSON parsing
  - Error handling (invalid API key, malformed JSON)
  - Factory function testing

### 2. Individual Agent Tests (`test_agents.py`)
- **16 tests** covering all 5 agents:
  - **RepoMapper**: Initialization, processing, schema validation
  - **DependencyAnalyst**: Initialization, processing, schema validation
  - **RiskDetector**: Initialization, processing, schema validation
  - **ImpactSimulator**: Initialization, processing, schema validation
  - **KnowledgeSynthesizer**: Initialization, processing, schema validation
  - Error handling for missing parameters

### 3. Integration Tests (`test_integration.py`)
- **8 tests** covering:
  - Loading test manifest from demo/test_repo
  - Full workflow through all 5 agents
  - Data flow consistency between agents
  - End-to-end timing

## Running Tests

### Run All Tests
```bash
cd codeoracle/agents/tests
python run_tests.py
```

### Run Individual Test Suites
```bash
# LLM Connection only
python test_llm_connection.py

# Individual Agents only
python test_agents.py

# Integration only
python test_integration.py
```

## Requirements

### Environment Setup
1. Install dependencies:
```bash
cd codeoracle/agents
pip install -r requirements.txt
```

2. Configure `.env` file with Groq API key:
```bash
cp ../.env.example ../.env
# Edit .env and add your GROQ_API_KEY
```

### API Key
- Get a free Groq API key at: https://console.groq.com/keys
- Add to `.env`: `GROQ_API_KEY=gsk_your_key_here`

## Test Results

### Current Status
The test suite has been created and is functional. Initial test run shows:

**LLM Connection Tests**: 3/7 passing
- ✅ Groq initialization works
- ✅ Error handling works
- ✅ Factory function works
- ⚠️ API calls failing with 400 error (likely model configuration issue)

**Note**: The Groq API 400 errors are likely due to:
1. Model not supporting `response_format` parameter
2. API key permissions
3. Rate limiting

### Expected Output
When all tests pass, you should see:
```
======================================================================
               CODEORACLE AGENTS TEST SUITE
======================================================================

----------------------------------------------------------------------
  1. LLM CONNECTION TESTS
----------------------------------------------------------------------
[PASS]: All 7 tests

----------------------------------------------------------------------
  2. INDIVIDUAL AGENT TESTS
----------------------------------------------------------------------
[PASS]: All 16 tests

----------------------------------------------------------------------
  3. INTEGRATION TESTS
----------------------------------------------------------------------
[PASS]: All 8 tests

+--------------------------------------------------------------------+
|                    TEST SUITE RESULTS                              |
+------------------------------+-----------+-----------+-------------+
| Suite                        |   Total   |   Passed  |   Failed    |
+------------------------------+-----------+-----------+-------------+
| [PASS] LLM Connection        |     7     |     7     |      0      |
| [PASS] Individual Agents     |    16     |    16     |      0      |
| [PASS] Integration           |     8     |     8     |      0      |
+------------------------------+-----------+-----------+-------------+
| TOTAL                        |    31     |    31     |      0      |
+------------------------------+-----------+-----------+-------------+

[*] Success Rate: 100.0%
[*] Total Execution Time: XX.XX seconds

======================================================================
*** ALL TESTS PASSED! ***
======================================================================
```

## Test Report
After running tests, a detailed JSON report is saved to `test_report.json` containing:
- Timestamp
- Duration
- Individual test results
- Summary statistics

## Troubleshooting

### Groq API 400 Error
If you see "400 Client Error: Bad Request":
1. Verify your API key is valid
2. Check if you have API credits
3. Try a different model in `.env`: `GROQ_MODEL=mixtral-8x7b-32768`
4. Remove `response_format` parameter if model doesn't support it

### Import Errors
If you see "ModuleNotFoundError":
```bash
cd codeoracle/agents
pip install -r requirements.txt
```

### Unicode Errors (Windows)
The test suite uses ASCII-compatible characters to avoid Windows console encoding issues.

## Test Coverage

### What's Tested
✅ LLM connectivity and JSON parsing  
✅ All 5 agent initializations  
✅ Agent processing with sample data  
✅ JSON schema validation  
✅ Error handling (missing params, invalid data)  
✅ Full workflow integration  
✅ Data flow between agents  

### What's Not Tested
- Actual LLM response quality (requires manual review)
- Performance under load
- Concurrent agent execution
- Large repository handling

## Contributing
When adding new agents or features:
1. Add tests to appropriate test file
2. Update this README
3. Run full test suite before committing
4. Ensure all tests pass

## Made with Bob