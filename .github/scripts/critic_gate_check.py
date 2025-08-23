#!/usr/bin/env python3
import json, os, sys

REQUIRED_SECTIONS = [
    "Summary", "Critic Report", "Risks to novices", "Safety gaps",
    "Complexity increases", "Defaults & scope", "API & contracts",
    "Data/migrations", "Errors & DX", "Tests & Postman", "Status", "Checklist"
]

def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        print("::warning::GITHUB_EVENT_PATH not set; skipping Critic Gate check")
        return 0
    with open(event_path, 'r', encoding='utf-8') as f:
        evt = json.load(f)
    pr = evt.get('pull_request') or {}
    body = pr.get('body') or ''
    if not body.strip():
        print("::error::PR description is empty. Please fill the PR template and include the Critic Report.")
        return 1
    missing = []
    text = body.lower()
    for s in REQUIRED_SECTIONS:
        if s.lower() not in text:
            missing.append(s)
    if missing:
        print(f"::error::Critic Gate: Missing required sections in PR body: {', '.join(missing)}")
        print("Ensure you used the PR template and completed the Critic Report.")
        return 1
    # Basic sanity: must state Blockers line
    if 'blockers:' not in text:
        print("::error::Critic Gate: 'Blockers:' line is required in Status section.")
        return 1
    # Enforce that the Critic pass checklist item is checked
    if '[x] critic pass completed' not in text and '[x]  critic pass completed' not in text:
        print("::error::Critic Gate: Please check the 'Critic pass completed' item in the checklist (change [ ] to [x]).")
        return 1
    print("Critic Gate check passed: required sections present.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
