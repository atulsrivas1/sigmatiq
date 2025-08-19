from pathlib import Path
from typing import Any, Dict
import yaml
from .sets import IndicatorSet, IndicatorSpec

# Alias mapping to support idea-set names
ALIAS = {
    'returns': 'ret',
    'stddev': 'rolling_std',
    'bollinger': 'bollinger_bands',
    'iv_skew_25d_rr': 'iv_skew_25d',
}

def load_indicator_set(path: str | Path) -> IndicatorSet:
    p = Path(path)
    data = yaml.safe_load(p.read_text())
    name = data.get("name", p.stem)
    version = int(data.get("version", 1))
    desc = data.get("description", "")
    specs = []
    for item in data.get("indicators", []):
        iname = item.get("name")
        if iname in ALIAS:
            iname = ALIAS[iname]
        iver = int(item.get("version", 1))
        params: Dict[str, Any] = {k: v for k, v in item.items() if k not in ("name", "version")}
        specs.append(IndicatorSpec(name=iname, version=iver, params=params))
    return IndicatorSet(name=name, version=version, description=desc, indicators=specs)
