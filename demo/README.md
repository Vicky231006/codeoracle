# CodeOracle Demo Guide

This directory contains comprehensive demos and tests for the CodeOracle system.

## Overview

The demo showcases the complete CodeOracle workflow:
1. **Repository Ingestion** - Parse and analyze code structure
2. **Architecture Analysis** - Map components and layers
3. **Dependency Analysis** - Identify dependencies and relationships
4. **Risk Assessment** - Detect security and quality issues
5. **Knowledge Q&A** - Answer questions about the codebase
6. **Impact Simulation** - Predict effects of code changes
7. **API Integration** - Demonstrate orchestrated analysis

## Quick Start

### Run Complete Demo

```bash
# From the codeoracle directory
python demo/run_demo.py

# With custom repository
python demo/run_demo.py --repo-path /path/to/repo --output-dir demo/output

# Skip ingestion if manifest exists
python demo/run_demo.py --skip-ingestion
```

### Run Individual Scenarios

```bash
# Scenario 1: Architecture Analysis
python demo/scenarios/scenario1_architecture.py demo/test_manifest.json

# Scenario 2: Dependency Analysis
python demo/scenarios/scenario2_dependencies.py demo/test_manifest.json

# Scenario 3: Risk Assessment
python demo/scenarios/scenario3_risk.py demo/test_manifest.json

# Scenario 4: Q&A Demo
python demo/scenarios/scenario4_qa.py demo/test_manifest.json

# Scenario 5: Impact Simulation
python demo/scenarios/scenario5_impact.py demo/test_manifest.json

# Scenario 6: Full Workflow
python demo/scenarios/scenario6_full_workflow.py demo/test_repo
```

### Run Integration Tests

```bash
# Run all integration tests
python demo/test_integration.py

# Run with unittest
python -m unittest demo.test_integration -v
```

## Demo Components

### 1. Main Demo Script (`run_demo.py`)

Automated end-to-end demo that:
- Ingests the test repository
- Runs all 5 agents sequentially
- Tests API integration
- Generates comprehensive report

**Output:**
- `demo_output/manifest.json` - Repository manifest
- `demo_output/*_result.json` - Individual agent results
- `demo_output/demo_report.json` - Complete demo report

### 2. Demo Scenarios

#### Scenario 1: Architecture Analysis
Demonstrates RepoMapper agent identifying:
- Components and their purposes
- Architectural layers
- Design patterns
- Entry points
- Key insights

#### Scenario 2: Dependency Analysis
Demonstrates DependencyAnalyst agent analyzing:
- Internal dependencies
- External dependencies
- Dependency graph
- Circular dependencies
- Dependency metrics

#### Scenario 3: Risk Assessment
Demonstrates RiskDetector agent detecting:
- Security vulnerabilities
- Code quality issues
- Technical debt
- Risk severity levels
- Recommendations

#### Scenario 4: Natural Language Q&A
Demonstrates KnowledgeSynthesizer agent answering:
- Purpose and functionality questions
- Architecture questions
- Security concerns
- Code quality questions
- Impact questions

#### Scenario 5: Impact Simulation
Demonstrates ImpactSimulator agent predicting:
- Affected files from changes
- Impact levels (low/medium/high/critical)
- Required tests
- Recommendations
- Warnings

#### Scenario 6: Complete Workflow
Demonstrates full end-to-end workflow:
- Repository ingestion
- All agents in sequence
- API orchestration
- Comprehensive reporting

### 3. Integration Tests (`test_integration.py`)

Comprehensive test suite covering:
- Repository ingestion
- Individual agent functionality
- API orchestrator
- Data flow through layers
- Error handling
- Performance benchmarks
- End-to-end workflow

**Test Coverage:**
- 11 integration tests
- All system components
- Error scenarios
- Performance validation

## Test Repository

The `test_repo/` directory contains a sample Python project for testing:

```
test_repo/
├── main.py           # Main application
├── utils.py          # Utility functions
├── config.py         # Configuration
├── requirements.txt  # Dependencies
└── tests/
    └── test_main.py  # Unit tests
```

