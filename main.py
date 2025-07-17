from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from utils import generate_code_from_prompt  # Ensure utils.py is in the same folder

app = FastAPI()

# ✅ Update this with your actual frontend domain when deployed to Netlify
ALLOWED_ORIGINS = [
    "http://localhost:3000",                # Local dev
    "https://dancing-mousse-c5c6d5.netlify.app",        # Replace with your Netlify domain
]

# ✅ CORS for frontend (dev + prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request message schema
class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class CodeRequest(BaseModel):
    messages: List[ChatMessage]

@app.post("/generate_code")
def generate_code(request: CodeRequest):
    try:
        code = generate_code_from_prompt(request.messages)
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating code: {str(e)}")

@app.get("/")
def health_check():
    return {"message": "CopyPaste.ai backend is live ✅"}
