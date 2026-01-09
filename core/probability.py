import math
from core.feedback import get_signal_history
from core.news import get_latest_news_score

def compute_signal_probability(context):
    """
    Compute AI probability score for a given signal.
    Weighted by:
    - Trend confirmation
    - SMC/BOS/CHoCH signals
    - Momentum strength
    - Candle structure
    - News impact
    - Past signal history (feedback)
    """

    base_prob = 50  # Start at neutral 50%

    # Trend confirmation
    trend = context["vision"]["trend_bias"]
    if trend == "up":
        base_prob += 15
    elif trend == "down":
        base_prob -= 15

    # Momentum
    momentum = context["vision"].get("momentum", 0)
    base_prob += math.tanh(momentum) * 10  # Scaled momentum influence

    # Candle size influence
    candle_size = context["vision"].get("candle_size", [])
    if len(candle_size) > 0:
        avg_size = sum(candle_size[-5:])/5
        base_prob += min(avg_size*2, 10)  # max 10% influence

    # SMC / BOS / CHoCH confirmation
    confirmations = context.get("confirmations", 0)
    base_prob += min(confirmations*5, 20)  # max 20% influence

    # News impact
    news_score = get_latest_news_score(context["market"], context["pair"])
    base_prob += news_score  # news_score can be negative or positive

    # Past feedback influence
    history = get_signal_history(context["signal"]["entry"], context["market"], context["pair"])
    if history:
        wins = sum(1 for h in history if h=="win")
        losses = sum(1 for h in history if h=="loss")
        feedback_score = (wins - losses)/max(len(history),1)*10
        base_prob += feedback_score

    # Clamp between 0–100%
    base_prob = max(0, min(100, round(base_prob,1)))

    return base_prob
