# CodeOracle Demo Script

This script provides a step-by-step walkthrough for presenting CodeOracle in demos, presentations, or videos.

## Demo Overview

**Duration:** 15-20 minutes  
**Audience:** Technical stakeholders, developers, architects  
**Goal:** Showcase CodeOracle's AI-powered code analysis capabilities

---

## Introduction (2 minutes)

### Talking Points

"Welcome to CodeOracle - an AI-powered code intelligence platform that helps developers understand, analyze, and maintain complex codebases.

CodeOracle uses IBM watsonx.ai's Granite models to provide:
- **Automated architecture mapping**
- **Dependency analysis**
- **Risk detection**
- **Natural language Q&A about your code**
- **Impact prediction for changes**

Let me show you how it works."

### Screen: Project Overview

Show the CodeOracle directory structure:
```
codeoracle/
├── ingest/          # Code parsing and ingestion
├── agents/          # 5 specialized AI agents
├── api/             # REST API layer
├── frontend/        # React web interface
└── demo/            # Demo and tests
```

---

## Part 1: Repository Ingestion (2 minutes)

### Talking Points

"First, CodeOracle ingests your repository. It parses the code, extracts structure, and creates a comprehensive manifest."

### Demo Steps

1. **Show test repository**
   ```bash
   ls demo/test_repo/
   ```
   
   "Here's our sample Python project with multiple files, dependencies, and tests."

2. **Run ingestion**
   ```bash
   cd codeoracle
   python -m ingest.ingest demo/test_repo
   ```

3. **Show manifest**
   ```bash
   cat demo/test_manifest.json
   ```
   
   "The manifest contains parsed code, AST information, metrics, and metadata."

### Expected Output

```json
{
  "repository": {
    "name": "test_repo",
    "path": "demo/test_repo"
  },
  "files": [
    {
      "path": "main.py",
      "language": "python",
      "content": "...",
      "functions": [...],
      "classes": [...],
      "imports": [...]
    }
  ]
}
```

---

## Part 2: Architecture Analysis (3 minutes)

### Talking Points

"Now let's analyze the architecture. The RepoMapper agent uses AI to identify components, layers, and design patterns."

### Demo Steps

1. **Run architecture scenario**
   ```bash
   python demo/scenarios/scenario1_architecture.py demo/test_manifest.json
   ```

2. **Highlight key findings**
   - Components identified
   - Architectural layers
   - Design patterns detected
   - Entry points

### Expected Output

```
ARCHITECTURE OVERVIEW:
Type: Layered Architecture
Description: Application with clear separation of concerns

COMPONENTS (3):
• Main Application
  Type: Application Layer
  Purpose: Core application logic and entry point
  Files: main.py

• Utilities
  Type: Service Layer
  Purpose: Reusable utility functions
  Files: utils.py

• Configuration
  Type: Infrastructure Layer
  Purpose: Application configuration management
  Files: config.py
```

### Talking Points

"Notice how the AI automatically identified the layered architecture and categorized each component by its purpose."

---

## Part 3: Dependency Analysis (3 minutes)

### Talking Points

"Understanding dependencies is crucial. Let's see how CodeOracle maps the dependency graph."

### Demo Steps

1. **Run dependency scenario**
   ```bash
   python demo/scenarios/scenario2_dependencies.py demo/test_manifest.json
   ```

2. **Highlight findings**
   - Internal dependencies
   - External packages
   - Circular dependencies (if any)
   - Dependency metrics

### Expected Output

```
DEPENDENCIES (5):
• main.py → utils.py
  Type: import
  Line: 3

• main.py → config.py
  Type: import
  Line: 4

EXTERNAL DEPENDENCIES (3):
• requests
  Version: 2.31.0
  Used by: main.py, utils.py

DEPENDENCY GRAPH:
Nodes: 5
Edges: 8
```

### Talking Points

"The dependency graph helps identify tightly coupled code and potential refactoring opportunities."

---

## Part 4: Risk Assessment (3 minutes)

### Talking Points

"Security and code quality are critical. The RiskDetector agent scans for vulnerabilities and issues."

### Demo Steps

1. **Run risk scenario**
   ```bash
   python demo/scenarios/scenario3_risk.py demo/test_manifest.json
   ```

2. **Highlight findings**
   - Risk level and score
   - Security vulnerabilities
   - Code quality issues
   - Technical debt

### Expected Output

```
OVERALL RISK ASSESSMENT:
Risk Score: 45/100
Risk Level: MEDIUM

RISKS IDENTIFIED (8):
• CRITICAL: 1
• HIGH: 2
• MEDIUM: 3
• LOW: 2

CRITICAL & HIGH SEVERITY RISKS:
• [CRITICAL] Hardcoded Credentials
  Category: security
  File: config.py
  Line: 15
  Description: API key hardcoded in source code
  Recommendation: Use environment variables
```

### Talking Points

"The AI identifies specific issues with severity levels and provides actionable recommendations."

---

## Part 5: Natural Language Q&A (3 minutes)

### Talking Points

"One of the most powerful features - ask questions about your code in plain English."

### Demo Steps

1. **Run Q&A scenario**
   ```bash
   python demo/scenarios/scenario4_qa.py demo/test_manifest.json
   ```

2. **Show sample questions and answers**

### Expected Output

```
Question 1: What is the main purpose of this repository?
A: This repository implements a data processing application that 
   fetches data from external APIs, processes it using utility 
   functions, and stores results. The main entry point is main.py 
   which orchestrates the workflow.

Confidence: 85.0%
Sources: main.py, utils.py, config.py

Question 2: Are there any security concerns?
A: Yes, there are security concerns. The config.py file contains 
   hardcoded API credentials which should be moved to environment 
   variables. Additionally, the application doesn't validate input 
   data before processing.

Confidence: 78.5%
```

