import React from 'react';
import styled from 'styled-components';
import { theme } from '../../styles/theme';
import { Button } from '../common/Button';
import { DashboardCard } from './DashboardCard';
import { recentModels } from '../../data/dashboard.data';

const ModelsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
`;

const ModelItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: ${theme.colors.bg.surface2};
  border-radius: 8px;
  transition: all 0.2s;

  &:hover {
    background: ${theme.colors.bg.surface3};
  }
`;

const ModelInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
`;

const ModelId = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  color: ${theme.colors.text.primary};
  font-size: 14px;
`;

const ModelDot = styled.div<{ color: string }>`
  width: 4px;
  height: 4px;
  background: ${props => props.color};
  border-radius: 50%;
`;

const ModelMeta = styled.span`
  font-size: 11px;
  color: ${theme.colors.text.tertiary};
  padding-left: 12px;
`;

export const RecentModels: React.FC = () => {
  const getColor = (color: string) => {
    const colorMap: Record<string, string> = {
      teal: theme.colors.primary.brightTeal,
      golden: theme.colors.accent.golden,
      tealDark: theme.colors.primary.tealDark
    };
    return colorMap[color] || theme.colors.primary.brightTeal;
  };

  return (
    <DashboardCard title="Recent Models">
      <ModelsList>
        {recentModels.map(model => (
          <ModelItem key={model.id}>
            <ModelInfo>
              <ModelId>
                <ModelDot color={getColor(model.statusColor)} />
                <span>{model.id}</span>
              </ModelId>
              <ModelMeta>{model.pack} • Updated {model.updatedAt}</ModelMeta>
            </ModelInfo>
            <Button size="small">Open</Button>
          </ModelItem>
        ))}
      </ModelsList>
    </DashboardCard>
  );
};
