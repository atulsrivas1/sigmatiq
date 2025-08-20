from __future__ import annotations
import sys
import os
import argparse
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', default='0.0.0.0')
    ap.add_argument('--port', type=int, default=8001)
    ap.add_argument('--reload', action='store_true')
    args = ap.parse_args()

    # Dev-only path hacks, gated by SIGMA_USE_PATH_HACKS
    if os.getenv('SIGMA_USE_PATH_HACKS', '1') in ('1','true','True'):
        here = Path(__file__).resolve()
        product_root = here.parents[1]
        core_root = product_root.parent / 'sigma-core'
        platform_root = product_root.parent / 'sigma-platform'
        for p in [product_root, core_root, platform_root]:
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))

    import uvicorn  # type: ignore
    uvicorn.run("api.app:app", host=args.host, port=args.port, reload=bool(args.reload))

if __name__ == '__main__':
    main()
