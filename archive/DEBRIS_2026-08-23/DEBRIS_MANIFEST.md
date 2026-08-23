# DEBRIS ARCHIVE — 2026-08-23

Purpose: preserve a single record of temporary/testing files before they are removed from RIO's active production tree. These items are **DEBRIS**, not production runtime dependencies.

## DEBRIS — Claude direct test
- `.github/workflows/claude-direct-test.yml` — temporary issue-triggered Anthropic API workflow.
- `scripts/claude_direct_test.py` — direct Anthropic test client.
- `data/claude_direct_test_result.json` — sanitized failed test result (HTTP 401 invalid x-api-key).

## DEBRIS — Bedrock/Terra model discovery test
- `.github/workflows/bedrock-terra-direct-test.yml` — temporary Bedrock direct-test workflow.
- `scripts/bedrock_terra_direct_test.py` — temporary model-cycling test script.
- `data/bedrock_terra_direct_test_result.json` — sanitized result proving `qwen.qwen3-coder-next` worked; GLM returned HTTP 200 with fenced JSON; Grok route was unsupported.

## DEBRIS — Bedrock rulebook proof test
- `.github/workflows/bedrock-rulebook-test.yml` — temporary one-shot rulebook workflow.
- `scripts/bedrock_rulebook_test.py` — temporary exact-output instruction-following test.
- `data/Rule book.txt` — generated proof artifact: `I'll follow all the rules given by founder and Victor.`

## DEBRIS — generated/cache material
- `scripts/__pycache__/` — generated Python bytecode/cache; never required as source.

## NOT DEBRIS / KEEP ACTIVE
- `.github/workflows/rio.yml` — production orchestration, direct Telegram execution, heartbeat.
- `scripts/telegram_direct_command.py` — production webhook-triggered command runner.
- `scripts/telegram_chat.py` — provider/routing implementation currently reused by direct runner; keep until refactor proves replacement.
- `scripts/rio_autonomous_executor.py` — guarded production executor.
- `scripts/heartbeat.py` — autonomous health heartbeat and transition alerts.
- `aws/telegram_webhook/lambda_function.py` — AWS webhook source/reference; do not remove during debris cleanup without verifying deployed Lambda equivalence.
- `data/RIO_3.0_DEFINITION.md` and `data/AUTONOMY_POLICY.md` — protected core/rules.

## Archive policy
1. Every item listed above is explicitly tagged **DEBRIS**.
2. Active copies may be deleted after this manifest is committed.
3. Full historical contents remain recoverable from Git commit history even after deletion.
4. No secret values are stored in this archive.
5. Future temporary files should be added under a dated `archive/DEBRIS_YYYY-MM-DD/` manifest before removal.
