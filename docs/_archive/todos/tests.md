Testing – Plan (No Mocks Policy)

Completed
- Defined no-mocks policy and documented expectations.

Pending
- Add shape-only API smoke tests (no external calls).
- Opt-in live tests driven by env (e.g., `LIVE_POLYGON_TEST=1`) that hit Polygon for daily/hourly/snapshot.
- End-to-end checks running on actual built matrices (pipeline output), not mock data.
