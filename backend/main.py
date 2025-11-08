from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.adk.runners import Runner
from google.genai import types
from google.adk.sessions import InMemorySessionService
from my_agent.agent import root_agent
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "root-agent-app"
USER_ID = "test_user"
SESSION_ID = "root_session"

# Initialize ONE shared async session service
session_service = InMemorySessionService()

# Create the runner using that shared session service
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

# --- FastAPI setup ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Chrome extensions
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


async def ensure_session():
    """Ensure session exists for this user & session id."""
    existing_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    if not existing_session:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
            state={"initial_key": "initial_value"}
        )


async def chat_with_root(message: str):
    """Send message to root agent via runner."""
    print(f"\n>>> User: {message}")
    user_content = types.Content(role="user", parts=[types.Part(text=message)])

    final_response = "No response."
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text

    print(f"<<< Root Agent: {final_response}")
    return final_response



@app.get("/")
async def root():
    return {"Hello": "World"}


@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # Ensure a session exists before running
        await ensure_session()

        response = await chat_with_root(request.message)
        return {
            "status": "success",
            "response": response,
            "conversation_id": request.conversation_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "ok"} 