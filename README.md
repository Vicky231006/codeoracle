# CodeOracle - AI-Powered Code Intelligence Platform

> IBM watsonx.ai Hackathon Project

**Status**: ✅ Production Ready | **Version**: 1.0.0

## Overview

CodeOracle is an AI-powered code intelligence platform that helps developers understand, analyze, and maintain complex codebases. Using IBM watsonx.ai's Granite models, CodeOracle provides automated architecture mapping, dependency analysis, risk detection, natural language Q&A, and impact prediction.

### Key Features

🏗️ **Architecture Analysis** - Automatically map components, layers, and design patterns  
🔗 **Dependency Analysis** - Identify dependencies, detect circular references  
⚠️ **Risk Detection** - Find security vulnerabilities and code quality issues  
💬 **Natural Language Q&A** - Ask questions about your code in plain English  
🎯 **Impact Simulation** - Predict the effects of code changes before making them  
🚀 **REST API** - Easy integration with existing tools and workflows  
🌐 **Web Interface** - Intuitive React-based frontend  

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CodeOracle System                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐      ┌──────────────────────────────┐   │
│  │   Frontend   │◄────►│       REST API               │   │
│  │  (React +    │      │    (FastAPI)                 │   │
│  │  TypeScript) │      │                              │   │
│  └──────────────┘      │  ┌────────────────────────┐  │   │
│                        │  │  Orchestrator          │  │   │
│                        │  │  - Coordinates agents  │  │   │
│                        │  │  - Manages workflow    │  │   │
│                        │  └────────────────────────┘  │   │
│                        └──────────────────────────────┘   │
│                                    │                       │
│                                    ▼                       │
│  ┌─────────────────────────────────────────────────────┐  │
│  │           Agent Supervisor                          │  │
│  │  - Routes requests to specialized agents            │  │
│  │  - Manages agent lifecycle                          │  │
│  └─────────────────────────────────────────────────────┘  │
│                        │                                   │
│         ┌──────────────┼──────────────┬──────────────┐    │
│         ▼              ▼              ▼              ▼    │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌────────┐│
│  │RepoMapper │  │Dependency │  │   Risk    │  │Knowledge││
│  │           │  │ Analyst   │  │ Detector  │  │Synthesizer││
│  └───────────┘  └───────────┘  └───────────┘  └────────┘│
│         │              │              │              │    │
│         └──────────────┴──────────────┴──────────────┘    │
│                        │                                   │
│                        ▼                                   │
│  ┌─────────────────────────────────────────────────────┐  │
│  │         IBM watsonx.ai (Granite Models)             │  │
│  │  - Natural language understanding                   │  │
│  │  - Code analysis and reasoning                      │  │
│  │  - Structured output generation                     │  │
│  └─────────────────────────────────────────────────────┘  │
│                        ▲                                   │
│                        │                                   │
│  ┌─────────────────────────────────────────────────────┐  │
│  │         Repository Ingestion                        │  │
│  │  - Code parsing (Python, JavaScript)                │  │
│  │  - AST extraction                                   │  │
│  │  - Manifest generation                              │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+ (for frontend)
- IBM watsonx.ai API credentials

### Installation

```bash
# Clone repository
git clone <repository-url>
cd codeoracle

# Install backend dependencies
pip install -r ingest/requirements.txt
pip install -r agents/requirements.txt
pip install -r api/requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..

# Configure environment
cp .env.example .env
# Edit .env with your IBM watsonx.ai credentials
```

### Configuration

Edit `.env` file:

```env
# IBM watsonx.ai Configuration
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Model Configuration
WATSONX_MODEL=ibm/granite-3-8b-instruct
WATSONX_MAX_TOKENS=2048
WATSONX_TEMPERATURE=0.7
```

### Run Demo

```bash
# Quick demo (5 minutes)
python demo/run_demo.py

# Or run individual scenarios
python demo/scenarios/scenario1_architecture.py demo/test_manifest.json
python demo/scenarios/scenario2_dependencies.py demo/test_manifest.json
python demo/scenarios/scenario3_risk.py demo/test_manifest.json
```

### Start Services

```bash
# Terminal 1: Start API
python run_api.py

# Terminal 2: Start Frontend (optional)
cd frontend
npm run dev
```

### Using Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Components

### 1. Repository Ingestion (`ingest/`)

Parses code repositories and creates structured manifests.

**Features:**
- Multi-language support (Python, JavaScript)
- AST extraction
- Metrics calculation
- Extensible parser architecture

**Usage:**
```bash
python -m ingest.ingest /path/to/repository
```

**Documentation:** [ingest/README.md](ingest/README.md)

### 2. AI Agents (`agents/`)

Five specialized agents powered by IBM watsonx.ai Granite models.

#### RepoMapper
Maps repository architecture, identifies components and layers.

#### DependencyAnalyst
Analyzes code dependencies and detects circular references.

