# CodeOracle Virtual Environment Activation Script
# Run this script to activate the virtual environment

Write-Host "🚀 Activating CodeOracle Virtual Environment..." -ForegroundColor Green

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

Write-Host "✅ Virtual environment activated!" -ForegroundColor Green
Write-Host ""
Write-Host "📦 Installed packages:" -ForegroundColor Cyan
pip list | Select-String -Pattern "fastapi|uvicorn|pydantic|ibm-watsonx|pytest|requests"
Write-Host ""
Write-Host "🎯 Quick Commands:" -ForegroundColor Yellow
Write-Host "  • Run demo:           python demo/run_demo.py"
Write-Host "  • Start API:          python run_api.py"
Write-Host "  • Test ingestion:     python -m ingest.ingest demo/test_repo"
Write-Host "  • Run scenario 1:     python demo/scenarios/scenario1_architecture.py demo/test_manifest.json"
Write-Host ""
Write-Host "📚 For full demo guide, see: demo/DEMO_SCRIPT.md" -ForegroundColor Magenta

# Made with Bob
