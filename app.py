from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
from pipeline import run_pipeline

app = FastAPI()

@app.post("/api/analyze")
async def analyze():
    result = await run_pipeline()
    return result

# Serve static files for the frontend, falling back to index for .html
app.mount("/", StaticFiles(directory="Explain the Change prototype", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
