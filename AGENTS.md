# CodeOracle Agent System Architecture

## Project Overview
CodeOracle is an architectural decision support engine that helps engineers make confident decisions about unfamiliar codebases through multi-agent analysis.

## Core Problem
Engineers need to make changes RIGHT NOW to codebases they don't understand. They need decision support under uncertainty - not documentation, not onboarding, but real-time risk assessment and impact analysis.

## Agent Architecture

### Agent 1: REPO MAPPER
- **Responsibility**: Produce high-level structural map of repository
- **Input**: repo_manifest.json
- **Output**: Architecture type, layer map, service boundaries, summary
- **Model**: IBM Granite-13b-instruct-v2

### Agent 2: DEPENDENCY ANALYST
- **Responsibility**: Map import/dependency relationships, detect circular dependencies
- **Input**: repo_manifest.json (dependency_graph, imports)
- **Output**: Coupling scores, circular dependencies, orphan files, hub files
- **Model**: IBM Granite-13b-instruct-v2

### Agent 3: RISK DETECTOR
- **Responsibility**: Score files for change risk, identify dangerous files
- **Input**: Agent 1 + Agent 2 outputs + complexity scores
- **Output**: Risk scores, single points of failure, complexity hotspots, repo health
- **Model**: IBM Granite-13b-instruct-v2

### Agent 4: KNOWLEDGE SYNTHESIZER
- **Responsibility**: Answer natural language questions about codebase
- **Input**: User question + all agent outputs + file content
- **Output**: Structured answer with confidence, relevant files, follow-ups
- **Model**: IBM Granite-13b-instruct-v2

### Agent 5: IMPACT SIMULATOR
- **Responsibility**: Predict blast radius of hypothetical changes
- **Input**: User scenario + dependency graph + risk scores
- **Output**: Affected files, services, risk level, mitigation steps
- **Model**: IBM Granite-13b-instruct-v2

### SUPERVISOR AGENT
- **Responsibility**: Route user queries to appropriate specialist agents
- **Intent Classification**: explore, dependencies, risk, explain, what-if, onboarding
- **Orchestration**: watsonx Orchestrate coordination layer

## Tech Stack
- **IDE**: IBM Bob
- **Orchestration**: watsonx Orchestrate
- **Models**: watsonx.ai Granite (13b-instruct-v2, 3b-instruct)
- **Frontend**: React + Tailwind CSS + D3.js
- **Backend**: Python 3.9+
- **Parsing**: Python AST, esprima (JavaScript)

## Data Flow
1. Repository → Ingestion Pipeline → repo_manifest.json
2. Manifest → Agent 1 (Mapper) → Architecture context
3. Manifest → Agent 2 (Dependencies) → Coupling analysis
4. Agent 1 + 2 → Agent 3 (Risk) → Risk scores
5. All outputs → Agent 4 (Synthesizer) → Q&A responses
6. All outputs → Agent 5 (Impact) → What-if analysis
7. Supervisor → Routes queries → Aggregates responses → Frontend

## Demo Strategy
- Pre-process demo repository (Flask or Express)
- Cache agent outputs for instant demo responses
- 90-second wow moment: upload → risk radar → impact simulation
- 5-minute total demo time

## Hackathon Scoring Optimization
1. ✅ Bob IDE usage (exported task sessions)
2. ✅ watsonx Orchestrate as coordination layer
3. ✅ Sub-5-minute demo
4. ✅ 90-second wow moment

## Development Phases
- Phase 0: ✅ Project initialization
- Phase 1: Repository ingestion pipeline
- Phase 2: Multi-agent architecture
- Phase 3: Supervisor agent
- Phase 4: Frontend
- Phase 5: watsonx Orchestrate integration
- Phase 6: Demo preparation
- Phase 7: Bob session documentation
- Phase 8: Pitch preparation