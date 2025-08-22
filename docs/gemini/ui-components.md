# UI Components

This document provides a detailed description of the UI components used in the Sigma Lab application.

## Common Components

These components are used throughout the application.

### StatusBadge

*   **File**: `products/sigma-lab/ui/srcsrc/components/common/StatusBadge.tsx`
*   **Description**: A badge component that displays a status message with a colored background.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `variant` | `success` \| `warning` \| `error` \| `info` \| `neutral` | The variant of the badge. Defaults to `neutral`. |
| `children` | `React.ReactNode` | The content of the badge. |

*   **Usage**:

```tsx
import { StatusBadge } from './StatusBadge';

<StatusBadge variant="success">Active</StatusBadge>
```

### Sparkline

*   **File**: `products/sigma-lab/ui/src/components/common/Sparkline.tsx`
*   **Description**: A component that displays a sparkline chart.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `points` | string | A string of points for the sparkline. Defaults to a sample set of points. |
| `stroke` | string | The color of the sparkline. Defaults to `var(--sigmatiq-bright-teal)`. |
| `fill` | string | The fill color of the sparkline. Defaults to `none`. |
| `height` | number | The height of the sparkline. Defaults to `28`. |

*   **Usage**:

```tsx
import { Sparkline } from './Sparkline';

<Sparkline points="0,20 20,10 40,16 60,12 80,9 100,7 120,11" />
```

### ModelIdLink

*   **File**: `products/sigma-lab/ui/src/components/common/ModelIdLink.tsx`
*   **Description**: A component that displays a link to a model's designer page.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `id` | string | The ID of the model. |

*   **Usage**:

```tsx
import { ModelIdLink } from './ModelIdLink';

<ModelIdLink id="spy_opt_0dte_hourly" />
```

### KPIStat

*   **File**: `products/sigma-lab/ui/src/components/common/KPIStat.tsx`
*   **Description**: A component that displays a key performance indicator (KPI) with a label, value, and optional trend indicator.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `label` | string | The label for the KPI. |
| `value` | `React.ReactNode` | The value of the KPI. |
| `trend` | `positive` \| `negative` | The trend of the KPI. This will color the value green for positive and red for negative. |

*   **Usage**:

```tsx
import { KPIStat } from './KPIStat';

<KPIStat label="Sharpe Ratio" value="1.2" trend="positive" />
```

### FreshIcon

*   **File**: `products/sigma-lab/ui/src/components/common/FreshIcon.tsx`
*   **Description**: A component that displays an SVG icon.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `name` | `IconName` | The name of the icon to display. See the `IconName` type in the source file for a list of available icons. |
| `size` | number | The size of the icon in pixels. Defaults to `18`. |
| `className` | string | An optional CSS class to apply to the icon. |
| `stroke` | string | The stroke color of the icon. Defaults to `currentColor`. |
| `fill` | string | The fill color of the icon. Defaults to `none`. |

*   **Usage**:

```tsx
import { FreshIcon } from './FreshIcon';

<FreshIcon name="grid" />
```

### ErrorBanner

*   **File**: `products/sigma-lab/ui/src/components/common/ErrorBanner.tsx`
*   **Description**: A component that displays an error message in a banner.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `message` | string | The error message to display. |

*   **Usage**:

```tsx
import { ErrorBanner } from './ErrorBanner';

<ErrorBanner message="Something went wrong." />
```

### DocLinkCard

*   **File**: `products/sigma-lab/ui/src/components/common/DocLinkCard.tsx`
*   **Description**: A card component that links to a documentation page.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `href` | string | The URL of the documentation page. Defaults to `#`. |
| `icon` | `React.ReactNode` | An optional icon to display on the card. |
| `title` | string | The title of the documentation page. |
| `description` | string | An optional description of the documentation page. |

*   **Usage**:

```tsx
import { DocLinkCard } from './DocLinkCard';

<DocLinkCard href="/docs/getting-started" title="Getting Started" description="A guide for new users." />
```

## Dashboard Components

These components are used on the Dashboard page.

### DashboardCard

*   **File**: `products/sigma-lab/ui/src/components/dashboard/DashboardCard.tsx`
*   **Description**: A card component that displays a title and content on the dashboard.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `title` | string | The title of the card. |
| `children` | `React.ReactNode` | The content of the card. |

*   **Usage**:

```tsx
import { DashboardCard } from './DashboardCard';

<DashboardCard title="Recent Activity">
  <p>Some recent activity...</p>
</DashboardCard>
```

### SystemHealth

*   **File**: `products/sigma-lab/ui/src/components/dashboard/SystemHealth.tsx`
*   **Description**: A component that displays the health of the system.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `items` | `Item[]` | An array of health items to display. See the `Item` type in the source file for the structure of each item. |

*   **Usage**:

