# UI Pages

This document provides a detailed description of the UI pages in the Sigma Lab application.

## Dashboard Page

*   **File**: `products/sigma-lab/ui/src/pages/Dashboard.tsx`
*   **Description**: The Dashboard page is the main landing page of the Sigma Lab application. It provides an overview of recent activities, system health, and a list of trading models.
*   **Components Used**:
    *   `RecentModels`
    *   `LastRuns`
    *   `QuickActions`
    *   `SystemHealth`
    *   `ControlsBar`
    *   `ModelsContainer`
    *   `Pagination`
    *   `ErrorBanner`
*   **Data Fetched**:
    *   Models data from `/models` API endpoint.
    *   Leaderboard data from `/leaderboard` API endpoint.
    *   Health data from `/health` API endpoint.
*   **Sections**:
    *   **Dashboard Section**: Displays `RecentModels`, `LastRuns`, `QuickActions`, and `SystemHealth` components.
    *   **Models Section**: Displays `ControlsBar`, `ModelsContainer`, and `Pagination` components for managing and viewing trading models.

## Models Page

*   **File**: `products/sigma-lab/ui/src/pages/Models.tsx`
*   **Description**: The Models page allows users to browse, search, filter, and manage their trading models. It displays models in a sortable table and provides quick actions for each model.
*   **Components Used**:
    *   `Link` (from `react-router-dom`)
    *   `Input` (for search)
    *   `Select` (for pack filter)
    *   `Button` (for actions)
*   **Data Fetched**:
    *   Models data from `/models` API endpoint.
*   **Sections**:
    *   **Page Header**: Displays the page title and a button to create a new model.
    *   **Filters Bar**: Contains input for searching models by ID and a dropdown for filtering by pack. Also displays the number of models shown.
    *   **Models Table**: A sortable table displaying `Model ID`, `Pack`, `Sharpe`, `Win Rate`, `Trades`, `Updated` date, and `Actions` for each model.
    *   **Model Statistics**: Displays overall statistics like total models, average Sharpe, and active packs.

## Model Create Page

*   **File**: `products/sigma-lab/ui/src/pages/ModelCreate.tsx`
*   **Description**: The Model Create page is a multi-step wizard that guides users through the process of creating a new trading model. Users can select a template, configure model details, and review their selections.
*   **Components Used**:
    *   `Link` (from `react-router-dom`)
    *   `Input`
    *   `Select`
    *   `Button`
    *   Custom components for template cards and risk options.
*   **Data Fetched**:
    *   Model creation API endpoint (`apiService.createModel`).
*   **Sections**:
    *   **Step 1: Choose a Template**: Users select a pre-configured model template. Displays template cards with details like name, description, pack, horizon, and cadence.
    *   **Step 2: Configure Your Model**: Users name their model and select a risk profile (Conservative, Balanced, Aggressive). Displays risk options with descriptions.
    *   **Step 3: Review & Create**: Users review their model configuration before creating the model. Displays a summary of selected template, model name, pack, and risk profile. Also outlines next steps after creation (Model Designer, Composer, Deploy).

## Model Designer Page

*   **File**: `products/sigma-lab/ui/src/pages/ModelDesigner.tsx`
*   **Description**: The Model Designer page is intended for configuring indicators and policy settings for a trading model. **Note**: This page is currently a placeholder and its full implementation is pending.
*   **Components Used**:
    *   None (currently a placeholder)
*   **Data Fetched**:
    *   None (currently a placeholder)
*   **Sections**:
    *   Currently displays a heading and a message indicating that the implementation is coming soon.

## Composer Page

*   **File**: `products/sigma-lab/ui/src/pages/Composer.tsx`
*   **Description**: The Composer page provides a multi-tab interface for the Build, Train, and Backtest (BTB) pipeline. Users can navigate between these stages to manage their model development workflow. **Note**: The content for each stage is currently a placeholder.
*   **Components Used**:
    *   `Link` (from `react-router-dom`)
    *   `Routes` (from `react-router-dom`)
    *   `Route` (from `react-router-dom`)
*   **Data Fetched**:
    *   None (currently a placeholder for the content of each tab)
*   **Sections**:
    *   **Page Header**: Displays the page title and description.
    *   **Composer Tabs**: Navigation links for `Build`, `Train`, and `Backtest` stages.
    *   **Composer Container**: Renders the content of the active tab. Each tab (`ComposerBuild`, `ComposerTrain`, `ComposerBacktest`) currently displays a placeholder message.

