#!/usr/bin/env python3
"""
Simple test script to verify CodeOracle setup
"""
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 60)
print("CodeOracle Simple Test")
print("=" * 60)

# Test 1: Import ingest module
print("\n[Test 1] Testing ingest module...")
try:
    from ingest.ingest import process_repository
    print("[OK] Ingest module imported successfully")
except Exception as e:
    print(f"[ERROR] Failed to import ingest: {e}")
    sys.exit(1)

# Test 2: Import agents
print("\n[Test 2] Testing agents module...")
try:
    from agents.supervisor import SupervisorAgent
    from agents.repo_mapper import RepoMapperAgent
    print("[OK] Agents imported successfully")
except Exception as e:
    print(f"[ERROR] Failed to import agents: {e}")
    sys.exit(1)

# Test 3: Test ingestion
print("\n[Test 3] Testing repository ingestion...")
try:
    manifest = process_repository("demo/test_repo")
    print(f"[OK] Ingestion successful!")
    print(f"     Files processed: {manifest['total_files']}")
    print(f"     Total lines: {manifest['total_lines']}")
    print(f"     Primary language: {manifest['language_primary']}")
except Exception as e:
    print(f"[ERROR] Ingestion failed: {e}")
    sys.exit(1)

# Test 4: Test agent
print("\n[Test 4] Testing RepoMapper agent...")
try:
    agent = RepoMapperAgent()
    result = agent.process(manifest=manifest)
    print(f"[OK] Agent executed successfully!")
    if 'result' in result and 'components' in result['result']:
        print(f"     Components found: {len(result['result']['components'])}")
except Exception as e:
    print(f"[ERROR] Agent failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)

# Made with Bob