```tsx
import { SystemHealth } from './SystemHealth';

const healthItems = [
  {
    label: 'API',
    value: 'Online',
    className: 'ok',
    color: 'var(--status-success)',
    icon: 'shield'
  },
  {
    label: 'Database',
    value: 'Online',
    className: 'ok',
    color: 'var(--status-success)',
    icon: 'database'
  },
  {
    label: 'Polygon',
    value: 'Online',
    className: 'ok',
    color: 'var(--status-success)',
    icon: 'globe'
  }
];

<SystemHealth items={healthItems} />
```

### RecentModels

*   **File**: `products/sigma-lab/ui/src/components/dashboard/RecentModels.tsx`
*   **Description**: A component that displays a list of recently updated models.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `items` | `Item[]` | An array of model items to display. See the component's source for the structure of each item. |

*   **Usage**:

```tsx
import { RecentModels } from './RecentModels';

const recentModels = [
  {
    id: 'spy_opt_0dte_hourly',
    pack: 'zerosigma',
    color: 'var(--sigmatiq-bright-teal)',
    updatedAt: '2 hours ago'
  }
];

<RecentModels items={recentModels} />
```

### QuickActions

*   **File**: `products/sigma-lab/ui/src/components/dashboard/QuickActions.tsx`
*   **Description**: A component that displays a list of quick actions on the dashboard.
*   **Props**: None

*   **Usage**:

```tsx
import { QuickActions } from './QuickActions';

<QuickActions />
```

### LastRuns

*   **File**: `products/sigma-lab/ui/src/components/dashboard/LastRuns.tsx`
*   **Description**: A component that displays a list of the last runs.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `runs` | `Run[]` | An array of run objects to display. See the `Run` type in the source file for the structure of each item. |

*   **Usage**:

```tsx
import { LastRuns } from './LastRuns';

const lastRuns = [
  {
    name: 'spy_opt_0dte_hourly',
    sub: 'Backtest',
    type: 'success'
  },
  {
    name: 'aapl_eq_swing_daily',
    sub: 'Training',
    type: 'running'
  },
  {
    name: 'tsla_opt_0dte_hourly',
    sub: 'Backtest',
    type: 'failed'
  }
];

<LastRuns runs={lastRuns} />
```

## Data Display Components

These components are used to display data in a structured way.

### DataGrid

*   **File**: `products/sigma-lab/ui/src/components/data-display/DataGrid.tsx`
*   **Description**: A versatile component for displaying data in a grid or card view. It supports searching, filtering, sorting, and pagination.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `data` | `T[]` | An array of data items to display. |
| `columns` | `DataGridColumn[]` | An array of column definitions for the grid view. |
| `viewMode` | `card` \| `row` | The view mode to display. If not provided, the component will manage its own view state. |
| `defaultView` | `card` \| `row` | The default view mode to display. Defaults to `card`. |
| `renderCard` | `(item: T, index: number) => ReactNode` | A function to render a single item in card view. |
| `renderRow` | `(item: T, index: number) => ReactNode` | A function to render a single item in row view. |
| `showSearch` | boolean | Whether to show the search input. Defaults to `true`. |
| `showFilters` | boolean | Whether to show the filter dropdowns. Defaults to `true`. |
| `showViewToggle` | boolean | Whether to show the view mode toggle. Defaults to `true`. |
| `showPagination` | boolean | Whether to show the pagination controls. Defaults to `true`. |
| `showItemsPerPage` | boolean | Whether to show the items per page dropdown. Defaults to `true`. |
| `showSorting` | boolean | Whether to show the sorting dropdown. Defaults to `true`. |
| `searchPlaceholder` | string | The placeholder text for the search input. Defaults to `Search...`. |
| `onSearch` | `(query: string) => void` | A callback function that is called when the search query changes. |
| `filters` | `Filter[]` | An array of filter definitions. |
| `sortOptions` | `SortOption[]` | An array of sorting options. |
| `defaultSort` | string | The default sort option. |
| `onSort` | `(sortBy: string) => void` | A callback function that is called when the sort option changes. |
| `itemsPerPage` | number | The number of items to display per page. Defaults to `12`. |
| `itemsPerPageOptions` | `number[]` | An array of options for the items per page dropdown. Defaults to `[12, 24, 48]`. |
| `currentPage` | number | The current page number. Defaults to `1`. |
| `totalItems` | number | The total number of items. If not provided, it will be calculated from the `data` prop. |
| `onPageChange` | `(page: number) => void` | A callback function that is called when the page number changes. |
| `onItemsPerPageChange` | `(items: number) => void` | A callback function that is called when the number of items per page changes. |
| `loading` | boolean | Whether the grid is in a loading state. Defaults to `false`. |
| `emptyMessage` | string | The message to display when there is no data. Defaults to `No items found`. |
| `className` | string | An optional CSS class to apply to the container. |
| `gridClassName` | string | An optional CSS class to apply to the grid. |
| `cardClassName` | string | An optional CSS class to apply to the cards. |
| `rowClassName` | string | An optional CSS class to apply to the rows. |