#### RiskDetector
Identifies security vulnerabilities and code quality issues.

#### KnowledgeSynthesizer
Answers natural language questions about the codebase.

#### ImpactSimulator
Predicts the impact of code changes.

**Usage:**
```python
from agents.supervisor import AgentSupervisor

supervisor = AgentSupervisor()
result = supervisor.run_agent('repo_mapper', manifest)
```

**Documentation:** [agents/README.md](agents/README.md) | [AGENTS.md](AGENTS.md)

### 3. REST API (`api/`)

FastAPI-based REST API for all functionality.

**Endpoints:**
- `POST /ingest` - Ingest repository
- `POST /analyze/architecture` - Architecture analysis
- `POST /analyze/dependencies` - Dependency analysis
- `POST /analyze/risks` - Risk assessment
- `POST /analyze/query` - Natural language Q&A
- `POST /analyze/impact` - Impact simulation
- `POST /analyze/full` - Complete analysis

**Usage:**
```bash
curl -X POST http://localhost:8000/analyze/architecture \
  -H "Content-Type: application/json" \
  -d @manifest.json
```

**Documentation:** [api/README.md](api/README.md)

### 4. Web Frontend (`frontend/`)

React + TypeScript web interface with Tailwind CSS.

**Features:**
- Repository upload
- Interactive analysis dashboard
- Natural language query interface
- Impact simulation
- Responsive design

**Usage:**
```bash
cd frontend
npm run dev
```

**Documentation:** [frontend/README.md](frontend/README.md)

### 5. Demo & Testing (`demo/`)

Comprehensive demos and integration tests.

**Components:**
- Main demo script
- 6 demo scenarios
- Integration test suite
- Test repository

**Usage:**
```bash
# Run complete demo
python demo/run_demo.py

# Run integration tests
python demo/test_integration.py
```

**Documentation:** [demo/README.md](demo/README.md) | [demo/DEMO_SCRIPT.md](demo/DEMO_SCRIPT.md)

---

## Use Cases

### 1. Onboarding New Developers
Help new team members understand complex codebases quickly through natural language Q&A and architecture visualization.

### 2. Code Review & Quality Assurance
Automatically identify security vulnerabilities, code quality issues, and technical debt before code review.

### 3. Impact Analysis
Predict the effects of changes before implementation, reducing the risk of breaking changes.

### 4. Technical Debt Management
Track and prioritize technical debt with AI-powered risk assessment and recommendations.

### 5. Architecture Documentation
Automatically generate and maintain architecture documentation as code evolves.

### 6. Dependency Management
Identify and resolve circular dependencies, track external dependencies, and optimize dependency graphs.

---

## API Examples

### Analyze Architecture

```python
import requests

with open('manifest.json', 'r') as f:
    manifest = f.read()

response = requests.post(
    'http://localhost:8000/analyze/architecture',
    json=manifest
)

result = response.json()
print(f"Components: {len(result['result']['components'])}")
```

### Ask Questions

```python
response = requests.post(
    'http://localhost:8000/analyze/query',
    json={
        'manifest': manifest,
        'query': 'What are the security concerns in this codebase?'
    }
)

answer = response.json()['result']['answer']
print(f"Answer: {answer}")
```

### Simulate Impact

```python
response = requests.post(
    'http://localhost:8000/analyze/impact',
    json={
        'manifest': manifest,
        'change': {
            'file': 'main.py',
            'change_type': 'modify',
            'description': 'Update main logic'
        }
    }
)

impact = response.json()['result']
print(f"Impact Level: {impact['impact_level']}")
print(f"Affected Files: {len(impact['affected_files'])}")
```

---

## Testing

### Run All Tests

```bash
# Ingestion tests
python -m pytest ingest/

# Agent tests
python agents/tests/run_tests.py

# API tests
python -m pytest api/tests/

# Integration tests
python demo/test_integration.py

# Frontend tests
cd frontend
npm test
```

### Test Coverage

- ✅ Unit tests for all components
- ✅ Integration tests for workflows
- ✅ API endpoint tests
- ✅ Frontend component tests
- ✅ End-to-end demo tests

---

## Deployment

### Local Deployment

