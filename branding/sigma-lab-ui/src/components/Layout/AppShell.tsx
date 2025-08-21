import React from 'react';
import styled from 'styled-components';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';

const AppShellContainer = styled.div`
  display: flex;
  height: 100vh;
`;

const MainContent = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
`;

const ContentArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 24px;
`;

interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  return (
    <AppShellContainer>
      <Sidebar />
      <MainContent>
        <TopBar />
        <ContentArea>
          {children}
        </ContentArea>
      </MainContent>
    </AppShellContainer>
  );
};