*   **Usage**:

```tsx
import { DataGrid } from './DataGrid';

const data = [
  { id: 1, name: 'Item 1' },
  { id: 2, name: 'Item 2' }
];

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'name', label: 'Name' }
];

<DataGrid data={data} columns={columns} />
```

## Feedback Components

These components are used to provide feedback to the user.

### Alert

*   **File**: `products/sigma-lab/ui/src/components/feedback/Alert.tsx`
*   **Description**: A component that displays an alert message.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `children` | `React.ReactNode` | The content of the alert. |
| `variant` | `success` \| `warning` \| `error` \| `info` | The variant of the alert. Defaults to `info`. |
| `title` | string | An optional title for the alert. |
| `dismissible` | boolean | Whether the alert can be dismissed. Defaults to `false`. |
| `onDismiss` | `() => void` | A callback function that is called when the alert is dismissed. |
| `icon` | boolean | Whether to display an icon in the alert. Defaults to `true`. |
| `className` | string | An optional CSS class to apply to the alert. |

*   **Usage**:

```tsx
import { Alert } from './Alert';

<Alert variant="success" title="Success">
  This is a success message.
</Alert>
```

### Toast

*   **File**: `products/sigma-lab/ui/src/components/feedback/Alert.tsx`
*   **Description**: A component that displays a temporary notification.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `children` | `React.ReactNode` | The content of the toast. |
| `variant` | `success` \| `warning` \| `error` \| `info` | The variant of the toast. Defaults to `info`. |
| `title` | string | An optional title for the toast. |
| `duration` | number | The duration in milliseconds to display the toast. Defaults to `5000`. |
| `onDismiss` | `() => void` | A callback function that is called when the toast is dismissed. |
| `className` | string | An optional CSS class to apply to the toast. |

*   **Usage**:

```tsx
import { Toast } from './Toast';

<Toast variant="success" title="Success" onDismiss={() => {}}>
  This is a success message.
</Toast>
```

### EmptyState

*   **File**: `products/sigma-lab/ui/src/components/feedback/EmptyState.tsx`
*   **Description**: A component that displays a message when there is no data to show.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `variant` | `no-data` \| `no-results` \| `first-time` \| `error` \| `custom` | The variant of the empty state. Defaults to `no-data`. |
| `icon` | `React.ReactNode` | An optional icon to display. |
| `title` | string | The title of the empty state message. |
| `message` | string | An optional message to display. |
| `action` | `React.ReactNode` | An optional action to display, such as a button. |
| `className` | string | An optional CSS class to apply to the component. |

*   **Usage**:

```tsx
import { EmptyState } from './EmptyState';

<EmptyState variant="no-data" title="No Data" message="There is no data to display." />
```

### ErrorState

*   **File**: `products/sigma-lab/ui/src/components/feedback/ErrorState.tsx`
*   **Description**: A component that displays an error message when something goes wrong.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `variant` | `connection` \| `validation` \| `server` \| `custom` | The variant of the error state. Defaults to `server`. |
| `title` | string | The title of the error message. |
| `message` | string | An optional message to display. |
| `details` | string \| `string[]` | Optional details about the error. Can be a string or an array of strings. |
| `actions` | `React.ReactNode` | Optional actions to display, such as a button to retry the action. |
| `className` | string | An optional CSS class to apply to the component. |

*   **Usage**:

```tsx
import { ErrorState } from './ErrorState';

<ErrorState variant="server" title="Server Error" message="Could not connect to the server." />
```

### ErrorBanner

*   **File**: `products/sigma-lab/ui/src/components/feedback/ErrorState.tsx`
*   **Description**: A component that displays an error message in a banner.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `variant` | `critical` \| `warning` \| `info` | The variant of the error banner. Defaults to `critical`. |
| `message` | string | The error message to display. |
| `dismissible` | boolean | Whether the banner can be dismissed. Defaults to `true`. |
| `onDismiss` | `() => void` | A callback function that is called when the banner is dismissed. |
| `className` | string | An optional CSS class to apply to the banner. |

*   **Usage**:

```tsx
import { ErrorBanner } from './ErrorState';

<ErrorBanner variant="critical" message="This is a critical error." />
```

## Filter Components

These components are used for filtering and searching data.

### SearchInput

*   **File**: `products/sigma-lab/ui/src/components/filters/SearchInput.tsx`
*   **Description**: A component that displays a search input with a search icon.
*   **Props**: This component accepts all the standard props for an HTML `input` element.

*   **Usage**:

```tsx
import { SearchInput } from './SearchInput';

<SearchInput placeholder="Search..." />
```

### FiltersRow

*   **File**: `products/sigma-lab/ui/src/components/filters/FiltersRow.tsx`
*   **Description**: A component that displays a row of filters.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `left` | `React.ReactNode` | The content to display on the left side of the row. |
| `children` | `React.ReactNode` | The content to display in the center of the row. |
| `right` | `React.ReactNode` | The content to display on the right side of the row. |

