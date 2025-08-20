import sys
from pathlib import Path

# Ensure both product and core packages are importable in CI
HERE = Path(__file__).resolve()
PRODUCT_ROOT = HERE.parents[2]  # products/sigma-lab
CORE_ROOT = PRODUCT_ROOT.parent / 'sigma-core'
for p in (PRODUCT_ROOT, CORE_ROOT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

