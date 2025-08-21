import React from 'react';
import styled from 'styled-components';
import { theme } from '../../styles/theme';
import { Icon } from '../common/Icon';
import { navigationItems } from '../../data/dashboard.data';

const SidebarContainer = styled.nav`
  width: 240px;
  background: ${theme.colors.bg.surface1};
  border-right: 1px solid ${theme.colors.bg.border};
  display: flex;
  flex-direction: column;
`;

const SidebarHeader = styled.div`
  padding: 20px;
  border-bottom: 1px solid ${theme.colors.bg.border};
  display: flex;
  align-items: center;
  gap: 12px;
`;

const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;

const LogoIcon = styled.div`
  width: 32px;
  height: 32px;
  position: relative;
  
  .square {
    position: absolute;
    width: 14px;
    height: 14px;
    border-radius: 2px;
    
    &:nth-child(1) { top: 0; left: 0; background: #1ABC9C; }
    &:nth-child(2) { top: 0; right: 0; background: #48C9B0; }
    &:nth-child(3) { bottom: 0; left: 0; background: #F59E0B; }
    &:nth-child(4) { bottom: 0; right: 0; background: #16A085; }
  }
`;

const LogoText = styled.div`
  font-size: 18px;
  font-weight: 600;
  color: ${theme.colors.text.primary};
`;

const NavSection = styled.div`
  padding: 12px;
`;

const NavItemEl = styled.a<{ active?: boolean }>`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  color: ${props => props.active ? theme.colors.primary.brightTeal : theme.colors.text.secondary};
  background: ${props => props.active ? theme.colors.bg.surface3 : 'transparent'};
  text-decoration: none;
  transition: all 0.2s;
  margin-bottom: 4px;
  cursor: pointer;

  &:hover {
    background: ${theme.colors.bg.surface2};
    color: ${theme.colors.text.primary};
  }
`;

export const Sidebar: React.FC = () => {
  const [activeItem, setActiveItem] = React.useState('dashboard');

  return (
    <SidebarContainer>
      <SidebarHeader>
        <Logo>
          <LogoIcon>
            <div className="square" />
            <div className="square" />
            <div className="square" />
            <div className="square" />
          </LogoIcon>
          <LogoText>SIGMA LAB</LogoText>
        </Logo>
      </SidebarHeader>
      
      <NavSection>
        {navigationItems.map(item => (
          <NavItemEl 
            key={item.id}
            active={activeItem === item.id}
            onClick={() => setActiveItem(item.id)}
          >
            <Icon name={item.icon} />
            <span>{item.label}</span>
          </NavItemEl>
        ))}
      </NavSection>
    </SidebarContainer>
  );
};
