from sentence_transformers import SentenceTransformer

class Transformer:
  model: SentenceTransformer
  chunks: list
  data = []

  def __init__(self, chunks: list):
    self.model = SentenceTransformer("all-MiniLM-L6-v2")
    self.chunks = chunks
    if len(chunks) == 0:
      return None
    
  def embed_chunks(self):
    lines = [c["text"] for c in self.chunks]
    vectors = self.model.encode(lines)

    for i, vector in enumerate(vectors):
      self.data.append({
        "vector": vector.tolist(),
        "text": self.chunks[i]['text'],
        "sections": self.chunks[i]['sections']
      })

  def get_data(self) -> list:
    return self.data


