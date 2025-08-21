import React from 'react';
import styled from 'styled-components';
import { theme } from '../../styles/theme';
import { Button } from '../common/Button';

const TopBarContainer = styled.header`
  height: 60px;
  background: ${theme.colors.bg.surface1};
  border-bottom: 1px solid ${theme.colors.bg.border};
  display: flex;
  align-items: center;
  padding: 0 24px;
  justify-content: space-between;
`;

const TopBarLeft = styled.div`
  display: flex;
  align-items: center;
  gap: 20px;
`;

const Breadcrumb = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  color: ${theme.colors.text.tertiary};
  font-size: 13px;
`;

const TopBarRight = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
`;

export const TopBar: React.FC = () => {
  return (
    <TopBarContainer>
      <TopBarLeft>
        <Breadcrumb>
          <span>Home</span>
          <span>/</span>
          <span>Dashboard</span>
        </Breadcrumb>
      </TopBarLeft>
      <TopBarRight>
        <Button size="small">Theme</Button>
        <Button size="small">Settings</Button>
        <Button variant="primary" size="small">Create Model</Button>
      </TopBarRight>
    </TopBarContainer>
  );
};
