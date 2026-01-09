import json
import os

FEEDBACK_FILE = "temp_uploads/feedback.json"

# ----------------------
# Record Feedback
# ----------------------
def record_feedback(signal_id, market, pair, result):
    feedback_list = []
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            feedback_list = json.load(f)

    feedback_entry = {
        "signal_id": signal_id,
        "market": market,
        "pair": pair,
        "result": result  # "win" or "loss"
    }

    feedback_list.append(feedback_entry)

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback_list, f, indent=2)

# ----------------------
# Compute Overall Accuracy
# ----------------------
def compute_accuracy():
    if not os.path.exists(FEEDBACK_FILE):
        return 0

    with open(FEEDBACK_FILE, "r") as f:
        feedback_list = json.load(f)

    if not feedback_list:
        return 0

    wins = sum(1 for fb in feedback_list if fb["result"]=="win")
    total = len(feedback_list)
    return round((wins/total)*100,1)

# ----------------------
# Market/Pair Stats
# ----------------------
def get_feedback_stats():
    if not os.path.exists(FEEDBACK_FILE):
        return {}

    with open(FEEDBACK_FILE, "r") as f:
        feedback_list = json.load(f)

    stats = {}
    for fb in feedback_list:
        key = f"{fb['market']}_{fb['pair']}"
        if key not in stats:
            stats[key] = {"win":0, "loss":0, "accuracy":0}
        stats[key][fb["result"]] +=1
        stats[key]["accuracy"] = round((stats[key]["win"]/(stats[key]["win"]+stats[key]["loss"]))*100,1)

    return stats

# ----------------------
# Get Signal History → for Probability
# ----------------------
def get_signal_history(entry_price, market, pair):
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r") as f:
        feedback_list = json.load(f)

    history = [fb["result"] for fb in feedback_list if fb["market"]==market and fb["pair"]==pair]
    return history
