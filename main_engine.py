from utils import sentence_split
from scoring import heuristic_score, score_to_action
from embeddings import Embedder
from faiss_index import FaissIndex          
from document_loader import extract_claims_from_file
from credibility_updater import IncrementalUpdater

class CredibilityEngine:
    """
    Main Pipeline Engine:  Ingestion -> Scoring -> Corroboration.
    """
    def __init__(self):
        self.embedder = Embedder()
        self.index = FaissIndex()
        self.claims = []

    def ingest_text(self, source_id, text, meta):
        """
        Directly Ingest Raw text into the Pipeline. 
        """
        claims = sentence_split(text)
        if claims:
            self._ingest_claims(source_id, claims, meta)

    def ingest_file(self, source_id, file_path, meta):
        claims = extract_claims_from_file(file_path)
        if claims:
            self._ingest_claims(source_id, claims, meta)

    def _ingest_claims(self, source_id, claims, meta):
        new_claims = [{"text": c, "source": source_id, "meta": meta} for c in claims]
        new_embs = self.embedder.encode([c["text"] for c in new_claims]) 
        self.index.add(new_embs)
        self.claims.extend(new_claims)

    def rescore_incremental(self, top_k=5):
        all_embs = self.index.all_embeddings()
        if all_embs.shape[0] == 0:
            return self.claims

        for i, claim in enumerate(self.claims):
            base = heuristic_score(claim["text"], claim["meta"])
            q = all_embs[i:i+1].astype("float32")
            D, I = self.index.search(q, top_k + 1)
            sims = [d for idx, d in zip(I[0], D[0]) if idx != i]
            max_sim = max(sims) if sims else 0

            if max_sim > 0.85: base += 20
            elif max_sim > 0.60: base += 10
            elif max_sim > 0.40: base += 5
            else: base -= 2

            claim["score"] = round(min(max(base, 0), 100), 1)
            claim["action"] = score_to_action(claim["score"])

        return self.claims

    def report(self):
        return [
            {
                "text": c["text"],
                "source": c["source"],
                "score": c.get("score"),
                "action": c.get("action"),
            }
            for c in self.claims
        ]
        
    def incremental_update(self, new_source_id, new_text, meta):
        """
        Ingest new claims and incrementally update existing claims based on vector search.
        """
        new_claims = [{"text": c, "source": new_source_id, "meta": meta} 
                    for c in sentence_split(new_text)]
        if not new_claims:
            return []

        new_embs = self.embedder.encode([c["text"] for c in new_claims])
        self.index.add(new_embs)
        self.claims.extend(new_claims)

        updater = IncrementalUpdater(self.embedder, self.index, self.claims)
        updated_claims = updater.update_with_new_claims(new_claims)

        for claim in self.claims:
            if "score" in claim:
                claim["action"] = score_to_action(claim["score"])

        return updated_claims