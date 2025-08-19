
# Paper Trader & Alerts — High‑Level Design (HLD)
*Generated: 2025-08-15 20:56 UTC*

**Objectives**
- Convert model signals into **paper orders/fills** deterministically.
- Support **multi‑model** netting/allocation and full **attribution**.
- Emit **alerts** for Signal → Order → Fill → Stop/Target → Flat.
- Keep everything **reproducible** via pack‑versioned configs and fingerprints.

**Architecture**
Live Signal Runtime gains a **Paper Broker** + **Fill Engine**. Flow:
`Model → Signal → Policy → Allocator/Netter → Paper Broker → Fill Engine → Positions/P&L` (alerts at each step).

**Components**
1. Signal Source (rule‑based or ML)
2. Policy Engine (risk/execution; **brackets** support)
3. Allocator/Netter (capital rules, de‑dup/netting across models)
4. Paper Broker (orders/positions/portfolio endpoints)
5. Fill Engine (next_bar_open, moc, limit_cross; slippage; VP caps; calendar)
6. State Store (DB tables for accounts/orders/fills/positions/equity/alerts)
7. Alerts Dispatcher (SSE stream + paged pull)
8. UI Panels (Blotter, Positions/P&L, Alerts, Attribution)

**Stops/Targets**
- **Rule‑based:** ATR multiples (e.g., 1.2x stop, 2.0x target), optional time stop.
- **ML‑based:** quantiles of forward drawdown/run‑up → bracket levels.

**Non‑Goals (MVP)**
- Real broker connectivity; complex microstructure/queue modeling; cross‑asset margin netting.

**Governance**
Pack assets for paper accounts/fill models/policies; run fingerprints; parity with backtests.
