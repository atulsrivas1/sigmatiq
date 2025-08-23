# Editorial Workflow — Author, Review, Publish

States
- draft → in_review → published (latest published is default in API).

Roles
- Author: writes/updates content using templates.
- Reviewer: checks accuracy, clarity, evidence, and accessibility.
- Publisher: approves changes, version bumps, and publishes.

Templates
- One template per entity type (Indicator, Set, Strategy). Required sections:
  - Indicator: What it measures, How to read, Typical ranges, Parameters, Best/Worst, Example condition, Caveats, QA checks, Media.
  - Set: Purpose, Components & roles, Signal logic, Redundancy/conflict notes, Timeframe alignment, Best/Worst, Anti-patterns, Example rule, Media.
  - Strategy: Objective, Entry/Exit, Risk/Sizing, Execution policy, How it behaves, How to evaluate, Typical ranges, Compliance note, Media.

Style Guide
- Plain English; define jargon; limit to 4–6 bullets per section.
- Show examples before theory; include one visual per explainer minimum.
- Accessibility: alt text and captions for all media.

Quality Gates
- Completeness checklist per template.
- Readability threshold; link at least one glossary term.
- Evidence: 1+ external reference or internal report; fill “Evidence summary”.

Versioning
- Bump `version` when substantive content changes; include change notes.
- Track `lineage` with `code_version`, `git_sha`, and source docs.

Assistant Prep (Future)
- Add concise `assistant_hints` bullets (3–5) per explainer with the most important takeaways.
- Include one short, concrete example users can try (kept in sync with examples/ and workflows).
- Keep “how to read” to 2–3 short bullets for beginner mode; reserve depth for long_description.
