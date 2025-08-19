from typing import List, Dict, Any
from pydantic import BaseModel

class IndicatorSpec(BaseModel):
    name: str
    version: int
    params: Dict[str, Any]

class IndicatorSet(BaseModel):
    name: str
    version: int
    description: str
    indicators: List[IndicatorSpec]
