import importlib.util
from pathlib import Path
from typing import Dict, Type, List
from .base import Indicator
import re
import logging

class IndicatorRegistry:
    def __init__(self):
        self.indicators: Dict[str, Type[Indicator]] = {}
        self.load_errors: List[dict] = []
        self.register_builtins()

    def register(self, name: str, indicator_class: Type[Indicator]):
        self.indicators[name] = indicator_class

    def get(self, name: str) -> Type[Indicator]:
        return self.indicators[name]

    def register_builtins(self):
        builtins_dir = Path(__file__).parent / "builtins"
        for f in builtins_dir.glob("*.py"):
            if f.name == "__init__.py":
                continue
            try:
                spec = importlib.util.spec_from_file_location(f"sigma_core.indicators.builtins.{f.stem}", f)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for name, obj in module.__dict__.items():
                        try:
                            if isinstance(obj, type) and issubclass(obj, Indicator) and obj is not Indicator:
                                key = getattr(obj, 'NAME', None) or getattr(obj, 'name', None)
                                if not key:
                                    # CamelCase -> snake_case
                                    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', obj.__name__)
                                    key = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
                                self.register(key, obj)
                        except Exception as e:
                            logging.getLogger(__name__).warning("indicator class registration failed in %s: %s", f.name, e)
                            self.load_errors.append({"file": f.name, "error": str(e), "where": "class_register"})
                else:
                    raise ImportError(f"no loader for {f}")
            except Exception as e:
                logging.getLogger(__name__).warning("indicator module load failed for %s: %s", f.name, e)
                self.load_errors.append({"file": f.name, "error": str(e), "where": "module_load"})

registry = IndicatorRegistry()

def get_indicator(name: str) -> Type[Indicator]:
    return registry.get(name)
def get_load_errors() -> List[dict]:
    return list(registry.load_errors)
