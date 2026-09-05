from fastapi import FastAPI, Response
import requests
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import asyncio
import os
import json
from pipeline import run_pipeline
from anthropic import Anthropic
from prismtrace.claude_tracer import ClaudeAgentTracer

app = FastAPI()

@app.post("/api/analyze")
async def analyze():
    result = await run_pipeline()
    return result

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]

@app.post("/api/chat")
async def chat(request: ChatRequest):
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    tracer = ClaudeAgentTracer(client, api_key=os.environ.get("PRISMTRACE_API_KEY"), project_id="f801d3ca-24a6-4561-ab94-65c0018b5cfa", agent_name="chat-agent")
    tracer.instrument_client()
    
    # Read the latest run data as context
    run_context = "No run data available yet."
    if os.path.exists("run_data.json"):
        try:
            with open("run_data.json", "r") as f:
                run_context = f.read()
        except:
            pass

    system_prompt = f"""
    You are a customer service AI assistant helping a customer with Financial Planning & Analysis (FP&A).
    You are helping the customer analyze the financial changes for this quarter.
    Answer their questions intelligently, concisely, and professionally based ONLY on the following run data payload.
    
    IMPORTANT FORMATTING RULES:
    - DO NOT use ANY markdown formatting (no asterisks, no bolding, no special characters).
    - Output pure plain text only.
    - Use simple line breaks (newlines) to separate paragraphs.
    - If you need to make a list, just use standard dashes or numbers without any bolding.
    
    <run_data>
    {run_context}
    </run_data>
    """
    
    messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
    
    try:
        # Use Sonnet for chat
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )
        
        reply_text = "".join(block.text for block in response.content if hasattr(block, 'text'))
        return {"reply": reply_text}
    except Exception as e:
        return {"error": str(e)}

class TTSRequest(BaseModel):
    text: str

@app.post("/api/tts")
async def tts(request: TTSRequest):
    # Use the ElevenLabs API key from the environment
    key = os.environ.get("ELEVENLABS_API_KEY", "")
    headers = {
        "xi-api-key": key,
        "Content-Type": "application/json"
    }
    data = {
        "text": request.text,
        "model_id": "eleven_multilingual_v2"
    }
    try:
        # Send request to ElevenLabs (we run this synchronously since it's a simple requests call, 
        # but in production we'd use httpx for async)
        response = requests.post(
            "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM", 
            headers=headers, 
            json=data,
            stream=True
        )
        if response.status_code == 200:
            return Response(content=response.content, media_type="audio/mpeg")
        else:
            return Response(content=f"Error {response.status_code}: {response.text}", status_code=500)
    except Exception as e:
        return Response(content=str(e), status_code=500)

# Serve static files for the frontend, falling back to index for .html
app.mount("/", StaticFiles(directory="Explain the Change prototype", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
