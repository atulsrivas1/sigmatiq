from .indicator_registry import IndicatorRegistry as DBIndicatorRegistry, indicator_registry
from .strategy_registry import StrategyRegistry as DBStrategyRegistry
from .indicator_catalog_registry import IndicatorCatalogRegistry as DBIndicatorCatalogRegistry
from .watchlist_registry import WatchlistRegistry as DBWatchlistRegistry
from .preset_registry import PresetRegistry as DBPresetRegistry

__all__ = [
    'DBIndicatorRegistry',
    'DBStrategyRegistry',
    'DBIndicatorCatalogRegistry',
    'DBWatchlistRegistry',
    'DBPresetRegistry',
    'indicator_registry',
]

from .watchlist_registry import WatchlistRegistry as DBWatchlistRegistry
