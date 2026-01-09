def detect_smc_signals(chart_data):
    """
    Detect SMC signals:
    - Break of Structure (BOS)
    - Change of Character (CHoCH)
    - Supply/Demand zones
    Returns: list of confirmations (each counts +1 for probability)
    """

    closes = chart_data["close"]
    highs = chart_data["high"]
    lows = chart_data["low"]

    confirmations = []

    # Simple BOS/CHoCH detection (advanced logic can be expanded)
    for i in range(2, len(closes)-1):
        # Break of Structure Up
        if closes[i] > max(closes[i-2:i]):
            confirmations.append("BOS_up")
        # Break of Structure Down
        if closes[i] < min(closes[i-2:i]):
            confirmations.append("BOS_down")
        # Change of Character (CHoCH)
        if closes[i] > closes[i-1] and closes[i-1] < closes[i-2]:
            confirmations.append("CHoCH_up")
        if closes[i] < closes[i-1] and closes[i-1] > closes[i-2]:
            confirmations.append("CHoCH_down")

    # Supply/Demand zones placeholder
    # For advanced: detect FVG/OB zones and tag as confirmations
    # Can link with indicators['fvg'] and indicators['ob'] in analyzer.py

    return confirmations
