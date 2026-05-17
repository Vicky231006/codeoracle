# CodeOracle Agents

AI-powered agents for intelligent code analysis using LLMs (Groq, Ollama, or IBM watsonx.ai).

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd codeoracle/agents
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure your LLM provider:

```bash
cp ../.env.example ../.env
```

Edit `.env`:
```env
# Choose your provider: groq, ollama, or watsonx
LLM_PROVIDER=groq

# Groq (recommended - fast and free)
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.1-70b-versatile

# Ollama (local)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# IBM watsonx.ai (future)
WATSONX_API_KEY=your_key_here
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL=ibm/granite-13b-instruct-v2
```

### 3. Test LLM Connection

```bash
python -m agents.base_llm
```

You should see: `✅ groq LLM is working!`

## 📦 Available Agents

### 1. **Repo Mapper Agent**
Analyzes repository structure and architecture.

```python
from agents import create_repo_mapper

agent = create_repo_mapper()
result = agent.analyze_repository(manifest)

print(result["architecture_type"])  # monolith, microservices, etc.
print(result["summary_paragraph"])  # Plain English summary
```

**Output:**
- `architecture_type`: monolith | microservices | monorepo | library | cli_tool
- `layer_map`: Files categorized by layer (frontend, backend, data, config, tests)
- `service_boundaries`: Service identification for microservices
- `summary_paragraph`: 3-4 sentence overview

---

### 2. **Dependency Analyst Agent**
Analyzes code dependencies and coupling.

```python
from agents import create_dependency_analyst

agent = create_dependency_analyst()
result = agent.analyze_dependencies(
    dependency_graph=graph,
    files_imports=imports,
    total_files=100
)

print(result["coupling_scores"])  # File coupling scores
print(result["hub_files"])        # Critical infrastructure files
```

**Output:**
- `coupling_scores`: Dict[file_path, score] (0.0-1.0)
- `circular_dependencies`: List of circular dependency chains
- `orphan_files`: Files with no imports/exports
- `hub_files`: Critical files imported by many others
- `external_risk`: External dependency risk assessment

---

### 3. **Risk Detector Agent**
Assesses change risk for files.

```python
from agents import create_risk_detector

agent = create_risk_detector()
result = agent.assess_risk(
    architecture_summary=summary,
    coupling_scores=scores,
    complexity_scores=complexity,
    hub_files=hubs,
    test_coverage=coverage
)

print(result["overall_repo_health"])  # Health score and grade
```

**Output:**
- `risk_scores`: Dict[file_path, {score, reasons, category}]
- `single_points_of_failure`: Critical files that would break the system
- `dead_code_candidates`: Potentially unused files
- `complexity_hotspots`: Files needing refactoring
- `overall_repo_health`: Score (0-100), grade (A-F), summary

**Risk Categories:**
- `critical`: score >= 0.75 (DO NOT TOUCH without review)
- `high`: score >= 0.50 (Requires careful analysis)
- `medium`: score >= 0.25 (Standard caution)
- `low`: score < 0.25 (Relatively safe)

---

### 4. **Knowledge Synthesizer Agent**
Answers natural language questions about code.

```python
from agents import create_knowledge_synthesizer

agent = create_knowledge_synthesizer()
result = agent.answer_question(
    question="How does authentication work?",
    architecture_summary=summary,
    hub_files=hubs,
    risk_summary=risk_summary,
    relevant_files_content=files
)

print(result["answer"])              # Detailed explanation
print(result["confidence"])          # high | medium | low
print(result["follow_up_questions"]) # Suggested next questions
```

**Output:**
- `answer`: Detailed plain English explanation
- `confidence`: high | medium | low
- `relevant_files`: List of files referenced in answer
- `follow_up_questions`: 2-3 suggested follow-up questions
- `impact_chain`: File flow showing dependencies

---

### 5. **Impact Simulator Agent**
Simulates "what if" scenarios.

```python
from agents import create_impact_simulator

agent = create_impact_simulator()
result = agent.simulate_impact(
    scenario="What if I delete config.py?",
    dependency_graph=graph,
    risk_scores=risks,
    architecture_summary=summary
)

print(result["estimated_risk_level"])  # catastrophic | high | medium | low
print(result["mitigation_steps"])      # Steps to take before change
```

**Output:**
- `scenario`: Paraphrased scenario
- `directly_affected`: Files directly impacted
- `transitively_affected`: Files impacted through dependencies (up to 3 hops)
- `services_affected`: Services that would be impacted
- `estimated_risk_level`: catastrophic | high | medium | low | negligible
- `mitigation_steps`: 3-5 concrete steps to take
- `confidence`: high | medium | low

---

### 6. **Supervisor Agent**
Orchestrates all other agents based on user queries.

```python
from agents import create_supervisor

supervisor = create_supervisor()
result = supervisor.process(
    user_query="Analyze the architecture and assess risks",
    manifest=manifest,
    dependency_graph=graph,
    files_imports=imports,
    total_files=100,
    complexity_scores=complexity,
    test_coverage=coverage
)

print(result["intent"])          # Detected intent
print(result["agents_invoked"])  # List of agents called
print(result["results"])         # Results from each agent
print(result["summary"])         # High-level summary
```

**Features:**
- **Intent Detection**: Automatically determines which agents to invoke
- **Multi-Agent Orchestration**: Handles complex queries requiring multiple agents
- **Context Caching**: Reuses results from previous agents to avoid redundant calls
- **Smart Routing**: Routes queries based on intent patterns

