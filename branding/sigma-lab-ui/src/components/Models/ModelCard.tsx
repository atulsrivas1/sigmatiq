import React from 'react';
import styled from 'styled-components';
import { theme } from '../../styles/theme';
import { Model } from '../../types';
import { Icon } from '../common/Icon';

const Card = styled.div`
  background: ${theme.colors.bg.surface1};
  border: 1px solid ${theme.colors.bg.border};
  border-radius: ${theme.borderRadius.xl};
  overflow: hidden;
  transition: all 0.2s;
  cursor: pointer;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    border-color: ${theme.colors.primary.brightTeal};
  }
`;

const CardHeader = styled.div`
  padding: 14px;
  background: ${theme.colors.bg.surface2};
  border-bottom: 1px solid ${theme.colors.bg.border};
  display: flex;
  align-items: center;
  gap: 12px;
`;

const CardIcon = styled.div<{ bgColor: string }>`
  width: 32px;
  height: 32px;
  background: ${props => props.bgColor};
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
`;

const CardHeaderInfo = styled.div`
  flex: 1;
  min-width: 0;
`;

const CardTitle = styled.div`
  font-size: 14px;
  font-weight: 600;
  color: ${theme.colors.text.primary};
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`;

const CardSubtitle = styled.div`
  font-size: 12px;
  color: ${theme.colors.text.tertiary};
`;

const CardBadge = styled.span<{ variant: string }>`
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: ${props => 
    props.variant === 'success' ? 'rgba(0,196,167,0.2)' :
    props.variant === 'warning' ? 'rgba(255,184,0,0.2)' :
    'rgba(255,87,87,0.2)'
  };
  color: ${props => 
    props.variant === 'success' ? theme.colors.status.success :
    props.variant === 'warning' ? theme.colors.status.warning :
    theme.colors.status.error
  };
`;

const CardContent = styled.div`
  padding: 14px;
`;

const CardStats = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 14px;
`;

const StatItem = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2px;
`;

const StatLabel = styled.span`
  font-size: 11px;
  color: ${theme.colors.text.tertiary};
  text-transform: uppercase;
  letter-spacing: 0.3px;
`;

const StatValue = styled.span<{ trend?: string }>`
  font-size: 16px;
  font-weight: 600;
  color: ${props => 
    props.trend === 'positive' ? theme.colors.status.success :
    props.trend === 'negative' ? theme.colors.status.error :
    theme.colors.text.primary
  };
`;

const CardMeta = styled.div`
  display: flex;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid ${theme.colors.bg.border};
  font-size: 11px;
  color: ${theme.colors.text.tertiary};
`;

const CardActions = styled.div`
  padding: 10px;
  background: ${theme.colors.bg.surface2};
  border-top: 1px solid ${theme.colors.bg.border};
  display: flex;
  gap: 8px;
`;

const CardButton = styled.button<{ primary?: boolean }>`
  flex: 1;
  padding: 8px 12px;
  background: ${props => props.primary ? theme.colors.primary.brightTeal : theme.colors.bg.surface3};
  border: 1px solid ${props => props.primary ? theme.colors.primary.brightTeal : theme.colors.bg.border};
  border-radius: 6px;
  color: ${props => props.primary ? theme.colors.bg.primary : theme.colors.text.primary};
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: ${theme.colors.primary.brightTeal};
    border-color: ${theme.colors.primary.brightTeal};
    color: ${theme.colors.bg.primary};
  }
`;

interface ModelCardProps {
  model: Model;
}

export const ModelCard: React.FC<ModelCardProps> = ({ model }) => {
  return (
    <Card>
      <CardHeader>
        <CardIcon bgColor={model.icon.bgColor}>
          <Icon name={model.icon.type} size={18} color={theme.colors.bg.primary} />
        </CardIcon>
        <CardHeaderInfo>
          <CardTitle>{model.name}</CardTitle>
          <CardSubtitle>{model.pack} • {model.type}</CardSubtitle>
        </CardHeaderInfo>
        <CardBadge variant={model.badgeColor}>
          {model.status.toUpperCase()}
        </CardBadge>
      </CardHeader>
      
      <CardContent>
        <CardStats>
          <StatItem>
            <StatLabel>Sharpe</StatLabel>
            <StatValue>{model.stats.sharpe}</StatValue>
          </StatItem>
          <StatItem>
            <StatLabel>Return</StatLabel>
            <StatValue trend={model.stats.return.trend}>
              {model.stats.return.value}
            </StatValue>
          </StatItem>
          <StatItem>
            <StatLabel>Win Rate</StatLabel>
            <StatValue>{model.stats.winRate}</StatValue>
          </StatItem>
          <StatItem>
            <StatLabel>Trades</StatLabel>
            <StatValue>{model.stats.trades}</StatValue>
          </StatItem>
        </CardStats>

        <CardMeta>
          <span>Updated {model.meta.updatedAt}</span>
          <span>Risk: {model.meta.risk}</span>
        </CardMeta>
      </CardContent>

      <CardActions>
        {model.actions.map((action, index) => (
          <CardButton key={index} primary={action.primary}>
            {action.label}
          </CardButton>
        ))}
      </CardActions>
    </Card>
  );
};
