from fastapi import FastAPI, HTTPException
from fastapi import APIRouter
from pydantic import BaseModel
import uuid
import google.generativeai as genai

app = APIRouter()

# Configure GenAI
token = "AIzaSyDoODWms5gtz32k1gH5wr2Ti1f9z7w_0xc"
genai.configure(api_key=token)
model = genai.GenerativeModel("gemini-1.5-flash")

# Session storage
sessions = {}

class UserInput(BaseModel):
    session_id: str
    message: str

class SessionStartResponse(BaseModel):
    session_id: str
    assistant_response: str

@app.post("/start", response_model=SessionStartResponse)
async def start_session():
    session_id = str(uuid.uuid4())
    initial_message = (
        "👋 Welcome to IT Visionary Solutions! I'm your AI assistant. How can I help you today?\n\n"
        "You can ask about:\n"
        "- Network optimization strategies\n"
        "- Multi-cloud management\n"
        "- Zero-trust security\n"
        "- AI-powered efficiency\n"
        "Type your questions or describe your IT challenges below!"
    )
    system_prompt = (
    "You are the official AI assistant of IT Visionary Solutions, a premier technology consultancy "
    "specializing in digital transformation and cutting-edge IT solutions. Your role is to embody our "
    "core services:\n\n"
    "1. **Strategic Technology Consulting**: Guide enterprises through cloud adoption (AWS/Azure/GCP), "
    "legacy system modernization, and IT infrastructure optimization\n"
    "2. **Cybersecurity Excellence**: Advise on Zero Trust Architecture, SOC operations, and compliance "
    "(GDPR/HIPAA/PCI-DSS) implementations\n"
    "3. **Enterprise Solutions**: Design AI/ML integration strategies, IoT implementations, and "
    "data-driven decision systems\n"
    "4. **Managed Services**: Offer insights on 24/7 infrastructure monitoring, proactive maintenance, "
    "and SLA-driven support models\n\n"
    "Response Guidelines:\n"
    "- Maintain our brand voice: Innovative ∙ Technical Precision ∙ Client-Centric\n"
    "- Reference our methodology: Technology Alignment Framework (TAF™)\n"
    "- Highlight differentiators: Certified Solution Architects ∙ Vendor-Neutral Advice ∙ ROI-Focused Planning\n"
    "- Use technical depth while remaining accessible\n"
    "- Always offer to connect with human experts (Solution Architects/CTO Office) when needed"
)
    sessions[session_id] = {
        "conversation_history": [
            f"System: {system_prompt}",
            f"Assistant: {initial_message}"
        ],
        "active": True
    }
    
    return {
        "session_id": session_id,
        "assistant_response": initial_message
    }

@app.post("/chat")
async def chat(user_input: UserInput):
    session_id = user_input.session_id
    message = user_input.message.strip()
    
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    if not session["active"]:
        return {"assistant_response": "This session has ended. Please start a new session.", "session_id": session_id}
    
    session["conversation_history"].append(f"User: {message}")
    
    try:
        prompt = "\n".join(session["conversation_history"]) + "\nAssistant:"
        response = model.generate_content(prompt).text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    session["conversation_history"].append(f"Assistant: {response}")
    
    return {"assistant_response": response, "session_id": session_id}