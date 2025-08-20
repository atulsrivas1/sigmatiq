import sys
from pathlib import Path

# Ensure sigma_core package is importable when running from repo root (CI)
HERE = Path(__file__).resolve()
SIGMA_CORE_ROOT = HERE.parents[1]  # products/sigma-core
if str(SIGMA_CORE_ROOT) not in sys.path:
    sys.path.insert(0, str(SIGMA_CORE_ROOT))

