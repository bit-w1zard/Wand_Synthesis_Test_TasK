import numpy as np
from sentence_transformers import SentenceTransformer
from config import EMB_MODEL

class Embedder:
    """
    Wrapper around SentenceTransformer with normalization.
    """
    def __init__(self):
        self.model = SentenceTransformer(EMB_MODEL)

    def encode(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        embs = self.model.encode(texts, convert_to_numpy=True)
        embs = self._normalize(embs)
        return embs.astype(np.float32)

    def _normalize(self, vecs):
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        return vecs / np.clip(norms, 1e-8, None)
