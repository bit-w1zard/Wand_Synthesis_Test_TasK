import re
from config import SOURCE_TYPE, DOMAIN_REPUTATION, THRESHOLDS

def heuristic_score(claim: str, meta: dict) -> float:
    """
    Calculate credibility score based on source type, domain and language hints.
    Args: claim ( original claim statement ), meta ( associated meta data )
    """
    base = SOURCE_TYPE.get(meta.get("type", "unknown"), 50)
    rep = DOMAIN_REPUTATION.get(meta.get("domain"), 50)
    score = base * 0.6 + rep * 0.4

    if re.search(r'\d', claim): score += 5
    if re.search(r'\b(may|might|possible|suggests?|could|potentially|likely)\b', claim, re.I): score -= 7
    if meta.get("declared_conflict"): score -= 15
    return score

def score_to_action(score: float) -> str:
    """
    Decide call to action based on credibility score.
    Args: score ( score value returned by heuristic_score function )
    """
    if score < THRESHOLDS["remove"]:
        return "remove"
    if score < THRESHOLDS["warn"]:
        return "warn"
    return "validate"
