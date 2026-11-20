#!/usr/bin/env bash
# Called by a workflow step with `if: failure()`. Opens (or comments on) one issue
# titled "Wiki automation failed", so a broken job is never silent.
# Needs GH_TOKEN and the default GITHUB_* variables.
set -u
RUN_URL="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
TITLE="Wiki automation failed"
BODY="The **$GITHUB_WORKFLOW** workflow failed on $(date -u +%Y-%m-%d) (event: $GITHUB_EVENT_NAME, by @$GITHUB_ACTOR).

Details: $RUN_URL

Until this is fixed, the site or the weekly checks may not be updating. cc @JWinawer"
gh label create automation-failure --color B60205 --description "A wiki workflow failed" --repo "$GITHUB_REPOSITORY" 2>/dev/null || true
NUM=$(gh issue list --repo "$GITHUB_REPOSITORY" --label automation-failure --state open --json number -q '.[0].number' 2>/dev/null || true)
if [ -n "${NUM:-}" ]; then
  gh issue comment "$NUM" --repo "$GITHUB_REPOSITORY" --body "$BODY"
else
  gh issue create --repo "$GITHUB_REPOSITORY" --title "$TITLE" --label automation-failure --body "$BODY"
fi