*   **Usage**:

```tsx
import { FiltersRow } from './FiltersRow';

<FiltersRow left={<div>Left</div>} right={<div>Right</div>}>
  <div>Center</div>
</FiltersRow>
```

### FilterChip

*   **File**: `products/sigma-lab/ui/src/components/filters/FilterChip.tsx`
*   **Description**: A component that displays a filter chip.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `active` | boolean | Whether the chip is active. |
| `onClick` | `() => void` | A callback function that is called when the chip is clicked. |
| `children` | `React.ReactNode` | The content of the chip. |

*   **Usage**:

```tsx
import { FilterChip } from './FilterChip';

<FilterChip active onClick={() => {}}>
  My Filter
</FilterChip>
```

### CompactSelect

*   **File**: `products/sigma-lab/ui/src/components/filters/CompactSelect.tsx`
*   **Description**: A compact select component.
*   **Props**: This component accepts all the standard props for an HTML `select` element.

*   **Usage**:

```tsx
import { CompactSelect } from './CompactSelect';

<CompactSelect>
  <option value="1">Option 1</option>
  <option value="2">Option 2</option>
</CompactSelect>
```

## Form Components

These components are used for creating forms.

### Input

*   **File**: `products/sigma-lab/ui/src/components/forms/Input.tsx`
*   **Description**: A component that displays a text input.
*   **Props**: This component accepts all the standard props for an HTML `input` element, plus the following:

| Name | Type | Description |
| --- | --- | --- |
| `label` | string | The label for the input. |
| `error` | string | An error message to display. |
| `helpText` | string | Help text to display below the input. |
| `size` | `sm` \| `md` \| `lg` | The size of the input. Defaults to `md`. |
| `variant` | `default` \| `search` | The variant of the input. Defaults to `default`. |
| `leftIcon` | string | The name of an icon to display on the left side of the input. |
| `rightIcon` | string | The name of an icon to display on the right side of the input. |
| `onRightIconClick` | `() => void` | A callback function that is called when the right icon is clicked. |
| `fullWidth` | boolean | Whether the input should take up the full width of its container. Defaults to `false`. |

*   **Usage**:

```tsx
import { Input } from './Input';

<Input label="My Input" placeholder="Enter some text..." />
```

### Textarea

*   **File**: `products/sigma-lab/ui/src/components/forms/Input.tsx`
*   **Description**: A component that displays a textarea.
*   **Props**: This component accepts all the standard props for an HTML `textarea` element, plus the following:

| Name | Type | Description |
| --- | --- | --- |
| `label` | string | The label for the textarea. |
| `error` | string | An error message to display. |
| `helpText` | string | Help text to display below the textarea. |
| `resize` | `none` \| `both` \| `horizontal` \| `vertical` | The resize behavior of the textarea. Defaults to `vertical`. |
| `fullWidth` | boolean | Whether the textarea should take up the full width of its container. Defaults to `false`. |

*   **Usage**:

```tsx
import { Textarea } from './Input';

<Textarea label="My Textarea" placeholder="Enter some text..." />
```

### SearchInput

*   **File**: `products/sigma-lab/ui/src/components/forms/Input.tsx`
*   **Description**: A specialized input component for search queries.
*   **Props**: This component accepts all the props for the `Input` component, plus the following:

| Name | Type | Description |
| --- | --- | --- |
| `onClear` | `() => void` | A callback function that is called when the clear button is clicked. |
| `showClear` | boolean | Whether to show the clear button. Defaults to `false`. |

*   **Usage**:

```tsx
import { SearchInput } from './Input';

<SearchInput placeholder="Search..." />
```

### Select

*   **File**: `products/sigma-lab/ui/src/components/forms/Select.tsx`
*   **Description**: A component that displays a select dropdown.
*   **Props**: This component accepts all the standard props for an HTML `select` element, plus the following:

| Name | Type | Description |
| --- | --- | --- |
| `label` | string | The label for the select. |
| `error` | string | An error message to display. |
| `helpText` | string | Help text to display below the select. |
| `size` | `sm` \| `md` \| `lg` | The size of the select. Defaults to `md`. |
| `options` | `SelectOption[]` | An array of options to display in the select. See the `SelectOption` interface in the source file for the structure of each option. |
| `placeholder` | string | A placeholder to display when no option is selected. |
| `fullWidth` | boolean | Whether the select should take up the full width of its container. Defaults to `false`. |

*   **Usage**:

```tsx
import { Select } from './Select';

const options = [
  { value: '1', label: 'Option 1' },
  { value: '2', label: 'Option 2' }
];

<Select label="My Select" options={options} />
```

### FilterSelect

*   **File**: `products/sigma-lab/ui/src/components/forms/Select.tsx`
*   **Description**: A specialized select component for filtering.
*   **Props**: This component accepts all the props for the `Select` component, plus the following:

