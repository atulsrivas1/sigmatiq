"""
BracketGenerator — generate stop/target/time-stop at signal-time (no look-ahead).

Usage:
    from bracket_generator import Params, generate_brackets
    params = Params(mode="atr", atr_mult_stop=1.2, atr_mult_target=2.0, time_stop_days=10)
    out = generate_brackets({"entry_px": 100.0, "atr_14": 2.5}, params)

Notes:
- Modes:
    * "atr"            -> equity-style ATR multiples
    * "premium"        -> options premium % move
    * "underlying_atr" -> map underlying ATR to premium via delta
    * "ml"             -> use model-provided fields: ml_stop_px/ml_target_px
- Paper Broker enforces OCO & time stops; backtests must mirror logic (parity).
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Params:
    mode: str = "atr"                # 'atr'|'premium'|'underlying_atr'|'ml'
    atr_mult_stop: float = 1.2
    atr_mult_target: float = 2.0
    premium_stop_pct: float = 0.35   # 35% drop from premium for stop
    premium_target_pct: float = 0.75 # 75% rise for target
    time_stop_minutes: Optional[int] = None
    time_stop_days: Optional[int] = None
    force_flat_time: Optional[str] = None   # 'HH:MM' (exchange local)
    trailing: bool = False
    trail_mode: Optional[str] = None        # e.g., 'atr'
    trail_mult: Optional[float] = None

def generate_brackets(row: Dict[str, Any], params: Params) -> Dict[str, Any]:
    mode = (params.mode or "atr").lower()
    out: Dict[str, Any] = {"enabled": True, "mode": mode}

    if mode == "atr":
        entry_px = row.get("entry_px", row.get("close"))
        atr = row.get("atr_14") or row.get("atr")
        if entry_px is None or atr is None:
            raise ValueError("ATR mode requires 'entry_px' (or 'close') and 'atr_14'.")
        out["stop_px"] = float(entry_px) - float(params.atr_mult_stop) * float(atr)
        out["target_px"] = float(entry_px) + float(params.atr_mult_target) * float(atr)

    elif mode == "premium":
        premium = row.get("premium") or row.get("option_price")
        if premium is None:
            raise ValueError("Premium mode requires 'premium' (option price).")
        out["stop_premium"]   = float(premium) * (1.0 - float(params.premium_stop_pct))
        out["target_premium"] = float(premium) * (1.0 + float(params.premium_target_pct))

    elif mode == "underlying_atr":
        und_px = row.get("underlying_price")
        und_atr = row.get("underlying_atr_14") or row.get("atr_14")
        premium = row.get("premium") or row.get("option_price")
        delta = abs(float(row.get("delta", 0.5)))
        if und_px is None or und_atr is None or premium is None:
            raise ValueError("Underlying ATR mode requires 'underlying_price', 'underlying_atr_14', and 'premium'.")
        move_stop = float(params.atr_mult_stop) * float(und_atr)
        move_tgt  = float(params.atr_mult_target) * float(und_atr)
        # First-order premium change approximation using delta
        out["stop_premium"]   = max(0.0, float(premium) - delta * move_stop)
        out["target_premium"] = float(premium) + delta * move_tgt

    elif mode == "ml":
        out["stop_px"]   = row.get("ml_stop_px")
        out["target_px"] = row.get("ml_target_px")
        if out["stop_px"] is None or out["target_px"] is None:
            raise ValueError("ML mode expects 'ml_stop_px' and 'ml_target_px' in the row.")

    else:
        raise ValueError(f"Unknown mode: {mode}")

    # Optional time stops / force-flat
    if params.time_stop_minutes is not None:
        out["time_stop_minutes"] = int(params.time_stop_minutes)
    if params.time_stop_days is not None:
        out["time_stop_days"] = int(params.time_stop_days)
    if params.force_flat_time:
        out["force_flat_time"] = params.force_flat_time

    # Optional trailing metadata (handled by runtime)
    if params.trailing:
        out["trailing"] = True
        if params.trail_mode:
            out["trail_mode"] = params.trail_mode
        if params.trail_mult is not None:
            out["trail_mult"] = float(params.trail_mult)

    return out

if __name__ == "__main__":
    # Minimal self-check
    ex = {"entry_px": 100.0, "atr_14": 2.5}
    p = Params(mode="atr", atr_mult_stop=1.2, atr_mult_target=2.0, time_stop_days=10)
    print(generate_brackets(ex, p))
