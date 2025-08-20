# Development Guide

Welcome to the Sigmatiq Sigma Lab development guide! This document covers everything you need to contribute to the project.

## 🚀 Development Setup

### Prerequisites

Ensure you have the following installed:
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Git
- Docker (optional, for containerized development)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork:
```bash
git clone https://github.com/YOUR-USERNAME/sigmatiq.git
cd sigmatiq
```

3. Add upstream remote:
```bash
git remote add upstream https://github.com/atulsrivas1/sigmatiq.git
```

### Environment Setup

#### Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # Unix/macOS
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### Node Environment

```bash
cd products/sigma-lab/ui
npm install
```

#### Database Setup

```bash
# Create development database
createdb sigmalab_dev

# Run migrations
psql -U postgres -d sigmalab_dev -f products/sigma-lab/api/migrations/0001_init.sql
```

#### Environment Variables

Create `.env.development`:
```env
# Development Environment
DEBUG=true
LOG_LEVEL=DEBUG

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sigmalab_dev
DB_USER=dev_user
DB_PASSWORD=dev_password

# API Keys (use test keys)
POLYGON_API_KEY=your_test_key

# Services
REDIS_URL=redis://localhost:6379
API_BASE_URL=http://localhost:8001
```

## 📁 Project Structure

```
sigmatiq/
├── products/
│   ├── sigma-lab/
│   │   ├── api/           # FastAPI backend
│   │   │   ├── endpoints/ # API routes
│   │   │   ├── services/  # Business logic
│   │   │   ├── models/    # Data models
│   │   │   └── tests/     # API tests
│   │   └── ui/            # React frontend
│   │       ├── src/
│   │       │   ├── components/
│   │       │   ├── pages/
│   │       │   └── services/
│   │       └── tests/     # UI tests
│   ├── sigma-core/        # Core libraries
│   └── sigma-platform/    # Platform services
├── docs/                  # Documentation
├── scripts/              # Build/deploy scripts
└── tests/               # Integration tests
```

## 🎨 Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Good example
from typing import List, Optional
from datetime import datetime

from sigma_core.models import Model
from sigma_core.utils import calculate_metrics