See [Quick Start](#quick-start) above.

### Docker Deployment

```bash
# Build and start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api
```

### Cloud Deployment

Supports deployment to:
- AWS (EC2, ECS, Lambda)
- Azure (Container Instances, App Service)
- GCP (Cloud Run, Compute Engine)

**Full deployment guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

## Configuration

### Environment Variables

```env
# Required
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id

# Optional
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL=ibm/granite-3-8b-instruct
WATSONX_MAX_TOKENS=2048
WATSONX_TEMPERATURE=0.7
API_HOST=0.0.0.0
API_PORT=8000
```

### Model Configuration

CodeOracle uses IBM watsonx.ai Granite models:
- **Default:** `ibm/granite-3-8b-instruct`
- **Alternative:** `ibm/granite-3-2b-instruct` (faster, less accurate)
- **Alternative:** `ibm/granite-20b-multilingual` (more accurate, slower)

---

## Performance

### Benchmarks

| Operation | Time | Notes |
|-----------|------|-------|
| Ingestion | 1-2s | Per 10 files |
| Architecture Analysis | 5-10s | Depends on complexity |
| Dependency Analysis | 5-10s | Depends on file count |
| Risk Assessment | 5-10s | Depends on code size |
| Q&A | 3-5s | Per question |
| Impact Simulation | 3-5s | Per scenario |
| Full Analysis | 30-60s | All agents |

*Times vary based on repository size and API response times*

### Optimization Tips

- Use caching for repeated analyses
- Increase API workers for concurrent requests
- Use faster model variants for quick analysis
- Implement rate limiting to manage costs

---

## Security

### Best Practices

- ✅ Never commit API keys to version control
- ✅ Use environment variables for secrets
- ✅ Enable HTTPS in production
- ✅ Implement authentication for API
- ✅ Validate all user inputs
- ✅ Use rate limiting
- ✅ Review IBM watsonx.ai data privacy policies

### Data Privacy

- Code is sent to IBM watsonx.ai for analysis
- Review IBM's data privacy and security policies
- Consider on-premises deployment for sensitive code
- Implement data encryption at rest and in transit

---

## Contributing

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 .
pylint agents/ api/ ingest/

# Run type checking
mypy agents/ api/ ingest/

# Format code
black .
```

### Adding New Language Support

1. Create parser in `ingest/parsers/`
2. Register parser in `ingest/parsers/__init__.py`
3. Add tests
4. Update documentation

### Adding New Agents

1. Create agent class extending `BaseAgent`
2. Create prompt in `prompts/`
3. Define JSON schema
4. Add tests
5. Register in supervisor

---

## Troubleshooting

### Common Issues

**API Connection Errors**
```bash
# Check API is running
curl http://localhost:8000/health

# Verify credentials
echo $WATSONX_API_KEY
```

**Import Errors**
```bash
# Ensure you're in the correct directory
cd codeoracle
python demo/run_demo.py
```

**Memory Issues**
```bash
# Increase Docker memory limits
# Edit docker-compose.yml
```

**See full troubleshooting guide:** [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting)

---

## Documentation

- **[AGENTS.md](AGENTS.md)** - Detailed agent documentation
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guide
- **[CHECKLIST.md](CHECKLIST.md)** - Project completion checklist
- **[demo/README.md](demo/README.md)** - Demo documentation
- **[demo/DEMO_SCRIPT.md](demo/DEMO_SCRIPT.md)** - Presentation script
- **[ingest/README.md](ingest/README.md)** - Ingestion documentation
- **[agents/README.md](agents/README.md)** - Agent documentation
- **[api/README.md](api/README.md)** - API documentation
- **[frontend/README.md](frontend/README.md)** - Frontend documentation

---

## Project Status

✅ **Phase 1:** Repository Ingestion - Complete  
✅ **Phase 2:** AI Agents - Complete  
✅ **Phase 3:** API & Orchestration - Complete  
✅ **Phase 4:** Frontend - Complete  
✅ **Phase 5:** Demo & Integration - Complete  

**Current Status:** 🎉 Production Ready

See [CHECKLIST.md](CHECKLIST.md) for detailed completion status.

---

## Tech Stack

### Backend
- **Python 3.11** - Core language
- **FastAPI** - REST API framework
- **IBM watsonx.ai** - AI/ML platform
- **Granite Models** - LLM for code analysis

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Vite** - Build tool
- **Zustand** - State management

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **pytest** - Testing framework
- **Vitest** - Frontend testing

---

## Cost Estimation

### IBM watsonx.ai Usage

Approximate monthly costs (varies by usage):
- **Light:** ~$50-100/month (100 analyses/day)
- **Medium:** ~$250-500/month (500 analyses/day)
- **Heavy:** ~$1000-2000/month (2000 analyses/day)

### Infrastructure

- **Local:** Free
- **Docker:** Free (local) or ~$30-100/month (cloud)
- **Cloud:** ~$100-600/month depending on scale

**See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed cost breakdown**

---

## Acknowledgments

- **IBM watsonx.ai** - AI platform and Granite models
- **IBM Bob Hackathon** - Project inspiration
- **Open Source Community** - Various libraries and tools

---
## Quick Links

- 📚 [Full Documentation](#documentation)
- 🚀 [Quick Start](#quick-start)
- 🎯 [Demo Guide](demo/README.md)
- 🔧 [API Reference](api/README.md)
- 🏗️ [Architecture](#architecture)
- 📦 [Deployment Guide](DEPLOYMENT.md)
- ✅ [Project Checklist](CHECKLIST.md)
