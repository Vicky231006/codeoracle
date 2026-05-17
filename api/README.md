# CodeOracle API Documentation

REST API for CodeOracle - AI-powered code analysis and orchestration system.

## Overview

The CodeOracle API provides a comprehensive set of endpoints for analyzing codebases, detecting risks, answering questions, and simulating the impact of changes. It uses IBM watsonx.ai for intelligent analysis and orchestration.

## Features

- 🔍 **Repository Analysis** - Complete codebase structure and architecture analysis
- 📦 **Dependency Analysis** - Identify dependencies, vulnerabilities, and coupling issues
- ⚠️ **Risk Assessment** - Detect security, maintainability, and complexity risks
- 💬 **Natural Language Q&A** - Ask questions about your codebase in plain English
- 🎯 **Impact Simulation** - Predict the impact of proposed changes
- 🤖 **Intelligent Orchestration** - Supervisor agent coordinates multiple analyses

## Installation

### Prerequisites

- Python 3.9+
- IBM watsonx.ai account with API credentials

### Setup

1. **Install dependencies:**
```bash
cd codeoracle/api
pip install -r requirements.txt
```

2. **Configure environment variables:**

Create a `.env` file in the `codeoracle` directory:
```env
WATSONX_API_KEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

3. **Start the server:**
```bash
cd codeoracle
python run_api.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Health & Status

#### GET /api/health
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "agents_available": [
    "repo_mapper",
    "dependency_analyst",
    "risk_detector",
    "knowledge_synthesizer",
    "impact_simulator",
    "supervisor"
  ]
}
```

#### GET /api/status
Get detailed system status.

**Response:**
```json
{
  "status": "healthy",
  "agents": [...],
  "cache_size": 0,
  "uptime": 123.45
}
```

### Analysis Endpoints

#### POST /api/analyze/repository
Perform full repository analysis.

**Request:**
```json
{
  "manifest_path": "/path/to/manifest.json",
  "analysis_depth": "standard"
}
```

**Parameters:**
- `manifest_path` (required): Path to repository manifest JSON file
- `analysis_depth` (optional): "quick", "standard", or "deep" (default: "standard")

**Response:**
```json
{
  "status": "success",
  "repository_map": {
    "architecture_type": "monolithic",
    "components": [...],
    "summary_paragraph": "..."
  },
  "dependencies": {...},
  "risks": {...},
  "summary": "Analysis complete",
  "execution_time": 2.5
}
```

#### POST /api/analyze/dependencies
Analyze repository dependencies.

**Request:**
```json
{
  "manifest_path": "/path/to/manifest.json",
  "focus_areas": ["security", "performance"]
}
```

**Response:**
```json
{
  "status": "success",
  "dependencies": {...},
  "vulnerabilities": [...],
  "recommendations": [...],
  "execution_time": 1.5
}
```

#### POST /api/analyze/risk
Assess repository risks.

**Request:**
```json
{
  "manifest_path": "/path/to/manifest.json",
  "risk_categories": ["security", "maintainability"]
}
```

**Response:**
```json
{
  "status": "success",
  "risks": [...],
  "overall_risk_score": 35.5,
  "critical_issues": [...],
  "recommendations": [...],
  "execution_time": 1.8
}
```

### Query Endpoint

#### POST /api/query
Answer natural language questions about the codebase.

**Request:**
```json
{
  "manifest_path": "/path/to/manifest.json",
  "query": "What is the main entry point of this application?",
  "context": {
    "focus": "main files"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "answer": "The main entry point is...",
  "sources": [...],
  "confidence": 0.92,
  "execution_time": 1.2
}
```

### Simulation Endpoint

#### POST /api/simulate/impact
Simulate the impact of proposed changes.

**Request:**
```json
{
  "manifest_path": "/path/to/manifest.json",
  "change_description": "Refactor authentication module",
  "affected_files": ["auth.py", "user.py"],
  "change_type": "modification"
}
```

**Parameters:**
- `change_type`: "addition", "modification", or "deletion"

**Response:**
```json
{
  "status": "success",
  "impact_analysis": {...},
  "affected_components": [...],
  "risk_level": "medium",
  "recommendations": [...],
  "test_suggestions": [...],
  "execution_time": 1.5
}
```

### Orchestration Endpoint

#### POST /api/orchestrate
Orchestrate complex tasks using the supervisor agent.

**Request:**
```json
{
  "manifest_path": "/path/to/manifest.json",
  "task": "Analyze the repository and identify all security risks",
  "agents_to_use": ["repo_mapper", "risk_detector"],
  "max_iterations": 5
}
```

**Parameters:**
- `agents_to_use` (optional): Specific agents to use. If not provided, supervisor decides.
- `max_iterations` (optional): Maximum iterations (1-20, default: 5)

**Response:**
```json
{
  "status": "success",
  "task_result": {...},
  "agents_used": ["repo_mapper", "risk_detector"],
  "execution_plan": [...],
  "total_execution_time": 3.5,
  "recommendations": [...]
}
```

### Cache Management

#### DELETE /api/cache
Clear the orchestrator cache.

**Response:**
```json
{
  "status": "success",
  "message": "Cache cleared"
}
```

## Usage Examples

### Using curl

**Health check:**
```bash
curl http://localhost:8000/api/health
```

**Repository analysis:**
```bash
curl -X POST http://localhost:8000/api/analyze/repository \
  -H "Content-Type: application/json" \
  -d '{
    "manifest_path": "/path/to/manifest.json",
    "analysis_depth": "standard"
  }'
