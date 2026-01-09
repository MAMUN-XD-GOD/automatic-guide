import cv2
import numpy as np

# ----------------------
# Extract OHLC from chart screenshot
# ----------------------
def get_candle_data(image_path):
    """
    Placeholder function:
    - Extract open, high, low, close lists from chart image
    - For full implementation, integrate OCR / image recognition
    """
    # For now, dummy data for testing / development
    n = 100
    close = np.cumsum(np.random.randn(n)) + 100
    open_ = close + np.random.randn(n)
    high = np.maximum(open_, close) + np.random.rand(n)
    low = np.minimum(open_, close) - np.random.rand(n)

    return {
        "open": list(open_),
        "high": list(high),
        "low": list(low),
        "close": list(close)
    }

# ----------------------
# Round Number Detection
# ----------------------
def round_number_check(chart_data, step=5):
    """
    Detect round number levels in chart
    step: e.g., 5 → every 5 units
    Returns list of levels
    """
    highs = chart_data["high"]
    lows = chart_data["low"]
    all_prices = highs + lows
    min_price = int(min(all_prices))
    max_price = int(max(all_prices))

    round_levels = [i for i in range(min_price, max_price+step, step)]
    return round_levels

# ----------------------
# Additional Helpers
# ----------------------
def normalize_signal(signal_value, min_val=0, max_val=100):
    """
    Normalize any signal/score to 0-100 range
    """
    return max(min_val, min(max_val, signal_value))

def calculate_tp_sl(entry, direction, percent_tp=1, percent_sl=0.5):
    """
    Calculate TP/SL prices
    """
    if direction=="up":
        tp = entry + entry*percent_tp/100
        sl = entry - entry*percent_sl/100
    elif direction=="down":
        tp = entry - entry*percent_tp/100
        sl = entry + entry*percent_sl/100
    else:
        tp = sl = entry
    return round(tp,4), round(sl,4)
