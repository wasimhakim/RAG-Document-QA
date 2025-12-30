from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/")
def redirect_to_health():
  return RedirectResponse(url="/health")

@app.get("/health")
async def root():
  return { "message": "Hello I am working :)"}