```

**Natural language query:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "manifest_path": "/path/to/manifest.json",
    "query": "What are the main components?"
  }'
```

### Using Python requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/health")
print(response.json())

# Repository analysis
response = requests.post(
    "http://localhost:8000/api/analyze/repository",
    json={
        "manifest_path": "/path/to/manifest.json",
        "analysis_depth": "standard"
    }
)
result = response.json()
print(f"Analysis complete: {result['summary']}")

# Natural language query
response = requests.post(
    "http://localhost:8000/api/query",
    json={
        "manifest_path": "/path/to/manifest.json",
        "query": "What is the main function?"
    }
)
answer = response.json()
print(f"Answer: {answer['answer']}")
print(f"Confidence: {answer['confidence']}")
```

### Using JavaScript/TypeScript

```javascript
// Health check
const healthResponse = await fetch('http://localhost:8000/api/health');
const health = await healthResponse.json();
console.log(health);

// Repository analysis
const analysisResponse = await fetch('http://localhost:8000/api/analyze/repository', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    manifest_path: '/path/to/manifest.json',
    analysis_depth: 'standard'
  })
});
const result = await analysisResponse.json();
console.log('Analysis:', result);
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK` - Successful request
- `404 Not Found` - Manifest file not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service unhealthy

**Error response format:**
```json
{
  "error": "Error message",
  "detail": "Detailed error information",
  "code": "ERROR_CODE"
}
```

## Configuration

Configuration is managed through environment variables and the `config.py` file.

### Environment Variables

- `WATSONX_API_KEY` - IBM watsonx.ai API key (required)
- `WATSONX_PROJECT_ID` - IBM watsonx.ai project ID (required)
- `WATSONX_URL` - IBM watsonx.ai URL (default: https://us-south.ml.cloud.ibm.com)

### Server Settings

Edit `api/config.py` to customize:
- Host and port
- CORS origins
- Logging level
- Agent timeout
- Cache TTL

## Deployment

### Development

```bash
python run_api.py
```

### Production

Use a production ASGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn api.server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY codeoracle /app/codeoracle
COPY requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "codeoracle/run_api.py"]
```

Build and run:
```bash
docker build -t codeoracle-api .
docker run -p 8000:8000 --env-file .env codeoracle-api
```

## Testing

Run the test suite:

```bash
cd codeoracle/api
pytest tests/ -v
```

Run specific test file:
```bash
pytest tests/test_api.py -v
```

Run with coverage:
```bash
pytest tests/ --cov=api --cov-report=html
```

## Performance

- **Concurrent Requests**: Supports up to 10 concurrent requests (configurable)
- **Caching**: Results are cached for 1 hour (configurable)
- **Timeouts**: Agent operations timeout after 5 minutes (configurable)

## Security

- CORS is enabled for specified origins
- API key validation for watsonx.ai
- Input validation using Pydantic
- No sensitive data in logs

## Troubleshooting

### API won't start

1. Check environment variables are set
2. Verify Python version (3.9+)
3. Check port 8000 is not in use

### Slow responses

1. Check watsonx.ai API status
2. Increase timeout settings
3. Use "quick" analysis depth for faster results

### Agent errors

1. Verify manifest file format
2. Check watsonx.ai credentials
3. Review logs in `codeoracle_api.log`

## Support

For issues and questions:
- Check the logs: `codeoracle_api.log`
- Review API documentation: http://localhost:8000/docs
- Check agent documentation: `codeoracle/agents/README.md`

## License

Part of the CodeOracle project.