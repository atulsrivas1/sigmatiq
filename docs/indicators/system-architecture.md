# System Architecture — Single Indicator

```mermaid
graph LR
  subgraph Clients
    UI[Web UI]
    WS[WebSocket]
  end

  subgraph API[Sigma Lab API]
    IR[Indicators Router]
    CR[Compute Service]
    QC[QA/Validation]
  end

  subgraph Core[Sigma Core]
    REG[Indicators Registry]
    ENG[Compute Engine]
    CACHE[Feature Cache]
  end

  DB[(Postgres)]
  OBJ[(Artifacts Store)]
  MKT[(Market Data)]

  UI -->|REST| IR
  WS -->|Subscribe| IR
  IR --> CR
  CR --> ENG
  ENG --> CACHE
  ENG --> QC
  CR --> DB
  CACHE --> OBJ
  CR --> MKT
  QC --> DB
```

Notes
- Focuses on computing a single indicator per request or stream; combinations are out of scope.
- Registry validates params and exposes compute callable and metadata.
- Engine performs vectorized calculation and incremental updates; cache deduplicates repeated requests.
- QA runs basic checks (NaN, alignment) and returns warnings.