### Talking Points

"The AI understands your codebase and can answer complex questions with high confidence."

---

## Part 6: Impact Simulation (2 minutes)

### Talking Points

"Before making changes, predict their impact. The ImpactSimulator shows what will be affected."

### Demo Steps

1. **Run impact scenario**
   ```bash
   python demo/scenarios/scenario5_impact.py demo/test_manifest.json
   ```

2. **Show impact analysis**

### Expected Output

```
Scenario 1: Modify Main Application
File: main.py
Change Type: modify

Impact Level: HIGH
Risk Score: 75/100

Affected Files (4):
  • utils.py
    Reason: Direct dependency
    Impact: Function calls may need updates
  
  • tests/test_main.py
    Reason: Tests main.py functionality
    Impact: Tests will need to be updated

Tests to Run (3):
  • tests/test_main.py::test_process_data
  • tests/test_main.py::test_error_handling
  • tests/test_integration.py::test_full_workflow

Recommendations:
  • Update unit tests after changes
  • Review dependent modules
  • Run full test suite before deployment
```

### Talking Points

"This helps prevent breaking changes and ensures you test the right components."

---

## Part 7: Complete Workflow (2 minutes)

### Talking Points

"Let's see everything working together in one automated workflow."

### Demo Steps

1. **Run full demo**
   ```bash
   python demo/run_demo.py
   ```

2. **Show progress through all steps**
   - Ingestion
   - All 5 agents
   - API integration
   - Final report

### Expected Output

```
================================================================================
  CodeOracle End-to-End Demo
================================================================================

[Step 1] Repository Ingestion
✓ Manifest created: demo/demo_output/manifest.json
✓ Files analyzed: 5

[Step 2] Architecture Analysis (RepoMapper)
✓ Architecture analysis complete
✓ Components identified: 3
✓ Layers identified: 3

[Step 3] Dependency Analysis (DependencyAnalyst)
✓ Dependency analysis complete
✓ Dependencies found: 5

[Step 4] Risk Assessment (RiskDetector)
✓ Risk assessment complete
✓ Risks identified: 8

[Step 5] Q&A Demo (KnowledgeSynthesizer)
✓ Q&A demo complete

[Step 6] Impact Simulation (ImpactSimulator)
✓ Impact simulation complete

[Step 7] API Integration Test
✓ API integration test passed

================================================================================
  Demo Complete!
================================================================================
Duration: 45.23 seconds
Successful steps: 8/8
```

---

## Part 8: API & Frontend (Optional, 2 minutes)

### Talking Points

"CodeOracle also provides a REST API and web interface for easy integration."

### Demo Steps

1. **Show API**
   ```bash
   python run_api.py
   ```
   
   "The API exposes all functionality via REST endpoints."

2. **Show Frontend** (if available)
   ```bash
   cd frontend
   npm run dev
   ```
   
   "The React frontend provides an intuitive interface for all features."

---

## Conclusion (1 minute)

### Talking Points

"To summarize, CodeOracle provides:

✓ **Automated code analysis** - No manual review needed  
✓ **AI-powered insights** - Leveraging IBM watsonx.ai  
✓ **Multiple perspectives** - 5 specialized agents  
✓ **Natural language interface** - Ask questions in plain English  
✓ **Impact prediction** - Understand changes before making them  
✓ **Easy integration** - REST API and web interface  

CodeOracle helps teams:
- Understand complex codebases faster
- Identify risks and technical debt
- Make informed decisions about changes
- Maintain code quality and security

Thank you! Questions?"

---

## Q&A Preparation

### Common Questions

**Q: What languages does it support?**  
A: Currently Python and JavaScript, with extensible parser architecture for adding more languages.

**Q: How accurate is the AI analysis?**  
A: The AI provides confidence scores with each analysis. Typical confidence is 75-90% for well-structured code.

**Q: Can it analyze large codebases?**  
A: Yes, it's designed for production codebases. Performance scales with repository size.

**Q: How does it integrate with existing tools?**  
A: Via REST API - can integrate with CI/CD, IDEs, or custom tools.

**Q: What about private/sensitive code?**  
A: All analysis happens through IBM watsonx.ai with enterprise security. Code is not stored or shared.

**Q: How much does it cost?**  
A: Depends on IBM watsonx.ai usage. See deployment guide for cost estimation.

---

## Demo Tips

### Before the Demo

- [ ] Test all commands work
- [ ] Verify API credentials are configured
- [ ] Check test repository is present
- [ ] Clear previous demo outputs
- [ ] Have backup slides ready
- [ ] Test internet connection

### During the Demo

- Speak clearly and at moderate pace
- Explain what you're doing before running commands
- Highlight key outputs and insights
- Be prepared for questions at any time
- Have the architecture diagram ready
- Keep to time limits

### After the Demo

- Share demo repository link
- Provide documentation links
- Offer to run custom analysis
- Collect feedback
- Follow up on questions

---

## Backup Slides

Prepare slides covering:
1. Architecture diagram
2. Agent descriptions
3. Use cases
4. Integration examples
5. Pricing/licensing
6. Roadmap

---

## Demo Variations

### Quick Demo (5 minutes)
- Run scenario 6 only
- Show final report
- Answer questions

### Technical Deep Dive (30 minutes)
- Show code structure
- Explain agent implementation
- Demonstrate API calls
- Show prompt engineering
- Discuss architecture decisions

### Business Demo (10 minutes)
- Focus on benefits
- Show ROI examples
- Discuss use cases
- Less technical detail
- More business value

---

## Resources

- Full documentation: `../README.md`
- API docs: `../api/README.md`
- Agent docs: `../agents/README.md`
- Deployment guide: `../DEPLOYMENT.md`
- Demo repository: `test_repo/`