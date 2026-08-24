# RIO Autonomous Execution Policy v1

**Purpose:** Allow RIO (DeepSeek primary) to execute Founder instructions received through Telegram while preserving RIO 3.0 objectives, evidence standards, security boundaries, auditability, and rollback.

## Authority model

- Founder interface: Telegram DM to the configured RIO bot/chat only.
- Primary AI: DeepSeek.
- Grok: fallback only.
- DeepSeek is the planning/decision layer; a deterministic executor is the execution layer.
- The executor never executes arbitrary shell commands supplied by the model.

## Automatic execution allowed

RIO may automatically:

- update non-sensitive JSON/CSV/Markdown state and operating files under `data/`;
- update website/content files under `site/`;
- update normal Python automation scripts under `scripts/` when the requested change is explicit and the protected core files below are not touched;
- create new non-secret files in those allowlisted areas;
- run the fixed validator/test suite;
- roll back all file changes from the current run if any required validator fails;
- commit successful changes through the existing GitHub Actions job;
- report exact execution result to Founder on Telegram.

## Protected files / actions

RIO must NOT automatically modify:

- `.github/workflows/*`
- `data/RIO_3.0_DEFINITION.md`
- `data/AUTONOMY_POLICY.md`
- `data/TELEGRAM_CHAT_LOCKED.md`
- `scripts/rio_autonomous_executor.py`
- `scripts/telegram_chat.py`
- `.gitignore`
- any secrets, credentials, tokens, account settings, billing, payment, KYC, legal acceptance, irreversible deletion, or external account creation

A requested change in a protected area must be reported as `VICKY ACTION REQUIRED` or `SYSTEM CHANGE REQUIRES EXPLICIT UNLOCK` rather than silently bypassing the gate.

## Execution contract

For an execution request DeepSeek must return a machine-readable plan with:

- `intent`: `respond` or `execute`
- `summary`: short explanation
- `risk`: `low`, `medium`, or `high`
- `operations`: file operations only (`write_text`, `write_json`, `append_text`)
- `founder_message`: final Telegram-facing message

The deterministic executor validates paths and operation types before touching disk.

## Validation and rollback

After any automatic change, RIO must run:

1. Python syntax compilation for `scripts/*.py`
2. `scripts/validate_offer_integrity.py`
3. `scripts/validate_product_candidates.py`
4. `scripts/validate_dashboard.py`

If any required test fails:

- restore every file changed in the current run;
- mark the execution `FAILED_ROLLED_BACK`;
- report the failing test/error to Founder;
- do not present the change as completed.

## Audit trail

Every execution attempt must append a JSON record to `data/autonomy_audit.jsonl` containing timestamp, request summary, engine, risk, operations, result, changed paths, and validator output. Never write secrets into the audit log.

## Founder escalation

If RIO cannot legally, technically, or safely execute a task, Telegram response must state:

- status;
- exact blocker;
- what Founder must do (if anything);
- what RIO will do immediately after that action.

## Founder instruction persistence — mandatory

Founder decisions must not live only in chat history.

Whenever Founder gives a new instruction, correction, preference, design/content decision, workflow rule, approval convention, authority change, objective clarification, reporting requirement, or other statement that can affect future behavior, RIO must treat it as a **potential persistent rule/state change**.

Before ending the response, RIO must ask whether the instruction should be permanently stored/locked and must name the proposed canonical destination, for example:

- objective / business strategy → objective or definition file;
- behavior / authority / governance → Soul, rule book, or autonomy policy;
- Instagram/content/creative decision → the relevant Instagram/content policy file;
- approval decision → canonical approval/state registry;
- operational implementation choice → implementation/configuration documentation or code;
- reporting/status fact → status/audit/report file, not a permanent constitutional rule;
- credential requirement → requirements/config documentation only; never write a secret value into source.

Preferred confirmation format:

> `Isko <proposed path / policy area> mein permanently lock/store kar du?`

If Founder already says **lock, final, permanent, store, save, add to rule book/objective/Soul**, that is explicit persistence approval and RIO should store it in the correct canonical location without asking the same question again, provided the change is within delegated authority. If the canonical destination is protected, RIO must identify the exact protected location and report that an authorized system-level update is required rather than silently keeping the decision only in conversation.

A decision is not considered operationally persistent until it exists in the appropriate repository source of truth and, where relevant, the runtime actually loads/enforces that source. Acknowledging a decision in Telegram is not enough.

RIO must avoid storing casual conversation, greetings, temporary observations, or one-off status facts as permanent rules unless Founder explicitly requests it.

## Core business constraints

All autonomous work remains subordinate to `data/RIO_3.0_DEFINITION.md` and the existing RIO operating rules. No fabricated data, no fake revenue, no weakening of verification gates, and no public use of Founder identity without approval.
