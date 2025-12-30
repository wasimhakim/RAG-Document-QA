import pymupdf
from fastapi import UploadFile

class ProcessPDF:
  data = ""

  def __init__(self, file: UploadFile):
    file_stream = file.file.read()
    if not file_stream:
      return None
    
    doc = pymupdf.open(stream=file_stream, filetype="pdf")
    for page in doc:
      self.data += page.get_text()

  def get_data(self):
    return self.data
  
  def _is_heading(self, line: str) -> bool:
    s = line.strip()
    return s.isupper() or s.endswith(":")
  
  def get_chunks(self):
    lines = [ln.strip() for ln in self.data.split("\n") if ln.strip()]

    chunks = []
    buf = []
    current_section = None

    for line in lines:
      if self._is_heading(line):
        if buf:
          chunks.append({
            "sections": current_section,
            "text": " ".join(buf)
          })
          buf = []
        current_section = line.rstrip(":")
      buf.append(line)
    
    if buf:
      chunks.append({
        "sections": current_section,
        "text": " ".join(buf)
      })
    
    return chunks