| Name | Type | Description |
| --- | --- | --- |
| `onFilterChange` | `(value: string) => void` | A callback function that is called when the selected filter changes. |

*   **Usage**:

```tsx
import { FilterSelect } from './Select';

const options = [
  { value: '1', label: 'Option 1' },
  { value: '2', label: 'Option 2' }
];

<FilterSelect options={options} onFilterChange={(value) => console.log(value)} />
```

### Toggle

*   **File**: `products/sigma-lab/ui/src/components/forms/Toggle.tsx`
*   **Description**: A component that displays a toggle switch.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `checked` | boolean | Whether the toggle is checked. This is for controlled components. |
| `defaultChecked` | boolean | The default checked state of the toggle. Defaults to `false`. |
| `onChange` | `(checked: boolean) => void` | A callback function that is called when the toggle state changes. |
| `disabled` | boolean | Whether the toggle is disabled. Defaults to `false`. |
| `label` | string | The label for the toggle. |
| `labelPosition` | `left` \| `right` | The position of the label. Defaults to `right`. |
| `size` | `sm` \| `md` \| `lg` | The size of the toggle. Defaults to `md`. |
| `className` | string | An optional CSS class to apply to the toggle. |
| `id` | string | The ID of the toggle. |
| `name` | string | The name of the toggle. |

*   **Usage**:

```tsx
import { Toggle } from './Toggle';

<Toggle label="My Toggle" />
```

## Model Components

These components are used for displaying information about trading models.

### ModelCard

*   **File**: `products/sigma-lab/ui/src/components/models/ModelCard.tsx`
*   **Description**: A component that displays a card with information about a trading model.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `model` | `ModelCardModel` | An object containing the data for the model card. See the `ModelCardModel` type in the source file for the structure of this object. |
| `view` | `card` \| `row` | The view mode for the card. |

*   **Usage**:

```tsx
import { ModelCard } from './ModelCard';

const model = {
  id: 'spy_opt_0dte_hourly',
  title: 'SPY 0DTE Options',
  subtitle: 'Hourly',
  iconName: 'grid',
  iconBg: 'var(--sigmatiq-teal-primary)',
  badge: 'Live',
  badgeClass: 'success',
  stats: [
    { label: 'Sharpe', value: '1.2', trend: 'positive' },
    { label: 'Trades', value: '100' }
  ],
  chart: 'g1',
  updated: '2 hours ago',
  risk: 'Medium',
  actions: ['Backtest', 'Deploy']
};

<ModelCard model={model} view="card" />
```

### ModelsContainer

*   **File**: `products/sigma-lab/ui/src/components/models/ModelsContainer.tsx`
*   **Description**: A container for `ModelCard` components.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `view` | `card` \| `row` | The view mode for the container. |
| `models` | `ModelCardModel[]` | An array of model data to display. |

*   **Usage**:

```tsx
import { ModelsContainer } from './ModelsContainer';

const models = [
  // ... array of model data
];

<ModelsContainer models={models} view="card" />
```

### Pagination

*   **File**: `products/sigma-lab/ui/src/components/models/Pagination.tsx`
*   **Description**: A component that displays pagination controls.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `total` | number | The total number of items to paginate. |

*   **Usage**:

```tsx
import { Pagination } from './Pagination';

<Pagination total={42} />
```

### ControlsBar

*   **File**: `products/sigma-lab/ui/src/components/models/ControlsBar.tsx`
*   **Description**: A component that displays a control bar with search, filtering, and view mode options.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `view` | `card` \| `row` | The current view mode. |
| `setView` | `(v: 'card' | 'row') => void` | A callback function to set the view mode. |

*   **Usage**:

```tsx
import { ControlsBar } from './ControlsBar';

const [view, setView] = React.useState('card');

<ControlsBar view={view} setView={setView} />
```

## Navigation Components

These components are used for navigation within the application.

### Tabs

*   **File**: `products/sigma-lab/ui/src/components/navigation/Tabs.tsx`
*   **Description**: A component that displays a set of tabs.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `tabs` | `Tab[]` | An array of tab objects to display. See the `Tab` interface in the source file for the structure of each tab. |
| `activeTab` | string | The ID of the currently active tab. This is for controlled components. |
| `defaultTab` | string | The ID of the default active tab. |
| `onChange` | `(tabId: string) => void` | A callback function that is called when the active tab changes. |
| `variant` | `default` \| `pills` \| `underline` | The variant of the tabs. Defaults to `default`. |
| `size` | `sm` \| `md` \| `lg` | The size of the tabs. Defaults to `md`. |
| `fullWidth` | boolean | Whether the tabs should take up the full width of their container. Defaults to `false`. |
| `className` | string | An optional CSS class to apply to the tabs. |
| `children` | `React.ReactNode` | The content of the tabs. This should be a set of `TabPanel` components. |

*   **Usage**:

