import json
from main_engine import CredibilityEngine
from credibility_updater import IncrementalUpdater

if __name__ == "__main__":

    eng = CredibilityEngine()

    eng.ingest_text("sourceA", "Our CEO, Jane Smith, is a world-renowned cybersecurity expert.", {"type": "investor_presentation", "domain": "company.com","declared_conflict": True})
    eng.ingest_file("sourceB", "Data/market_report.txt", {"type": "licensed_database", "domain": "pitchbook.com"})
    # eng.ingest_file("sourceC", "Data/Investor_Pitch.pdf", {"type": "investor_presentation", "domain": "company.com", "declared_conflict": True})
    # eng.ingest_file("sourceD", "Data/Research_Study.docx", {"type": "peer_reviewed", "domain": "nature.com"})

    eng.rescore_incremental()
    # print("========PREVIOUS SCORE=========")
    print(json.dumps(eng.report(), indent=2))

    # eng.incremental_update(
    #     "sourceC",
    #     "Independent auditors reported revenue growth was 60% in FY2024.",
    #     {"type": "licensed_database", "domain": "pitchbook.com"}
    # )
    # print("========UPDATED SCORE=========")
    # print(json.dumps(eng.report(), indent=2))
