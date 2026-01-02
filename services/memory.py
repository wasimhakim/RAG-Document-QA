import faiss
import numpy as np

class Memory:
  DIM = 384 # sentence transformer embeddings
  index = faiss.IndexFlatL2(DIM)
  chunks = []

  def store(self, vectors, chunks):
    self.chunks = chunks
    embeddings = np.array(vectors, dtype=np.float32)
    self.index.add(embeddings)

  def search(self, query_vectors, k = 5):
    query_embeddings = np.array([query_vectors], dtype=np.float32)
    D, I = self.index.search(query_embeddings, k)

    metadata = []
    for idx in I[0]:
      metadata.append(self.chunks[idx])
    return metadata

