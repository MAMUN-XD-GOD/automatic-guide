import pandas as pd
import numpy as np

# ----------------------
# Calculate Indicators
# ----------------------
def calculate_indicators(chart_data):
    """
    chart_data: dict with OHLC lists
    Returns: dict of indicators + momentum + candle size + FVG/OB zones
    """

    df = pd.DataFrame({
        "open": chart_data["open"],
        "high": chart_data["high"],
        "low": chart_data["low"],
        "close": chart_data["close"]
    })

    indicators = {}

    # EMA
    df['ema_fast'] = df['close'].ewm(span=10, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=25, adjust=False).mean()
    indicators["ema_fast"] = df['ema_fast'].tolist()
    indicators["ema_slow"] = df['ema_slow'].tolist()

    # RSI
    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))
    indicators["rsi"] = df['rsi'].fillna(50).tolist()

    # MACD
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    indicators["macd"] = df['macd'].tolist()
    indicators["macd_signal"] = df['signal'].tolist()

    # Bollinger Bands
    df['mbb'] = df['close'].rolling(window=20).mean()
    df['upper'] = df['mbb'] + 2*df['close'].rolling(20).std()
    df['lower'] = df['mbb'] - 2*df['close'].rolling(20).std()
    indicators["bollinger_upper"] = df['upper'].tolist()
    indicators["bollinger_lower"] = df['lower'].tolist()
    indicators["bollinger_middle"] = df['mbb'].tolist()

    # Candle size
    df['candle_size'] = df['high'] - df['low']
    indicators["candle_size"] = df['candle_size'].tolist()

    # Momentum
    df['momentum'] = df['close'] - df['close'].shift(1)
    indicators["momentum"] = df['momentum'].fillna(0).tolist()

    # FVG / OB zones placeholder
    indicators["fvg"] = []  # Can implement real detection logic later
    indicators["ob"] = []   # Order block detection

    return indicators