```tsx
import { Tabs, TabPanel } from './Tabs';

const tabs = [
  { id: 'tab1', label: 'Tab 1' },
  { id: 'tab2', label: 'Tab 2' }
];

<Tabs tabs={tabs}>
  <TabPanel tabId="tab1">Content for Tab 1</TabPanel>
  <TabPanel tabId="tab2">Content for Tab 2</TabPanel>
</Tabs>
```

### TabPanel

*   **File**: `products/sigma-lab/ui/src/components/navigation/Tabs.tsx`
*   **Description**: A component that displays the content of a tab.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `tabId` | string | The ID of the tab that this panel corresponds to. |
| `children` | `React.ReactNode` | The content of the tab panel. |
| `className` | string | An optional CSS class to apply to the tab panel. |

*   **Usage**: See the usage example for the `Tabs` component.

### PeriodSelector

*   **File**: `products/sigma-lab/ui/src/components/navigation/Tabs.tsx`
*   **Description**: A specialized tabs component for selecting a time period.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `periods` | `Period[]` | An array of period objects to display. See the component's source for the structure of each period. |
| `activePeriod` | string | The ID of the currently active period. This is for controlled components. |
| `defaultPeriod` | string | The ID of the default active period. Defaults to `1m`. |
| `onChange` | `(period: string) => void` | A callback function that is called when the active period changes. |
| `className` | string | An optional CSS class to apply to the component. |

*   **Usage**:

```tsx
import { PeriodSelector } from './Tabs';

<PeriodSelector onChange={(period) => console.log(period)} />
```

## Signals Components

These components are used for displaying trading signals.

### SignalsTable

*   **File**: `products/sigma-lab/ui/src/components/signals/SignalsTable.tsx`
*   **Description**: A component that displays a table of trading signals.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `rows` | `SignalsRow[]` | An array of signal row objects to display. See the `SignalsRow` type in the source file for the structure of each row. |

*   **Usage**:

```tsx
import { SignalsTable } from './SignalsTable';

const signals = [
  {
    ts: '2025-08-21 12:00:00',
    model: 'spy_opt_0dte_hourly',
    ticker: 'SPY',
    side: 'buy',
    conf: 0.8,
    pack: 'zerosigma'
  }
];

<SignalsTable rows={signals} />
```

### TickerBadge

*   **File**: `products/sigma-lab/ui/src/components/signals/TickerBadge.tsx`
*   **Description**: A component that displays a ticker symbol in a badge.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `ticker` | string | The ticker symbol to display. |

*   **Usage**:

```tsx
import { TickerBadge } from './TickerBadge';

<TickerBadge ticker="SPY" />
```

### SidePill

*   **File**: `products/sigma-lab/ui/src/components/signals/SidePill.tsx`
*   **Description**: A component that displays a pill with the side of a trade (Long or Short).
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `side` | `Long` \| `Short` \| string | The side of the trade. |

*   **Usage**:

```tsx
import { SidePill } from './SidePill';

<SidePill side="Long" />
```

### ConfidenceBadge

*   **File**: `products/sigma-lab/ui/src/components/signals/ConfidenceBadge.tsx`
*   **Description**: A component that displays a badge with the confidence of a signal.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `value` | number | The confidence value. |

*   **Usage**:

```tsx
import { ConfidenceBadge } from './ConfidenceBadge';

<ConfidenceBadge value={0.8} />
```

## Templates Components

These components are used for displaying model templates.

### TemplateCard

*   **File**: `products/sigma-lab/ui/src/components/templates/TemplateCard.tsx`
*   **Description**: A component that displays a card with information about a model template.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `icon` | `IconName` | The name of the icon to display. Defaults to `barChart`. |
| `name` | string | The name of the template. |
| `description` | string | An optional description of the template. |
| `meta` | `TemplateMeta[]` | An array of metadata to display. See the `TemplateMeta` type in the source file for the structure of each item. |
| `tags` | `string[]` | An array of tags to display. |
| `featured` | boolean | Whether the template is featured. |
| `onPrimary` | `() => void` | A callback function that is called when the primary action button is clicked. |
| `onSecondary` | `() => void` | A callback function that is called when the secondary action button is clicked. |

*   **Usage**:

```tsx
import { TemplateCard } from './TemplateCard';

const template = {
  name: 'My Template',
  description: 'A template for my trading strategy.',
  meta: [
    { label: 'Author', value: 'John Doe' },
    { label: 'Version', value: '1.0' }
  ],
  tags: ['swing', 'daily']
};

<TemplateCard {...template} />
```

### TemplatesGrid

*   **File**: `products/sigma-lab/ui/src/components/templates/TemplateCard.tsx`
*   **Description**: A container for `TemplateCard` components.
*   **Props**: None

*   **Usage**:

```tsx
import { TemplatesGrid, TemplateCard } from './TemplateCard';

const templates = [
  // ... array of template data
];

<TemplatesGrid>
  {templates.map(t => <TemplateCard {...t} />)}
</TemplatesGrid>
```