## Sweeps Page

*   **File**: `products/sigma-lab/ui/src/pages/Sweeps.tsx`
*   **Description**: The Sweeps page allows users to configure and run backtest sweeps to find optimal parameters for their trading models. It provides options for defining risk profiles and sweep types. **Note**: The what-if analysis and results sections are currently placeholders.
*   **Components Used**:
    *   `Link` (from `react-router-dom`)
    *   `Input`
    *   `Select`
    *   `Button`
*   **Data Fetched**:
    *   None (currently a placeholder)
*   **Sections**:
    *   **Page Header**: Displays the page title, description, and a button to run a sweep.
    *   **Sweep Configuration**: Allows users to select a risk profile (Conservative, Balanced, Aggressive) and a sweep type (Thresholds, Allowed Hours, Top Percentage).
    *   **What-if Analysis**: A placeholder section for future implementation of what-if analysis.
    *   **Sweep Results**: A placeholder section where the results of the sweep will be displayed, including gate badges, performance metrics, and export options.

## Leaderboard Page

*   **File**: `products/sigma-lab/ui/src/pages/Leaderboard.tsx`
*   **Description**: The Leaderboard page allows users to compare and select backtest results across different models. It provides filtering options by pack, risk profile, and gate status, along with batch actions for training and export.
*   **Components Used**:
    *   `ErrorBanner`
    *   `Link` (from `react-router-dom`)
    *   `Input`
    *   `Select`
    *   `Button`
*   **Data Fetched**:
    *   Leaderboard data from `/leaderboard` API endpoint.
*   **Sections**:
    *   **Page Header**: Displays the page title, description, and action buttons for batch training and CSV export.
    *   **Filters**: Allows filtering by `Pack`, `Risk Profile`, and `Pass Gate Only` checkbox.
    *   **Leaderboard Table**: A sortable table displaying `Rank`, `Model ID`, `Pack`, `Gate` status, `Sharpe`, `Win Rate`, `Trades`, `Max DD`, `Cum Return`, and `Actions` for each entry. Includes checkboxes for batch selection.
    *   **Performance Summary**: Displays aggregated performance statistics like average Sharpe, average win rate, total trades, and pass rate.

## Signals Page

*   **File**: `products/sigma-lab/ui/src/pages/Signals.tsx`
*   **Description**: The Signals page provides a multi-tab interface for monitoring and analyzing trading signals. Users can view live signals, historical logs, and performance analytics. **Note**: The content for each tab is currently a placeholder.
*   **Components Used**:
    *   `Link` (from `react-router-dom`)
    *   `Routes` (from `react-router-dom`)
    *   `Route` (from `react-router-dom`)
*   **Data Fetched**:
    *   None (currently a placeholder for the content of each tab)
*   **Sections**:
    *   **Page Header**: Displays the page title and description.
    *   **Signals Tabs**: Navigation links for `Live`, `Log`, and `Analytics` stages.
    *   **Signals Container**: Renders the content of the active tab. Each tab (`SignalsLive`, `SignalsLog`, `SignalsAnalytics`) currently displays a placeholder message.

## Health Page

*   **File**: `products/sigma-lab/ui/src/pages/Health.tsx`
*   **Description**: The Health page provides a comprehensive overview of the system's operational status and diagnostics. It fetches real-time health data from the API and presents it in a clear, organized manner.
*   **Components Used**:
    *   None explicitly listed, but uses basic HTML elements for layout and display.
*   **Data Fetched**:
    *   Health data from `/health` API endpoint.
*   **Sections**:
    *   **Page Header**: Displays the page title and description.
    *   **Overall Status**: Indicates whether all systems are operational or if issues are detected.
    *   **Service Status Cards**: Displays individual cards for `Service Status`, `Version`, `Database`, and `FastAPI` status.
    *   **Health Check Details**: Shows the raw JSON response from the health API for detailed diagnostics.

## Options Overlay Page

*   **File**: `products/sigma-lab/ui/src/pages/Overlay.tsx`
*   **Description**: The Options Overlay page is designed to help users convert equity signals into options strategies. It highlights key features like strike selection, expiration optimization, and risk management for options trading. **Note**: This page is currently a placeholder and its full implementation is pending.
*   **Components Used**:
    *   None explicitly listed, but uses basic HTML elements for layout and display.
*   **Data Fetched**:
    *   None (currently a placeholder)
