from fastapi import FastAPI, UploadFile
from fastapi.responses import RedirectResponse
from services.process_pdf import ProcessPDF
from services.transformer import Transformer
from services.ask import Ask

app = FastAPI()

@app.get("/")
def redirect_to_health():
  return RedirectResponse(url="/health")

@app.get("/health")
async def root():
  return { "message": "Hello I am working :)"}

@app.post("/upload")
async def upload(file: UploadFile):

  process_pdf = ProcessPDF(file)
  chunks = process_pdf.get_chunks()

  transformer = Transformer(chunks)
  query = "What is the applicant name?"
  data = transformer.search(query)

  context = ""
  for item in data:
    context += item["text"] + " "

  response = Ask().question(query, context)

  return { "data": response }