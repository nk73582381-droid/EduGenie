import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from google import genai


# Load .env file
load_dotenv()

# Gemini client
client = genai.Client()

# FastAPI app
app = FastAPI(title="EduGenie")


# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML templates
templates = Jinja2Templates(directory="templates")


# Request model
class AIRequest(BaseModel):
    prompt: str


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    request,
    "index.html",
    {}
)


# Gemini function
def ask_gemini(prompt: str):
    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    return response.output_text


# Ask question
@app.post("/ask")
async def ask_question(data: AIRequest):
    answer = ask_gemini(
        f"Answer this student's question clearly and concisely: {data.prompt}"
    )

    return {
        "success": True,
        "answer": answer
    }