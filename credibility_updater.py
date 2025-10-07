import re
import numpy as np
import datetime
from scoring import heuristic_score

class IncrementalUpdater:
    """
    Incrementally update credibility based on corroboration/contradiction.
    """

    def __init__(self, embedder, index, claims):
        self.embedder = embedder
        self.index = index
        self.claims = claims

    def update_with_new_claims(self, new_claims, top_k=5):
        """
        Update weights of old claims if they are influenced by new claims. 
        Args: new_claims ( new claims via Input ), top_k ( Returns the number of similarity matches )
        """
        new_texts = [c["text"] for c in new_claims]
        new_vecs = self.embedder.encode(new_texts) 

        updated_claims = []

        if self.index.index.ntotal == 0:
            return updated_claims

        for i, new_vec in enumerate(new_vecs):
            new_claim = new_claims[i]
            q = np.ascontiguousarray(new_vec.reshape(1, -1).astype(np.float32))
            D, I = self.index.search(q, top_k)
            corroboration_boost = 0
            contradiction_penalty = 0

            for idx, sim in zip(I[0], D[0]):
                if idx < 0 or idx >= len(self.claims):
                    continue

                old_claim = self.claims[idx]
                old_score = float(old_claim.get("score", heuristic_score(old_claim["text"], old_claim["meta"])))

                contradicts = self._detect_contradiction(old_claim["text"], new_claim["text"])

                if sim > 0.85:
                    if contradicts:
                        old_claim["contradiction_count"] = old_claim.get("contradiction_count", 0) + 1
                        contradiction_penalty += 15
                    else:
                        old_claim["corroboration_count"] = old_claim.get("corroboration_count", 0) + 1
                        corroboration_boost += 15
                elif sim > 0.60:
                    corroboration_boost += 7

                old_claim["last_updated"] = datetime.datetime.utcnow().isoformat() + "Z"

                new_score = old_score + corroboration_boost - contradiction_penalty
                old_claim["score"] = round(min(max(new_score, 0), 100), 1)

                updated_claims.append(old_claim)

        return updated_claims

    def _detect_contradiction(self, old_text, new_text):
        """
        Checks if a new claim contradicts older claims based on numerical difference or negative words.
        Args: old_text ( old claims text ), new_text ( new claims text )
        """
        nums_old = re.findall(r"\d+\.?\d*", old_text)
        nums_new = re.findall(r"\d+\.?\d*", new_text)
        if nums_old and nums_new:
            try:
                old_v = float(nums_old[0])
                new_v = float(nums_new[0])
                if old_v != 0 and abs(old_v - new_v) / abs(old_v) > 0.4:
                    return True
            except:
                pass

        neg_words = ["not", "no", "never", "false", "incorrect"]
        if any(w in new_text.lower() for w in neg_words) and not any(w in old_text.lower() for w in neg_words):
            return True

        return False
