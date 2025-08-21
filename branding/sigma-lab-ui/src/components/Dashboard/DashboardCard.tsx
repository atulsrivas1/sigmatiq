import React from 'react';
import styled from 'styled-components';
import { theme } from '../../styles/theme';

const Card = styled.div`
  background: ${theme.colors.bg.surface1};
  border: 1px solid ${theme.colors.bg.border};
  border-radius: ${theme.borderRadius.xl};
  padding: 20px;
  display: flex;
  flex-direction: column;
  min-height: 260px;
`;

const CardTitle = styled.h3`
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: ${theme.colors.text.secondary};
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid ${theme.colors.bg.border};
`;

interface DashboardCardProps {
  title: string;
  children: React.ReactNode;
}

export const DashboardCard: React.FC<DashboardCardProps> = ({ title, children }) => {
  return (
    <Card>
      <CardTitle>{title}</CardTitle>
      {children}
    </Card>
  );
};