## Trust Components

These components are used for building trust with the user.

### GateBadge

*   **File**: `products/sigma-lab/ui/src/components/trust/GateBadge.tsx`
*   **Description**: A component that displays a badge indicating whether a gate has passed or failed.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `pass` | boolean | Whether the gate has passed. |
| `reasons` | `string[]` | An array of reasons why the gate failed. |

*   **Usage**:

```tsx
import { GateBadge } from './GateBadge';

<GateBadge pass={true} />

<GateBadge pass={false} reasons={['Reason 1', 'Reason 2']} />
```

## UI Components

These components are used for creating the user interface.

### Badge

*   **File**: `products/sigma-lab/ui/src/components/ui/Badge.tsx`
*   **Description**: A component that displays a badge.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `children` | `React.ReactNode` | The content of the badge. |
| `variant` | `success` \| `warning` \| `error` \| `info` \| `default` \| `neutral` | The variant of the badge. Defaults to `default`. |
| `size` | `sm` \| `md` \| `lg` | The size of the badge. Defaults to `md`. |
| `dot` | boolean | Whether to display a dot in the badge. Defaults to `false`. |
| `className` | string | An optional CSS class to apply to the badge. |

*   **Usage**:

```tsx
import { Badge } from './Badge';

<Badge variant="success">Success</Badge>
```

### StatusBadge

*   **File**: `products/sigma-lab/ui/src/components/ui/Badge.tsx`
*   **Description**: A specialized badge for displaying status.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `status` | `active` \| `inactive` \| `training` \| `paused` \| `error` \| `success` \| `pending` | The status to display. |
| `className` | string | An optional CSS class to apply to the badge. |

*   **Usage**:

```tsx
import { StatusBadge } from './Badge';

<StatusBadge status="active" />
```

### RiskBadge

*   **File**: `products/sigma-lab/ui/src/components/ui/Badge.tsx`
*   **Description**: A specialized badge for displaying risk profiles.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `risk` | `conservative` \| `balanced` \| `aggressive` | The risk profile to display. |
| `className` | string | An optional CSS class to apply to the badge. |

*   **Usage**:

```tsx
import { RiskBadge } from './Badge';

<RiskBadge risk="conservative" />
```

### PackBadge

*   **File**: `products/sigma-lab/ui/src/components/ui/Badge.tsx`
*   **Description**: A specialized badge for displaying pack names.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `pack` | string | The name of the pack to display. |
| `className` | string | An optional CSS class to apply to the badge. |

*   **Usage**:

```tsx
import { PackBadge } from './Badge';

<PackBadge pack="zerosigma" />
```

### Button

*   **File**: `products/sigma-lab/ui/src/components/ui/Button.tsx`
*   **Description**: A component that displays a button.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `children` | `React.ReactNode` | The content of the button. |
| `variant` | `primary` \| `secondary` \| `ghost` \| `danger` \| `success` | The variant of the button. Defaults to `primary`. |
| `size` | `sm` \| `md` \| `lg` | The size of the button. Defaults to `md`. |
| `disabled` | boolean | Whether the button is disabled. Defaults to `false`. |
| `loading` | boolean | Whether the button is in a loading state. Defaults to `false`. |
| `icon` | string | The name of an icon to display in the button. |
| `iconPosition` | `left` \| `right` | The position of the icon. Defaults to `left`. |
| `fullWidth` | boolean | Whether the button should take up the full width of its container. Defaults to `false`. |
| `className` | string | An optional CSS class to apply to the button. |
| `onClick` | `(e: React.MouseEvent<HTMLButtonElement>) => void` | A callback function that is called when the button is clicked. |
| `type` | `button` \| `submit` \| `reset` | The type of the button. Defaults to `button`. |

*   **Usage**:

```tsx
import { Button } from './Button';

<Button variant="primary">My Button</Button>
```

### IconButton

*   **File**: `products/sigma-lab/ui/src/components/ui/Button.tsx`
*   **Description**: A component that displays an icon-only button.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `icon` | string | The name of the icon to display. |
| `variant` | `primary` \| `secondary` \| `ghost` \| `danger` \| `success` | The variant of the button. Defaults to `secondary`. |
| `size` | `sm` \| `md` \| `lg` | The size of the button. Defaults to `md`. |
| `disabled` | boolean | Whether the button is disabled. Defaults to `false`. |
| `loading` | boolean | Whether the button is in a loading state. Defaults to `false`. |
| `className` | string | An optional CSS class to apply to the button. |
| `onClick` | `(e: React.MouseEvent<HTMLButtonElement>) => void` | A callback function that is called when the button is clicked. |
| `aria-label` | string | An ARIA label for the button. |

*   **Usage**:

```tsx
import { IconButton } from './Button';

<IconButton icon="search" aria-label="Search" />
```

### Card