class BacktestEngine:
    """Engine for running backtests on trading models."""
    
    def __init__(self, config: dict):
        """Initialize backtest engine.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self._validate_config()
    
    def run_backtest(
        self,
        model: Model,
        start_date: datetime,
        end_date: datetime,
        initial_capital: float = 100000.0
    ) -> dict:
        """Run backtest for given model.
        
        Args:
            model: Trading model to backtest
            start_date: Start date for backtest
            end_date: End date for backtest
            initial_capital: Starting capital
            
        Returns:
            Dictionary containing backtest metrics
        """
        # Implementation here
        pass
```

### TypeScript/React Style Guide

```typescript
// Good example
import React, { useState, useEffect } from 'react';
import { Model, BacktestResult } from '@/types';
import { useApi } from '@/hooks';

interface ModelCardProps {
  model: Model;
  onSelect?: (model: Model) => void;
}

export const ModelCard: React.FC<ModelCardProps> = ({ 
  model, 
  onSelect 
}) => {
  const [results, setResults] = useState<BacktestResult | null>(null);
  const { getBacktestResults } = useApi();
  
  useEffect(() => {
    const fetchResults = async () => {
      const data = await getBacktestResults(model.id);
      setResults(data);
    };
    
    fetchResults();
  }, [model.id]);
  
  return (
    <div className="model-card">
      {/* Component implementation */}
    </div>
  );
};
```

### Commit Message Convention

We follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

Examples:
```bash
feat(api): add sweep endpoint for batch backtesting

fix(ui): resolve theme toggle persistence issue

docs(wiki): update BTB pipeline documentation
```

## 🧪 Testing

### Python Tests

#### Unit Tests

```python
# tests/test_backtest_engine.py
import pytest
from datetime import datetime
from sigma_core.backtest import BacktestEngine

class TestBacktestEngine:
    @pytest.fixture
    def engine(self):
        config = {"mode": "test"}
        return BacktestEngine(config)
    
    def test_initialization(self, engine):
        assert engine is not None
        assert engine.config["mode"] == "test"
    
    def test_run_backtest(self, engine, sample_model):
        result = engine.run_backtest(
            model=sample_model,
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 12, 31)
        )
        
        assert "sharpe" in result
        assert result["sharpe"] > 0
```

Run tests:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sigma_core --cov-report=html

# Run specific test file
pytest tests/test_backtest_engine.py

# Run with verbose output
pytest -v
```

### JavaScript/React Tests

```typescript
// ModelCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ModelCard } from './ModelCard';

describe('ModelCard', () => {
  const mockModel = {
    id: 'test-model',
    name: 'Test Model',
    packId: 'swingsigma'
  };
  
  it('renders model name', () => {
    render(<ModelCard model={mockModel} />);
    expect(screen.getByText('Test Model')).toBeInTheDocument();
  });
  
  it('calls onSelect when clicked', () => {
    const handleSelect = jest.fn();
    render(<ModelCard model={mockModel} onSelect={handleSelect} />);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleSelect).toHaveBeenCalledWith(mockModel);
  });
});
```

Run tests:
```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

### Integration Tests

```python
# tests/integration/test_pipeline.py
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_full_pipeline():
    # Build matrix
    build_response = client.post("/build_matrix", json={
        "model_id": "test_model",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    })
    assert build_response.status_code == 200
    matrix_sha = build_response.json()["matrix_sha"]
    
    # Train model
    train_response = client.post("/train", json={
        "model_id": "test_model",
        "matrix_sha": matrix_sha
    })
    assert train_response.status_code == 200
    
    # Run backtest
    backtest_response = client.post("/backtest", json={
        "model_id": "test_model",
        "config": {"threshold": 0.7}
    })
    assert backtest_response.status_code == 200
```

## 🔧 Development Workflow

### Branch Strategy

We use Git Flow:

```
main
├── develop
│   ├── feature/add-new-indicator
│   ├── feature/improve-backtest-speed
│   └── feature/ui-dark-mode
├── release/v1.2.0
└── hotfix/fix-critical-bug
```

### Creating a Feature

1. Create feature branch:
```bash
git checkout develop
git pull upstream develop
git checkout -b feature/your-feature-name
```

2. Make changes and commit:
```bash
git add .
git commit -m "feat: add your feature"
```

3. Push to your fork:
```bash
git push origin feature/your-feature-name
```

4. Create Pull Request on GitHub

### Code Review Process

All PRs require:
- ✅ Passing CI/CD checks
- ✅ Code review approval
- ✅ Test coverage maintained
- ✅ Documentation updated

## 🏗️ Architecture Guidelines

### Service Layer Pattern

```python
# services/model_service.py
class ModelService:
    def __init__(self, repository: ModelRepository):
        self.repository = repository
    
    async def create_model(self, data: ModelCreate) -> Model:
        # Business logic here
        model = await self.repository.create(data)
        await self.publish_event("model.created", model)
        return model
```

### Repository Pattern

```python
# repositories/model_repository.py
class ModelRepository:
    def __init__(self, db: Database):
        self.db = db
    
    async def create(self, data: ModelCreate) -> Model:
        query = models.insert().values(**data.dict())
        result = await self.db.execute(query)
        return Model(**result)
```

### API Endpoint Structure

```python
# endpoints/models.py
from fastapi import APIRouter, Depends
from services import ModelService

router = APIRouter(prefix="/models", tags=["models"])

@router.post("/", response_model=Model)
async def create_model(
    data: ModelCreate,
    service: ModelService = Depends(get_model_service)
):
    return await service.create_model(data)
```

## 🐛 Debugging

### Backend Debugging

#### Using debugpy

```python
# Add to your development script
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()  # Pause until debugger connects
```

VSCode launch.json:
```json
{
  "name": "Python: Remote Attach",
  "type": "python",
  "request": "attach",
  "connect": {
    "host": "localhost",
    "port": 5678
  }
}
```

#### Logging

```python
import logging

logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug(f"Processing data: {data}")
    try:
        result = complex_operation(data)
        logger.info(f"Successfully processed: {result}")
        return result
    except Exception as e:
        logger.error(f"Error processing data: {e}", exc_info=True)
        raise
```

### Frontend Debugging

#### React DevTools

Install React DevTools browser extension for component inspection.

#### Console Debugging

```typescript
// Temporary debugging
console.log('Component state:', state);
console.table(data);
console.time('API Call');
// ... API call
console.timeEnd('API Call');
```

#### Source Maps

Ensure source maps are enabled in development:
```javascript
// vite.config.ts
export default {
  build: {
    sourcemap: true
  }
}
```

## 📦 Dependencies

### Adding Python Dependencies

```bash
# Add to requirements.txt
echo "new-package==1.0.0" >> requirements.txt

# Or use pip-tools
pip-compile requirements.in
```

### Adding Node Dependencies

```bash
# Production dependency
npm install package-name

# Development dependency
npm install -D package-name
```

## 🚀 Performance Optimization

### Python Performance

```python
# Use generators for large datasets
def process_large_dataset(data):
    for item in data:
        yield transform(item)

# Cache expensive computations
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(param):
    # Expensive operation
    return result

# Use numpy for numerical operations
import numpy as np

# Slow
result = [x * 2 for x in large_list]

# Fast
result = np.array(large_list) * 2
```

### React Performance

```typescript
// Memoize expensive components
import { memo, useMemo, useCallback } from 'react';

const ExpensiveComponent = memo(({ data }) => {
  const processedData = useMemo(
    () => expensiveProcessing(data),
    [data]
  );
  
  const handleClick = useCallback(() => {
    // Handle click
  }, []);
  
  return <div>{/* Render */}</div>;
});

// Virtualize large lists
import { FixedSizeList } from 'react-window';

const LargeList = ({ items }) => (
  <FixedSizeList
    height={600}
    itemCount={items.length}
    itemSize={50}
    width="100%"
  >
    {({ index, style }) => (
      <div style={style}>
        {items[index]}
      </div>
    )}
  </FixedSizeList>
);
```

## 📚 Documentation

### Inline Documentation

```python
def calculate_sharpe_ratio(
    returns: np.ndarray,
    risk_free_rate: float = 0.02
) -> float:
    """Calculate Sharpe ratio for given returns.
    
    The Sharpe ratio measures risk-adjusted performance by calculating
    the average return earned in excess of the risk-free rate per unit
    of volatility.
    
    Args:
        returns: Array of period returns
        risk_free_rate: Annual risk-free rate (default: 2%)
    
    Returns:
        Sharpe ratio value
        
    Example:
        >>> returns = np.array([0.01, 0.02, -0.01, 0.03])
        >>> sharpe = calculate_sharpe_ratio(returns)
        >>> print(f"Sharpe Ratio: {sharpe:.2f}")
    """
    excess_returns = returns - risk_free_rate / 252
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
```

### API Documentation

FastAPI automatically generates OpenAPI documentation at `/docs`.

### Component Documentation

```typescript
/**
 * ModelCard displays summary information for a trading model.
 * 
 * @component
 * @example
 * ```tsx
 * <ModelCard
 *   model={model}
 *   onSelect={(m) => console.log('Selected:', m)}
 * />
 * ```
 */
```

## 🔒 Security Guidelines

### Input Validation

```python
from pydantic import BaseModel, validator

class ModelCreate(BaseModel):
    name: str
    ticker: str
    
    @validator('ticker')
    def validate_ticker(cls, v):
        if not v.isalpha() or len(v) > 5:
            raise ValueError('Invalid ticker symbol')
        return v.upper()
```

### SQL Injection Prevention

```python
# Bad - vulnerable to SQL injection
query = f"SELECT * FROM models WHERE id = '{model_id}'"

# Good - parameterized query
query = "SELECT * FROM models WHERE id = %s"
cursor.execute(query, (model_id,))
```

### Authentication

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token = Depends(security)):
    user = await verify_token(token.credentials)
    if not user:
        raise HTTPException(status_code=401)
    return user
```

## 🚢 Deployment

### Local Build

```bash
# Build backend
cd products/sigma-lab/api
python -m build

# Build frontend
cd products/sigma-lab/ui
npm run build
```

### Docker Build

```bash
# Build all services
docker-compose build

# Run services
docker-compose up
```

### CI/CD Pipeline

GitHub Actions workflow:
```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest --cov
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## 📈 Monitoring

### Application Metrics

```python
from prometheus_client import Counter, Histogram

request_count = Counter('api_requests_total', 'Total API requests')
request_duration = Histogram('api_request_duration_seconds', 'API request duration')

@request_duration.time()
@request_count.count_exceptions()
async def api_endpoint():
    # Endpoint logic
    pass
```

### Logging

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "backtest_completed",
    model_id="model_123",
    sharpe=1.85,
    duration=45.2
)
```

## 🤝 Contributing

### How to Contribute

1. Check existing issues or create new one
2. Fork and create feature branch
3. Write code and tests
4. Update documentation
5. Submit pull request

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

## 📞 Getting Help

- **Discord**: [Join our community](https://discord.gg/sigmatiq)
- **GitHub Issues**: [Report bugs](https://github.com/atulsrivas1/sigmatiq/issues)
- **Documentation**: [Wiki](https://github.com/atulsrivas1/sigmatiq/wiki)
- **Email**: dev@sigmatiq.com

---

Happy coding! 🚀