**Intent Patterns:**
- `"explore|understand|overview"` → repo_mapper
- `"depends on|imports|circular|coupling"` → dependency_analyst
- `"risky|dangerous|safe|health"` → risk_detector
- `"why|how|explain|trace"` → knowledge_synthesizer
- `"what if|impact of|remove|delete"` → impact_simulator
- `"onboarding|getting started"` → repo_mapper + knowledge_synthesizer

**Output:**
- `intent`: Detected user intent
- `agents_invoked`: List of agents that were called
- `results`: Dict mapping agent names to their results
- `summary`: High-level summary of findings
- `is_multi_intent`: Boolean indicating if query had multiple intents

**Example Multi-Intent Query:**
```python
# This will invoke repo_mapper, dependency_analyst, and risk_detector
result = supervisor.process(
    user_query="What's the architecture and what are the risks?",
    manifest=manifest,
    dependency_graph=graph,
    files_imports=imports,
    total_files=100,
    complexity_scores=complexity,
    test_coverage=coverage
)
```

**Context Management:**
```python
# Cache results for reuse
supervisor.process(user_query="Analyze architecture", manifest=manifest)

# Subsequent queries can reuse cached results
supervisor.process(user_query="What are the risks?",
                  complexity_scores=complexity,
                  test_coverage=coverage)

# Clear cache when needed
supervisor.clear_cache()

# Check cached context
cached = supervisor.get_cached_context()
```

---

## 🔧 Advanced Usage

### Custom LLM Configuration

```python
from agents.base_llm import get_llm
from agents import RepoMapperAgent

# Use specific provider
llm = get_llm("groq")  # or "ollama" or "watsonx"

# Create agent with custom LLM
agent = RepoMapperAgent(llm=llm)
```

### Disable Output Validation

```python
# Skip JSON schema validation (faster, but risky)
result = agent.execute(validate_output=False, manifest=data)
```

### Error Handling

```python
from agents import AgentError, AgentValidationError

try:
    result = agent.analyze_repository(manifest)
except AgentValidationError as e:
    print(f"Output validation failed: {e}")
except AgentError as e:
    print(f"Agent error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🔄 Switching LLM Providers

### Groq (Recommended)
- ✅ Fastest (500+ tokens/sec)
- ✅ Free tier, no credit card
- ✅ Llama 3.1 70B model

```env
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_your_key_here
```

### Ollama (Local)
- ✅ 100% free, runs locally
- ✅ Privacy - data stays on your machine
- ⚠️ Slower (20-50 tokens/sec)

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1:8b
```

### IBM watsonx.ai (Future)
- ✅ Enterprise-grade
- ✅ Granite models optimized for code
- ⚠️ Requires IBM Cloud account

```env
LLM_PROVIDER=watsonx
WATSONX_API_KEY=your_key
WATSONX_PROJECT_ID=your_project_id
```

## 🧪 Testing

Test individual agents:

```bash
# Test Repo Mapper
python -m agents.repo_mapper

# Test Dependency Analyst
python -m agents.dependency_analyst

# Test Risk Detector
python -m agents.risk_detector

# Test Knowledge Synthesizer
python -m agents.knowledge_synthesizer

# Test Impact Simulator
python -m agents.impact_simulator

# Test Supervisor
python -m agents.supervisor
```

Run comprehensive test suite:

```bash
cd codeoracle/agents/tests
python run_tests.py
```

## 📊 Performance

| Provider | Speed | Cost | Quality |
|----------|-------|------|---------|
| Groq | ⚡⚡⚡ Very Fast | 💰 Free | ⭐⭐⭐⭐⭐ Excellent |
| Ollama | ⚡ Moderate | 💰 Free | ⭐⭐⭐⭐ Good |
| watsonx.ai | ⚡⚡ Fast | 💰💰 Paid | ⭐⭐⭐⭐⭐ Excellent |

## 🐛 Troubleshooting

### "GROQ_API_KEY not found"
- Make sure `.env` file exists in `codeoracle/` directory
- Check that `GROQ_API_KEY` is set correctly

### "Failed to parse JSON response"
- LLM might be returning markdown. The code handles this automatically.
- If persistent, try lowering temperature: `agent._call_llm(prompt, temperature=0.0)`

### "Ollama API error"
- Make sure Ollama is running: `ollama serve`
- Check model is pulled: `ollama pull llama3.1:8b`

### Slow responses with Ollama
- First request loads model (2-5 sec)
- Subsequent requests are faster (0.5-2 sec)
- Consider switching to Groq for faster responses

## 📝 Architecture

```
agents/
├── base_llm.py              # LLM abstraction layer
├── base_agent.py            # Base agent class
├── repo_mapper.py           # Architecture analysis
├── dependency_analyst.py    # Dependency analysis
├── risk_detector.py         # Risk assessment
├── knowledge_synthesizer.py # Q&A agent
├── impact_simulator.py      # Impact simulation
├── supervisor.py            # Agent orchestration
├── tests/                   # Test suite
│   ├── test_agents.py       # Individual agent tests
│   ├── test_supervisor.py   # Supervisor tests
│   ├── test_integration.py  # Integration tests
│   └── run_tests.py         # Test runner
└── __init__.py             # Module exports
```

## 🔐 Security

- **Never commit `.env`** - It's in `.gitignore`
- API keys are loaded from environment only
- Use `.env.example` as template for others

## 📚 Next Steps

1. ✅ Agents implemented
2. ✅ Supervisor agent (orchestration)
3. 🔄 Build API layer
4. 🔄 Create frontend interface
5. 🔄 End-to-end demo

## 🤝 Contributing

Each agent follows the same pattern:
1. Inherit from `BaseAgent`
2. Implement `agent_name` property
3. Implement `process(**kwargs)` method
4. Add convenience methods
5. Create factory function

See existing agents for examples.