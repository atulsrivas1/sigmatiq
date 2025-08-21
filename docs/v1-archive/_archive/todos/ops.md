Operations & Observability

Completed
- .env.example added; API loads env early.
- Strict caching policy: only historical data cached; never cache today.
- Policy validation endpoint and Make target.

Pending
- Replace prints with logging; env-configured levels.
- Optional: DB SSL support and `/healthz` DB connectivity check.
