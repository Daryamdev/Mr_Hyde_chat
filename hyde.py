import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# initialize the AsyncAnthropic client with the API key from environment variables
client = AsyncAnthropic(api_key=os.getenv("hyde"))

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("user_input", "")
    history = data.get("history", [])

    with open("prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()


    with open("memory.txt", "r", encoding="utf-8") as f:
        memory_data= f.read()

    full=f"{system_prompt}\n\n{memory_data}"

    #messages from the last 15 interactions
    messages = []
    for mes in history[-15:]:
        role = "user" if mes["role"] == "user" else "assistant"
        messages.append({"role": role, "content": mes["content"]})

    
    messages.append({"role": "user", "content": user_input})

    
    response = await client.messages.create(
        model="claude-sonnet-4-6",  #Claude-opus-4-8
        max_tokens=1000,
        temperature=1.0,
        system=full,
        messages=messages
    )

    bot_reply = response.content[0].text

    
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": bot_reply})

    return {"response": bot_reply, "history": history}