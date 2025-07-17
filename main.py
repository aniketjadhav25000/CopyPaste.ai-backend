from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from utils import generate_code_from_prompt  # Make sure this exists
import logging

app = FastAPI()

# ✅ Set up logging for debugging (especially helpful on mobile issues)
logging.basicConfig(level=logging.INFO)

# ✅ CORS Setup: Temporary allow all for mobile/device compatibility testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔁 TEMP: Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Schemas
class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class CodeRequest(BaseModel):
    messages: List[ChatMessage]

# ✅ Health Check
@app.get("/")
def root():
    return {"message": "AI backend is live!"}

# ✅ AI Code Generator Endpoint
@app.post("/generate_code")
async def generate_code(request: CodeRequest):
    try:
        # Log full incoming request for debugging
        logging.info("Received messages: %s", request.messages)

        # Optional validation
        if not request.messages or not isinstance(request.messages, list):
            raise HTTPException(status_code=400, detail="Invalid message format")

        code = generate_code_from_prompt(request.messages)
        return {"code": code}

    except Exception as e:
        logging.error("Error during code generation: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
