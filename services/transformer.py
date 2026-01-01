import torch
from sentence_transformers import SentenceTransformer

class Transformer:
  model: SentenceTransformer
  chunks: list
  vectors: list
  data = []

  def __init__(self, chunks: list):
    self.model = SentenceTransformer("all-MiniLM-L6-v2")
    self.chunks = chunks
    if len(chunks) == 0:
      return None
    
    lines = [c["text"] for c in self.chunks]
    self.vectors = self.model.encode_document(lines, convert_to_tensor=True)

    for i, vector in enumerate(self.vectors):
      self.data.append({
        "vector": vector.tolist(),
        "text": self.chunks[i]['text'],
        "sections": self.chunks[i]['sections']
      })
  
  def search(self, query):
    query_vector = self.model.encode_query(query, convert_to_tensor=True)

    top_k = min(5, len(self.data))
    similarity_scores = self.model.similarity(query_vector, self.vectors)[0]
    scores, indices = torch.topk(similarity_scores, k=top_k)

    print(indices)

    result = []
    for index in indices:
      result.append(self.chunks[index])

    return result

  def get_data(self) -> list:
    return self.data


