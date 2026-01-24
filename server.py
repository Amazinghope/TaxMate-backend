from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
import os 
from dotenv import load_dotenv
import openai
from prompt.prompts_builder import build_prompt
from prompt.guardrails import validate_message
from prompt.mock_engine import generate_mock_reply
from core.constants import VALID_MODES, VALID_PERSONAS
import time
import json 
from pathlib import Path

# Path to popular_topics.json file
TOPICS_PATH = Path("rulesets/popular_topics.json")

def get_popular_topics():
    """Load popular topics from JSON and return as a list"""
    if not TOPICS_PATH.exists():
        return []
    data = json.loads(TOPICS_PATH.read_text())
    return data.get("topics", [])


# - OPENAI API KEY SETUP 
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# FASTAPI APP 
app = FastAPI(title="TaxSense MVP Backend")
print("TaxMate backend booted successfully")

@app.get("/")
def root():
    return {"message": "TaxSense Backend is running!"}


#cors config
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   
        "https://tax-sense.vercel.app"   
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# limit-handler
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please slow down."}
    )

#  in-memory session storage
SESSIONS = {}
SESSION_TTL = 60 * 30

# REQUEST MODEL
class SessionStartRequest(BaseModel):
    persona: str = "generic"
    mode: str = "standard"   # frontend can set: standard, eli5, pidgin, hybrid


class SessionUpdateRequest(BaseModel):
    session_id: str
    persona: str
    mode: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

    # API Endpoints
@app.get("/topics")
def popular_topics():
    """Return popular topics so frontend can display them"""
    return {"topics": get_popular_topics()}

    
@app.post("/session/start")

def start_session(req: SessionStartRequest):
    session_id = str(uuid.uuid4())

    mode = req.mode.lower()
    persona = req.persona.lower()

    if mode not in VALID_MODES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid mode. Choose one of {sorted(VALID_MODES)}"
        )

    if persona not in VALID_PERSONAS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid persona. Choose one of {sorted(VALID_PERSONAS)}"
        )

    SESSIONS[session_id] = {
        "persona": persona,
        "mode": mode,
        "created_at": time.time()
    }

    return {
        "session_id": session_id,
        "persona": persona,
        "mode": mode,
    }



@app.post("/session/update")
def update_session(req: SessionUpdateRequest):
    session = SESSIONS.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if req.mode:
        mode = req.mode.lower()
        if mode not in VALID_MODES:
            raise HTTPException(status_code=400, detail="Invalid mode")
        session["mode"] = mode

    if req.persona:
        persona = req.persona.lower()
        if persona not in VALID_PERSONAS:
            raise HTTPException(status_code=400, detail="Invalid persona")
        session["persona"] = persona

    return {"status": "ok"}



@app.post("/chat")
@limiter.limit("8/minute")
def chat(request: Request, req: ChatRequest):
    session = SESSIONS.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Session expiry
    if time.time() - session["created_at"] > SESSION_TTL:
        del SESSIONS[req.session_id]
        raise HTTPException(
            status_code=401,
            detail="Session expired. Please start a new session."
        )

    # Refresh activity timestamp
    session["created_at"] = time.time()

    # Guardrails
    if not validate_message(req.message):
        return {
            "reply": "Sorry, I cannot answer questions about calculations, filing, or uploads."
        }

    persona = session.get("persona", "generic").lower()
    mode = session.get("mode", "standard").lower()

    print(f"[CHAT] persona={persona} mode={mode} msg='{req.message}'")

    prompt = build_prompt(session, req.message)

    # OpenAI path
    if openai.api_key:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            return {"reply": response.choices[0].message.content.strip()}

        except Exception as e:
            print(f"[OPENAI ERROR] {e}")

    # Mock fallback 
    try:
        return {"reply": generate_mock_reply(persona, mode, req.message)}
    except Exception as e:
        print(f"[MOCK ERROR] {e}")
        raise HTTPException(
            status_code=500,
            detail="Service temporarily unavailable. Please try again."
        )

