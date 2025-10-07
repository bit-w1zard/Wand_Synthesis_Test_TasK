"""
- Loads Sentence Transformer Lightweight Model, Embedding model all-MiniLM-L6-v2 returns 384 dimentional vectors.
- Assigns Static Weights to each Source Type.
- Assigns Static Weights to each Domain based on Generic Authencity.
- Assigns Static Threshold values to Signal Actions
"""

EMB_MODEL = "all-MiniLM-L6-v2"
EMB_DIM = 384

SOURCE_TYPE = {
    "academic_paper": 80,
    "peer_reviewed": 90,
    "government_report": 85,
    "independent_research": 80,
    "news_outlet": 60,
    "industry_report": 55,
    "investor_presentation": 40,
    "press_release": 45,
    "commercial_ad": 20,
    "social_media": 25,
    "licensed_database": 75,
    "unknown": 50
}

DOMAIN_REPUTATION = {
    "nature.com": 95,
    "sciencedirect.com": 90,
    "pitchbook.com": 85,
    "company.com": 40,
    "forbes.com": 75,
    "twitter.com": 30
}

THRESHOLDS = {
    "remove": 40,
    "warn": 75
}

