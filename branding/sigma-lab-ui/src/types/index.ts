export interface NavItem {
  id: string;
  label: string;
  icon: string;
  route: string;
  active?: boolean;
}

export interface Model {
  id: string;
  name: string;
  pack: string;
  type: string;
  status: 'active' | 'training' | 'paused';
  badgeColor: 'success' | 'warning' | 'error';
  icon: {
    type: string;
    bgColor: string;
  };
  stats: {
    sharpe: string;
    return: {
      value: string;
      trend: 'positive' | 'negative';
    };
    winRate: string;
    trades: string;
  };
  meta: {
    updatedAt: string;
    risk: string;
  };
  chartData: string;
  actions: Array<{
    label: string;
    primary?: boolean;
  }>;
}

export interface RecentModel {
  id: string;
  pack: string;
  status: string;
  statusColor: string;
  updatedAt: string;
}

export interface RunItem {
  name: string;
  model: string;
  time: string;
  status: string;
  statusLabel: string;
  icon: string;
}

export interface QuickAction {
  label: string;
  icon: string;
  route: string;
  primary?: boolean;
}

export interface HealthItem {
  label: string;
  status: string;
  statusClass: string;
  icon: string;
}

export interface FilterOption {
  id: string;
  type: 'search' | 'select';
  label?: string;
  placeholder?: string;
  options?: Array<{
    value: string;
    label: string;
  }>;
}
