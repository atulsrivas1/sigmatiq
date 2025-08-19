# Rebranding to Sigmatiq / Sigmatiq.ai — TODOs

Scope: Replace public-facing mentions of “Sigmatiq” with “Sigmatiq” and update visual assets/domains.

- Code/UI strings
  - FastAPI title updated to “Sigmatiq Edge API” (done).
  - Review any UI headers/titles in preview HTML under `docs/ui/branding/` and change copy to “Sigmatiq Edge”.

- Docs
  - Update headings and body text: `Sigmatiq -> Sigmatiq` (Release Summary updated; README updated).
  - Grep docs for remaining occurrences and replace in batches; watch for file encodings.
  - Add canonical domain references: `sigmatiq.ai` (where appropriate) instead of placeholders.

- Branding assets
  - If logo files are brand-specific, replace assets under `docs/ui/branding/` (favicons, badges) with Sigmatiq-branded versions.
  - Token comments (`/* Sigmatiq Edge – ... */`) can be updated as part of sweep.

- URLs & config
  - If any hard-coded URLs exist (CORS, redirects), update to `sigmatiq.ai` when deploying.
  - README badges, links, and examples to reflect new domain when live.

- Repo & package names (optional / longer-term)
  - Consider renaming top-level repo folder to `Sigmatiq-Edge` in Git hosting to match branding (no code change needed).
  - Python package/module names remain unchanged unless there is a policy to rename fully.

- Verification
  - Run a global search for `Sigmatiq` across the workspace; fix stragglers.
  - Rebuild docs/previews where HTML includes titles with brand.
