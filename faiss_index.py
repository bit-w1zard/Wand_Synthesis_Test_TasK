import faiss
import numpy as np
from config import EMB_DIM

class FaissIndex:
    """
    FAISS vector index with incremental storage, Handles dtype conversions and empty states.
    """
    def __init__(self):
        self.index = faiss.IndexFlatIP(EMB_DIM)
        self.embeddings = []  

    def add(self, vecs):
        vecs = np.asarray(vecs, dtype=np.float32)
        if vecs.ndim == 1:
            vecs = vecs.reshape(1, -1)
        self.index.add(vecs)
        self.embeddings.append(vecs)

    def search(self, vec, top_k=5):
        if self.index.ntotal == 0:
            return np.array([[]], dtype=np.float32), np.array([[]], dtype=np.int64)
        vec = np.asarray(vec, dtype=np.float32)
        if vec.ndim == 1:
            vec = vec.reshape(1, -1)
        return self.index.search(vec, top_k)

    def all_embeddings(self):
        if not self.embeddings:
            return np.zeros((0, EMB_DIM), dtype=np.float32)
        return np.vstack(self.embeddings)
