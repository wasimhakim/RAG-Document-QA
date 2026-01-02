from sentence_transformers import SentenceTransformer
class Transformer:
  model = SentenceTransformer("all-MiniLM-L6-v2")
  vectors: list  

  def encode_chunks(self, chunks: list):
    if len(chunks) == 0:
      return None
    
    lines = [c["text"] for c in chunks]
    self.vectors = self.model.encode_document(lines)
    return self.vectors
  
  def encode_query(self, query: str):
    query_vector = self.model.encode_query(query)
    return query_vector


