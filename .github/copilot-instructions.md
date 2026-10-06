# HPE Redfish-Style Lab Service — agent rules

Always-on rules for this repository. Procedures live in `.github/skills/`;
this file is only the things that are true for every task.

## The app

FastAPI service simulating a Redfish-style management API.
- `app/main.py` — all routes
- `tests/unit/` — pytest, uses FastAPI TestClient
- `tests/playwright/` — Playwright **API** tests via the `request` fixture (no browser)
- `jira/` — ticket text, usable offline if Atlassian MCP is unauthenticated

## How to run things

```
pytest -q                     unit / API tests
npm run test:playwright       Playwright API tests (auto-starts uvicorn)
docker compose up -d --build  packaged run on :8000
```

Playwright starts the server itself unless `BASE_URL` is set. Don't start
uvicorn separately first — the port collision looks like a test failure.

## Conventions

- Branch: `jira/<TICKET-KEY>-<short-slug>`
- Commit subject starts with the ticket key: `HPELAB-102: reject read-only SerialNumber`
- Redfish errors use the `@Message.ExtendedInfo` shape already in `app/main.py`
- Keep the diff minimal. No drive-by refactors, no formatting-only changes.

## Rules that do not bend

1. **Never weaken a test to get green.** Not by changing an assertion, not by
   skipping, not by deleting. A test that looks wrong is a finding to report —
   stop and say which assertion and why.
2. **Never merge a PR.** Open it as a draft and stop. A human merges.
3. **Never deploy from the IDE.** Deployment runs only through
   `.github/workflows/deploy-lab.yml` after its environment approval.
4. **Stay inside the ticket.** If the work needs a file the plan didn't name,
   stop and say so rather than widening silently.
5. **Don't invent business behaviour.** If the acceptance criteria don't settle
   a product question, ask — don't pick an answer.

6. **Never read, retrieve or use a credential.** Not from the credential
   manager, environment variables, `.git-credentials`, `.netrc`, or any
   other store. If `git push` or an API call fails for auth, stop and report
   it — that failure is a boundary, not an obstacle to solve. Finding another
   route to the same action is the thing this rule forbids.
## Evidence

Every PR body follows `.github/PULL_REQUEST_TEMPLATE.md`: the ticket key, what
changed, the RED output before the fix and the GREEN output after, and any risk
or assumption. CI re-runs everything independently — your local result is a
claim until the PR checks agree with it.
