# RAG-Document-QA

Document Q&A API that ingests a PDF, builds sentence-transformer embeddings, retrieves relevant chunks with FAISS, and answers questions with an Ollama-hosted LLM.

## Features
- PDF text extraction and lightweight section-based chunking
- Sentence-transformer embeddings (all-MiniLM-L6-v2)
- FAISS vector search for top-k context
- FastAPI endpoints for upload and Q&A
- Local LLM inference via Ollama (qwen2.5:7b)

## Tech Stack
- FastAPI
- PyMuPDF
- sentence-transformers
- FAISS (faiss-cpu)
- Ollama

## Setup
1. Create and activate a virtual environment.
```bash
source .venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Ensure Ollama is installed and the model is available:
```bash
ollama pull qwen2.5:7b
```

## Run
```bash
fastapi dev main.py
```

The API will be available at `http://127.0.0.1:8000`.

## API
### Health
```http
GET /health
```
Response:
```json
{ "message": "Hello I am working :)" }
```

### Upload PDF
```http
POST /upload
```
Multipart form field:
- `file`: PDF file

Example:
```bash
curl -F "file=@/path/to/document.pdf" http://localhost:8000/upload
```

Response:
```json
{ "message": "File Uploaded Successfully!" }
```

### Ask a Question
```http
GET /ask?query=...
```
Example:
```bash
curl "http://localhost:8000/ask?query=What%20is%20the%20deadline%3F"
```

Response:
```json
{ "data": "..." }
```

## Notes
- Uploading a new PDF resets the in-memory FAISS index.
- Answers are constrained to retrieved context; if the answer is missing, the model is instructed to reply: `Not found in document.`
- CORS is configured for `http://localhost:5173` only.

## Project Structure
```
main.py
services/
  llm_service.py
  memory.py
  process_pdf.py
  transformer.py
```
