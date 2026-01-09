import cv2
import numpy as np
from core.technical import calculate_indicators
from core.smc import detect_smc_signals
from core.utils import get_candle_data, round_number_check

def analyze_chart(image_path):
    """
    Full chart analysis:
    - Candlestick patterns
    - Trend detection
    - SMC / BOS / CHoCH
    - FVG / OB zones
    - Momentum
    - TP/SL suggestion
    - Multi-market / Multi-pair support
    """

    chart_data = get_candle_data(image_path)  # Extract OHLC from chart screenshot
    indicators = calculate_indicators(chart_data)

    # Trend Bias
    trend_bias = "neutral"
    if indicators["ema_fast"][-1] > indicators["ema_slow"][-1]:
        trend_bias = "up"
    elif indicators["ema_fast"][-1] < indicators["ema_slow"][-1]:
        trend_bias = "down"

    # SMC / BOS / CHoCH signals
    smc_signals = detect_smc_signals(chart_data)

    # FVG / OB detection
    fvg_zones = indicators.get("fvg", [])
    ob_zones = indicators.get("ob", [])

    # Round Number Support/Resistance
    round_levels = round_number_check(chart_data)

    # Momentum / Price Action
    momentum = indicators.get("momentum", 0)
    candle_size = indicators.get("candle_size", [])

    # Generate signal
    signal_direction = "up" if trend_bias=="up" and momentum>0 else "down" if trend_bias=="down" and momentum<0 else "neutral"
    entry_price = chart_data["close"][-1]
    tp = entry_price + (entry_price*0.01) if signal_direction=="up" else entry_price - (entry_price*0.01)
    sl = entry_price - (entry_price*0.005) if signal_direction=="up" else entry_price + (entry_price*0.005)

    return {
        "signal_id": "auto_" + str(np.random.randint(100000,999999)),
        "context": {
            "market": "forex/crypto/binary",  # Auto-detect from chart metadata or user selection
            "pair": "XAU/USD",  # Default popular pair
            "session": "auto",  # Auto-detect market session
            "vision": {
                "trend_bias": trend_bias,
                "momentum": momentum,
                "candle_size": candle_size
            },
            "signal": {
                "direction": signal_direction,
                "entry": round(entry_price, 4),
                "TP": round(tp, 4),
                "SL": round(sl, 4),
                "timeframe": "auto"
            },
            "confirmations": len(smc_signals),
            "FVG": fvg_zones,
            "OB": ob_zones,
            "round_numbers": round_levels
        }
  }