*   **Sections**:
    *   **Page Header**: Displays the page title and description.
    *   **Options Overlay Conversion**: Describes the process of transforming equity signals into options strategies.
    *   **Key Features**: Highlights `Strike Selection`, `Expiration Optimization`, and `Risk Management` for options.
    *   **Interface Placeholder**: A section indicating that the options overlay interface is coming soon.

## Components Showcase Page

*   **File**: `products/sigma-lab/ui/src/pages/ComponentShowcase.tsx`
*   **Description**: This page serves as a comprehensive showcase and testing ground for nearly all UI components implemented in the Sigmatiq application. It demonstrates various component types, their variants, sizes, and interactive behaviors.
*   **Components Used**:
    *   `Icon`, `Logo`
    *   `Card`, `CardHeader`, `CardIcon`, `CardHeaderInfo`, `CardBadge`, `CardContent`, `CardStats`, `StatItem`, `CardChart`, `CardMeta`, `CardActions`, `CardButton`
    *   `Button`, `IconButton`
    *   `Badge`, `StatusBadge`, `RiskBadge`, `PackBadge`, `GateBadge`, `TrustBadge`
    *   `Tooltip`
    *   `ProgressBar`, `CapacityBar`
    *   `Input`, `Textarea`, `SearchInput`, `Select`, `FilterSelect`, `Toggle`
    *   `Tabs`, `TabPanel`, `PeriodSelector`, `Pagination`
    *   `DataGrid`
    *   `Alert`, `Toast`, `EmptyState`, `ErrorState`, `ErrorBanner`
*   **Data Fetched**:
    *   None (uses hardcoded sample data for demonstration purposes).
*   **Sections**:
    *   **Core Components**: Demonstrates `Logo` and various `Icon` types.
    *   **Buttons**: Showcases `Button` variants, sizes, and `IconButton`.
    *   **Badges**: Displays `Badge` variants, `StatusBadge`, `RiskBadge`, and `PackBadge`.
    *   **Gate & Trust Badges**: Demonstrates `GateBadge` and `TrustBadge` components.
    *   **Form Components**: Showcases `Input`, `Textarea`, `SearchInput`, `Select`, `FilterSelect`, and `Toggle`.
    *   **Navigation Components**: Demonstrates `Tabs`, `PeriodSelector`, and `Pagination`.
    *   **Progress Bars**: Displays `ProgressBar` and `CapacityBar`.
    *   **Cards**: Showcases the `Card` component and its various sub-components for structuring content.
    *   **Data Grid**: Demonstrates the `DataGrid` component in both card and row views.
    *   **Tooltips**: Illustrates `Tooltip` functionality with different placements.
    *   **Feedback Components**: Displays `Alert`, `Toast`, `ErrorBanner`.
    *   **Empty & Error States**: Showcases `EmptyState` and `ErrorState` components with different variants and content.

## Components Demo Page

*   **File**: `products/sigma-lab/ui/src/pages/ComponentsDemo.tsx`
*   **Description**: This page serves as a demonstration and testing ground for various UI components used throughout the Sigma Lab application. It showcases how different components are rendered and interact.
*   **Components Used**:
    *   `GateBadge`
    *   `HealthTile`, `HealthTiles`
    *   `TemplateCard`, `TemplatesGrid`
    *   `FiltersRow`, `SearchInput`, `CompactSelect`, `FilterChip`
    *   `SignalsTable`, `ModelIdLink`, `TickerBadge`, `SidePill`, `ConfidenceBadge`, `StatusBadge`
    *   `JobsTable`, `JobStatusPill`
    *   `ChartHeader`, `ChartContainer`
    *   `KPIStat`
    *   `Sparkline`
*   **Data Fetched**:
    *   None (uses hardcoded sample data for demonstration purposes).
*   **Sections**:
    *   **Trust Gate + Health Tiles**: Demonstrates `GateBadge`, `HealthTile`, and `HealthTiles` components.
    *   **Template Cards**: Demonstrates `TemplateCard` and `TemplatesGrid` components.
    *   **Filters Row**: Demonstrates `FiltersRow`, `SearchInput`, `CompactSelect`, and `FilterChip` components.
    *   **Signals Table**: Demonstrates `SignalsTable` and related signal-specific badges (`ModelIdLink`, `TickerBadge`, `SidePill`, `ConfidenceBadge`, `StatusBadge`).
    *   **Jobs Table**: Demonstrates `JobsTable` and `JobStatusPill` components.
    *   **Charts**: Demonstrates `ChartHeader`, `ChartContainer`, `KPIStat`, and `Sparkline` components.
