from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from services.process_pdf import ProcessPDF
from services.transformer import Transformer
from services.llm_service import LLMService
from services.memory import Memory

app = FastAPI()
memory = Memory()
transformer = Transformer()
llm = LLMService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def redirect_to_health():
  return RedirectResponse(url="/health")

@app.get("/health")
async def root():
  return { "message": "Hello I am working :)"}

@app.post("/upload")
async def upload(file: UploadFile):
  memory.index.reset()

  process_pdf = ProcessPDF(file)
  chunks = process_pdf.get_chunks()

  embeddings = transformer.encode_chunks(chunks)
  memory.store(embeddings, chunks)

  return { "message": "File Uploaded Successfully!"}

@app.get("/ask")
async def ask(query: str):
  query_vectors = transformer.encode_query(query)
  data = memory.search(query_vectors)

  context = ""
  for item in data:
    context += item["text"] + " "

  response = llm.question(query, context)

  return { "data": response }