This repository is designed to demonstrate:
- Multiple file types
- Dependencies between modules
- Common code patterns
- Potential risks and issues
- Testing infrastructure

## Expected Outputs

### Demo Report Structure

```json
{
  "demo_info": {
    "timestamp": "2024-01-15T10:30:00",
    "duration_seconds": 45.2,
    "repository": "demo/test_repo",
    "output_directory": "demo/demo_output"
  },
  "results": {
    "ingestion": { "status": "success", ... },
    "repo_mapper": { "status": "success", ... },
    "dependency_analyst": { "status": "success", ... },
    "risk_detector": { "status": "success", ... },
    "knowledge_synthesizer": [...],
    "impact_simulator": [...],
    "api_integration": { "status": "success", ... }
  },
  "summary": {
    "total_steps": 8,
    "successful_steps": 8,
    "failed_steps": 0
  }
}
```

### Agent Result Structure

Each agent produces structured JSON output:

```json
{
  "status": "success",
  "agent": "repo_mapper",
  "timestamp": "2024-01-15T10:30:00",
  "result": {
    // Agent-specific analysis results
  },
  "metadata": {
    "execution_time": 5.2,
    "model_used": "watsonx/granite-3.0-8b-instruct"
  }
}
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Ensure you're running from the codeoracle directory
cd codeoracle
python demo/run_demo.py
```

#### 2. Missing Dependencies
```bash
# Install required packages
pip install -r ingest/requirements.txt
pip install -r agents/requirements.txt
pip install -r api/requirements.txt
```

#### 3. API Connection Issues
```bash
# Check .env file has correct credentials
cp .env.example .env
# Edit .env with your IBM watsonx credentials
```

#### 4. Test Repository Not Found
```bash
# Ensure test_repo exists
ls demo/test_repo/
# Should show: main.py, utils.py, config.py, etc.
```

### Debug Mode

Run with verbose output:
```bash
# Set environment variable
export DEBUG=1
python demo/run_demo.py
```

## Performance Benchmarks

Expected execution times (approximate):

| Component | Time |
|-----------|------|
| Ingestion | 1-2s |
| RepoMapper | 5-10s |
| DependencyAnalyst | 5-10s |
| RiskDetector | 5-10s |
| KnowledgeSynthesizer | 3-5s per question |
| ImpactSimulator | 3-5s per scenario |
| Full Demo | 30-60s |

*Times vary based on repository size and API response times*

## Customization

### Using Your Own Repository

```bash
# Run demo on your repository
python demo/run_demo.py --repo-path /path/to/your/repo

# Run specific scenario
python demo/scenarios/scenario1_architecture.py /path/to/manifest.json
```

### Custom Questions for Q&A

```bash
# Modify scenario4_qa.py or pass custom questions
python demo/scenarios/scenario4_qa.py manifest.json \
  --questions "What is the architecture?" "Are there security issues?"
```

### Custom Impact Scenarios

Edit `scenario5_impact.py` to add your own change scenarios:

```python
scenarios = [
    {
        'name': 'My Custom Change',
        'file': 'my_file.py',
        'change_type': 'modify',
        'description': 'Description of change'
    }
]
```

## Demo for Presentations

For live demonstrations:

1. **Quick Demo (5 minutes)**
   ```bash
   python demo/scenarios/scenario6_full_workflow.py demo/test_repo
   ```

2. **Detailed Demo (15 minutes)**
   ```bash
   python demo/run_demo.py
   ```

3. **Interactive Demo**
   - Run individual scenarios
   - Show specific agent outputs
   - Answer custom questions

## Next Steps

After running the demo:

1. **Review Results** - Check `demo_output/` for detailed analysis
2. **Try Your Code** - Run on your own repositories
3. **Explore API** - Use the REST API for integration
4. **Frontend Demo** - Try the web interface (see `frontend/README.md`)
5. **Deploy** - Follow `DEPLOYMENT.md` for production setup

## Support

For issues or questions:
- Check troubleshooting section above
- Review main `README.md`
- Check agent documentation in `agents/README.md`
- Review API documentation in `api/README.md`

## Demo Video Script

See `DEMO_SCRIPT.md` for a step-by-step presentation guide with talking points.