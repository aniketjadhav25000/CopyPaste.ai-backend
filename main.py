from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from utils import generate_code_from_prompt

app = FastAPI()

# ✅ Allow CORS for localhost + Netlify + any others you need
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://dancing-mousse-c5c6d5.netlify.app",  # your Netlify frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route for health check
@app.get("/")
def read_root():
    return {"message": "AI backend is live!"}

# ✅ Message structure
class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class CodeRequest(BaseModel):
    messages: List[ChatMessage]

# ✅ Code generation route
@app.post("/generate_code")
def generate_code(request: CodeRequest):
    try:
        code = generate_code_from_prompt(request.messages)
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
