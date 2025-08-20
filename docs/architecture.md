# Architecture

This page presents the high-level system architecture and the Sigma Core module relationships in Mermaid format for inline rendering on the wiki.

## System Overview

```mermaid
graph LR
  %% Nodes
  User((User))
  EDP[External Data Providers]
  DB[(PostgreSQL DB)]
  OS[(Object Storage (S3/MinIO))]

  subgraph Sigmatiq_Sigma_Platform[Sigmatiq Sigma Platform]
    UI["Sigma UI"]
    API["Sigma API"]
    Workers["Sigma Workers"]
    Core["Sigma Core"]
  end

  %% Interactions
  User --> UI
  UI --> API
  API --> Core
  Workers --> Core
  Core --> DB
  Core --> OS
  EDP --> Core
  API --> DB
  API --> OS
  Workers --> DB
  Workers --> OS
```

## Sigma Core Modules

```mermaid
graph LR
  subgraph Sigma_Core[Sigma Core]
    Indicators
    Features
    Data
    CV
    Models
    Evaluation
    Backtest
    Policies
    Live
    Orchestration
    Registry
    Storage
    Common
  end

  Indicators -->|Uses Types| Common
  Features -->|Uses Registry| Indicators
  Features -->|Uses Types| Common
  Data -->|Uses Types| Common
  Data -->|Uses Builder| Features
  CV -->|Uses Types| Common
  Models -->|Uses Types| Common
  Models -->|Select Features| Features
  Evaluation -->|Uses Types| Common
  Backtest -->|Uses Types| Common
  Backtest -->|Uses Models| Models
  Backtest -->|Uses Splits| CV
  Backtest -->|Uses Policies| Policies
  Policies -->|Uses Types| Common
  Live -->|Uses Types| Common
  Live -->|Uses Models| Models
  Live -->|Uses Policies| Policies
  Orchestration -->|Uses Types| Common
  Orchestration -->|Triggers Dataset Builds| Data
  Orchestration -->|Triggers Training| Models
  Orchestration -->|Triggers Backtests| Backtest
  Registry -->|Uses Types| Common
  Registry -->|Uses DB/Object Store| Storage
  Storage -->|Uses Types| Common
```

Source PlantUML: see `docs/design_diagrams.puml` in the repository.

