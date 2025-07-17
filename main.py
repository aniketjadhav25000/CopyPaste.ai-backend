from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from utils import generate_code_from_prompt

app = FastAPI()

# ✅ Secure and flexible CORS for Netlify + localhost
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https://.*\.netlify\.app|http://localhost:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Message schema
class ChatMessage(BaseModel):
    role: str
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
