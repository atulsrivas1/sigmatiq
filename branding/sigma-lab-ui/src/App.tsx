import React from 'react';
import styled, { createGlobalStyle } from 'styled-components';
import { AppShell } from './components/Layout/AppShell';
import { RecentModels } from './components/Dashboard/RecentModels';
import { ModelCard } from './components/Models/ModelCard';
import { modelsList } from './data/dashboard.data';
import { theme } from './styles/theme';

const GlobalStyle = createGlobalStyle`
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
    background: ${theme.colors.bg.primary};
    color: ${theme.colors.text.primary};
    min-height: 100vh;
  }
`;

const DashboardGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
`;

const ModelsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
`;

function App() {
  return (
    <>
      <GlobalStyle />
      <AppShell>
        <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
          <h2 style={{ fontSize: '20px', marginBottom: '24px' }}>Dashboard</h2>
          <DashboardGrid>
            <RecentModels />
          </DashboardGrid>
          <h2 style={{ fontSize: '20px', marginBottom: '24px' }}>Models</h2>
          <ModelsGrid>
            {modelsList.map(model => (
              <ModelCard key={model.id} model={model} />
            ))}
          </ModelsGrid>
        </div>
      </AppShell>
    </>
  );
}

export default App;
