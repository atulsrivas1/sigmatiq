#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Dict, List, Optional, Literal, Tuple
from pydantic import BaseModel, Field, field_validator, model_validator


class IndicatorRef(BaseModel):
    id: str
    version: Optional[int] = 1
    params: Optional[Dict[str, Any]] = None


class Featureset(BaseModel):
    # Exactly one of these must be provided
    set_id: Optional[str] = None
    version: Optional[int] = None

    strategy_id: Optional[str] = None
    strategy_version: Optional[int] = None

    indicators: Optional[List[IndicatorRef]] = None  # synthetic set

    extra_flags: Optional[Dict[str, Any]] = None

    @model_validator(mode="after")
    def validate_one_source(self):
        sources = sum([
            1 if self.set_id else 0,
            1 if self.strategy_id else 0,
            1 if (self.indicators or []) else 0,
        ])
        if sources != 1:
            raise ValueError("featureset must specify exactly one of set_id, strategy_id, or indicators[]")
        if self.set_id and not self.version:
            raise ValueError("featureset.version required when set_id is provided")
        if self.strategy_id and not self.strategy_version:
            raise ValueError("featureset.strategy_version required when strategy_id is provided")
        return self


class OptionsProxyCfg(BaseModel):
    type: Literal["atm", "custom"] = "atm"
    dte_min: Optional[int] = 7
    delta: Optional[float] = 0.5


class LabelCfg(BaseModel):
    horizon_bars: int = Field(..., ge=1)
    tp_pct: Optional[float] = Field(default=None)
    sl_pct: Optional[float] = Field(default=None)
    max_hold_bars: Optional[int] = Field(default=None, ge=1)
    options_proxy: Optional[OptionsProxyCfg] = None

    @model_validator(mode="after")
    def validate_tp_sl(self):
        if (self.tp_pct is None) != (self.sl_pct is None):
            raise ValueError("label_cfg.tp_pct and sl_pct must be both provided or both omitted")
        return self


class Thresholds(BaseModel):
    buy_min_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    sell_min_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    hold_band: Optional[Tuple[float, float]] = None
    budgets: Optional[Dict[str, int]] = None  # { daily:5, hourly:0 }
    diversity: Optional[Dict[str, Any]] = None  # { per_symbol_cooldown_bars: 10 }

    @field_validator("hold_band")
    def validate_hold_band(cls, v):
        if v is None:
            return v
        a, b = v
        if not (0.0 <= a <= b <= 1.0):
            raise ValueError("hold_band must be within [0,1] and ordered")
        return v


class GuardrailsCfg(BaseModel):
    exposure_caps: Optional[Dict[str, Any]] = None
    regime_bends: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None


class ArtifactsCfg(BaseModel):
    model_uri: str
    calibration_uri: Optional[str] = None
    feature_importances_uri: Optional[str] = None
    git_sha: Optional[str] = None


class PlanTemplate(BaseModel):
    stop_atr: Optional[float] = None
    tp_atr: Optional[float] = None
    max_hold_bars: Optional[int] = Field(default=None, ge=1)
    sizing_hint: Optional[str] = None  # e.g., small|medium|large


class ModelSpecConfig(BaseModel):
    featureset: Featureset
    label_cfg: LabelCfg
    thresholds: Thresholds
    guardrails: GuardrailsCfg
    artifacts: ArtifactsCfg
    plan_template: Optional[PlanTemplate] = None
    training_cfg: Optional[Dict[str, Any]] = None  # free-form validated upstream


class ModelSpecRow(BaseModel):
    model_id: str
    version: int
    status: Literal["draft", "in_review", "published", "deprecated"]
    target_kind: Optional[Literal["indicator_set", "strategy", "recipe"]] = None
    target_id: Optional[str] = None
    target_version: Optional[int] = None
    timeframe: Optional[str] = None
    market: Optional[str] = None
    instrument: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

    featureset: Dict[str, Any]
    label_cfg: Dict[str, Any]
    thresholds: Dict[str, Any]
    guardrails: Dict[str, Any]
    artifacts: Dict[str, Any]
    plan_template: Optional[Dict[str, Any]] = None
    training_cfg: Optional[Dict[str, Any]] = None

    def validate_embedded(self) -> ModelSpecConfig:
        return ModelSpecConfig(
            featureset=Featureset(**self.featureset),
            label_cfg=LabelCfg(**self.label_cfg),
            thresholds=Thresholds(**self.thresholds),
            guardrails=GuardrailsCfg(**self.guardrails),
            artifacts=ArtifactsCfg(**self.artifacts),
            plan_template=PlanTemplate(**self.plan_template) if self.plan_template else None,
            training_cfg=self.training_cfg if self.training_cfg else None,
        )