*   **File**: `products/sigma-lab/ui/src/components/ui/Card.tsx`
*   **Description**: A component that displays a card.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `children` | `React.ReactNode` | The content of the card. |
| `className` | string | An optional CSS class to apply to the card. |
| `onClick` | `() => void` | A callback function that is called when the card is clicked. |
| `hoverable` | boolean | Whether the card should have a hover effect. Defaults to `true`. |

*   **Usage**:

```tsx
import { Card } from './Card';

<Card>
  <p>Card content</p>
</Card>
```

### ProgressBar

*   **File**: `products/sigma-lab/ui/src/components/ui/ProgressBar.tsx`
*   **Description**: A component that displays a progress bar.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `value` | number | The current value of the progress bar. |
| `max` | number | The maximum value of the progress bar. Defaults to `100`. |
| `label` | string | An optional label to display. |
| `showValue` | boolean | Whether to show the current value. Defaults to `false`. |
| `variant` | `default` \| `success` \| `warning` \| `error` \| `gradient` | The variant of the progress bar. Defaults to `default`. |
| `size` | `sm` \| `md` \| `lg` | The size of the progress bar. Defaults to `md`. |
| `animated` | boolean | Whether to animate the progress bar. Defaults to `false`. |
| `className` | string | An optional CSS class to apply to the progress bar. |

*   **Usage**:

```tsx
import { ProgressBar } from './ProgressBar';

<ProgressBar value={50} />
```

### CapacityBar

*   **File**: `products/sigma-lab/ui/src/components/ui/ProgressBar.tsx`
*   **Description**: A specialized progress bar for displaying capacity.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `used` | number | The used capacity. |
| `total` | number | The total capacity. |
| `label` | string | An optional label to display. |
| `thresholdWarning` | number | The warning threshold. Defaults to `70`. |
| `thresholdError` | number | The error threshold. Defaults to `90`. |
| `showPercentage` | boolean | Whether to show the percentage. Defaults to `true`. |
| `className` | string | An optional CSS class to apply to the capacity bar. |

*   **Usage**:

```tsx
import { CapacityBar } from './ProgressBar';

<CapacityBar used={75} total={100} />
```

### Tooltip

*   **File**: `products/sigma-lab/ui/src/components/ui/Tooltip.tsx`
*   **Description**: A component that displays a tooltip.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `content` | `React.ReactNode` | The content of the tooltip. |
| `children` | `React.ReactElement` | The element that the tooltip is attached to. |
| `placement` | `top` \| `bottom` \| `left` \| `right` \| `auto` | The placement of the tooltip. Defaults to `auto`. |
| `delay` | number | The delay in milliseconds before the tooltip is shown. Defaults to `200`. |
| `className` | string | An optional CSS class to apply to the tooltip. |
| `disabled` | boolean | Whether the tooltip is disabled. Defaults to `false`. |
| `trigger` | `hover` \| `click` \| `focus` | The trigger that shows the tooltip. Defaults to `hover`. |

*   **Usage**:

```tsx
import { Tooltip } from './Tooltip';

<Tooltip content="This is a tooltip">
  <button>Hover me</button>
</Tooltip>
```

### Card Sub-components

The `Card` component has several sub-components that can be used to structure the content of the card.

*   **`CardHeader`**: The header of the card.
*   **`CardIcon`**: An icon to display in the card header.
*   **`CardHeaderInfo`**: A container for the title and subtitle in the card header.
*   **`CardBadge`**: A badge to display in the card header.
*   **`CardContent`**: The main content of the card.
*   **`CardStats`**: A container for stats in the card content.
*   **`StatItem`**: A single stat item.
*   **`CardChart`**: A container for a chart in the card content.
*   **`CardMeta`**: A container for metadata in the card content.
*   **`CardActions`**: A container for action buttons in the card content.
*   **`CardButton`**: A button to display in the card actions.

## Health Components

These components are used for displaying health status.

### HealthTile

*   **File**: `products/sigma-lab/ui/src/components/health/HealthTile.tsx`
*   **Description**: A component that displays a health status tile.
*   **Props**:

| Name | Type | Description |
| --- | --- | --- |
| `icon` | `React.ReactNode` | An optional icon to display. |
| `label` | string | The label for the health tile. |
| `value` | string | The value of the health tile. |
| `status` | `ok` \| `warn` \| `error` | The status of the health tile. Defaults to `ok`. |

*   **Usage**:

```tsx
import { HealthTile } from './HealthTile';

<HealthTile label="API" value="Online" status="ok" />
```

### HealthTiles

*   **File**: `products/sigma-lab/ui/src/components/health/HealthTile.tsx`
*   **Description**: A container for `HealthTile` components.
*   **Props**: None

*   **Usage**:

```tsx
import { HealthTiles, HealthTile } from './HealthTile';

<HealthTiles>
  <HealthTile label="API" value="Online" status="ok" />
  <HealthTile label="Database" value="Online" status="ok" />
</HealthTiles>
```
