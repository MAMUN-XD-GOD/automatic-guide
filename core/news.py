import random

# ----------------------
# Fetch Market News
# ----------------------
def fetch_market_news():
    """
    Returns list of latest market news
    Each item:
    - headline
    - impact_score (1-10)
    - source
    """
    # Placeholder / dummy news example
    # Can replace with real API like Investing.com, Yahoo Finance, etc.
    news_list = [
        {"headline":"USD rallies after NFP report", "impact_score":7, "source":"Reuters"},
        {"headline":"Gold drops amid weak demand", "impact_score":5, "source":"Bloomberg"},
        {"headline":"Bitcoin price breaks $40k", "impact_score":6, "source":"CoinDesk"},
        {"headline":"Oil prices steady ahead of OPEC meeting", "impact_score":4, "source":"CNBC"},
        {"headline":"Euro strengthens on ECB comments", "impact_score":5, "source":"Investing.com"}
    ]

    # Randomly shuffle and pick top 3
    random.shuffle(news_list)
    return news_list[:3]

# ----------------------
# Get Latest News Score → for Probability
# ----------------------
def get_latest_news_score(market, pair):
    """
    Return numeric score based on latest news impact.
    Positive score for favorable news, negative for unfavorable.
    """
    news_data = fetch_market_news()
    score = 0
    for news in news_data:
        # Example: simple weighting
        if pair in news["headline"] or market in news["headline"].lower():
            score += news["impact_score"]
    # Normalize
    score = max(-10, min(10, score))
    return score
