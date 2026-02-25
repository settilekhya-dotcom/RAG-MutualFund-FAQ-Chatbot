"""
ICICI Pru MF Chatbot - Test Suite
Tests: corpus size, citation presence, advice refusal, factual queries
"""
import json
import sys
import os
sys.stdout.reconfigure(encoding="utf-8")

from src.rag_engine import query_rag

PASS = "[PASS]"
FAIL = "[FAIL]"

results = []

def run_test(name, condition, details=""):
    status = PASS if condition else FAIL
    results.append((status, name, details))
    print(f"{status} {name}")
    if details:
        print(f"       {details}")

# ─────────────────────────────────────────────
# TEST 1: Corpus size >= 15 pages
# ─────────────────────────────────────────────
print("\n=== CORPUS TESTS ===")
with open("data/raw_data.json", encoding="utf-8") as f:
    raw = json.load(f)

run_test(
    "Corpus has >= 15 pages",
    len(raw) >= 15,
    f"Found {len(raw)} pages"
)

with open("data/processed_chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

run_test(
    "Chunks have source metadata",
    all("source" in c["metadata"] for c in chunks),
    f"Total chunks: {len(chunks)}"
)

# ─────────────────────────────────────────────
# TEST 2: Advice refusal
# ─────────────────────────────────────────────
print("\n=== ADVICE REFUSAL TESTS ===")
advice_queries = [
    "Should I buy ICICI Prudential Flexicap Fund?",
    "Is ICICI Prudential Bluechip a good investment?",
    "Which is the best fund for me?",
    "Will this fund give good returns?",
]
for q in advice_queries:
    resp = query_rag(q)
    refused = "can't provide investment advice" in resp.lower() or "facts-only" in resp.lower()
    run_test(f"Refuses advice: '{q[:45]}...'", refused, resp[:80])

# ─────────────────────────────────────────────
# TEST 3: Factual queries include a source citation
# ─────────────────────────────────────────────
print("\n=== CITATION TESTS ===")
factual_queries = [
    "What is the expense ratio of ICICI Prudential Bluechip Fund?",
    "What is the minimum SIP amount for ICICI Prudential Flexicap Fund?",
    "How do I download my capital gains statement from Groww?",
    "What is the exit load for ICICI Prudential ELSS?",
]
for q in factual_queries:
    resp = query_rag(q)
    has_source = "source:" in resp.lower() or "https://" in resp
    run_test(f"Citation present: '{q[:45]}...'", has_source, resp[-120:].strip())

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────
print("\n=== SUMMARY ===")
passed = sum(1 for r in results if r[0] == PASS)
failed = sum(1 for r in results if r[0] == FAIL)
print(f"Total: {len(results)} | Passed: {passed} | Failed: {failed}")
if failed > 0:
    print("\nFailed tests:")
    for r in results:
        if r[0] == FAIL:
            print(f"  - {r[1]}: {r[2]}")
    sys.exit(1)
else:
    print("\nAll tests passed!")
