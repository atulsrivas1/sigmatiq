Local Git Hooks (Optional)

Overview
- You can enable local hooks to nudge Critic Gate compliance before committing or pushing. These are advisory and opt-in.

Enable
```
git config core.hooksPath .githooks
```

Hooks Included
- `pre-commit`: Prints a reminder to run the Critic checklist for non-trivial changes.
- `commit-msg`: Requires a `Critic-Reviewed: yes|no` line if the commit touches API (`products/sigma-core/api/`) or migrations; blocks commit if missing.

Customize
- Edit the scripts in `.githooks/` to match your workflow. These run locally only and do not replace the CI Critic Gate.

