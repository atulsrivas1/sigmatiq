from typing import List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class IndicatorSetVersion(BaseModel):
    id: int
    name: str
    version: str
    description: str
    created_at: datetime
    updated_at: datetime

class IndicatorSpec(BaseModel):
    id: int
    indicator_set_id: int
    name: str
    version: str
    params: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class ModelVersion(BaseModel):
    id: int
    name: str
    version: str
    description: str
    artifact_uri: str
    data_hash: str
    git_sha: str
    metrics: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class PolicyVersion(BaseModel):
    id: int
    name: str
    version: str
    description: str
    spec: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class StrategyVersion(BaseModel):
    strategy_id: str
    version: int
    status: str
    title: str
    objective: str | None = None
    created_at: datetime
    updated_at: datetime

class IndicatorCatalogEntry(BaseModel):
    id: str
    version: int
    status: str
    title: str | None = None
    category: str | None = None
    subcategory: str | None = None
    created_at: datetime
    updated_at: datetime


class StrategyVersion(BaseModel):
    strategy_id: str
    version: int
    status: str
    title: str
    objective: str | None = None
    created_at: datetime
    updated_at: datetime
