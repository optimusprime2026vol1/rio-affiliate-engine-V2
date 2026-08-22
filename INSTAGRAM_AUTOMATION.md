# RIO Instagram automation

## Locked status flow

`APPROVED` -> `POST_PENDING` -> `INSTAGRAM_POSTED`

If Meta rejects a post, the state becomes `FAILED_RETRY` with the real error
reason. Missing credentials and failed RIO validators are hard failures; the
GitHub Actions run must not appear successful when nothing was posted.

## Approval source

Founder approval is stored in `data/instagram_approval.json`. A commit that
changes this file automatically starts the Instagram publisher. Only offers
that are also `READY`, `ACTIVE`, `VERIFIED`, `IN_STOCK`, fresh enough, and
have a public social card can publish.

## Evidence and deduplication

- `data/instagram_run_status.json` contains the latest attempt and reason.
- `data/ig_published.json` contains confirmed Meta media IDs and permalinks.
- A confirmed offer is never posted twice.
- The CEO dashboard shows approval, pending, posted and failed counts.

## Secrets

The workflow reads `IG_USER_ID_RIO` and `IG_ACCESS_TOKEN_RIO` only from
GitHub Actions secrets. Secret values must never be committed to the repo.
