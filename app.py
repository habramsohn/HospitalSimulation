import os
from dotenv import load_dotenv
from gemini.compile import *
import gemini as g
from gemini import main
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

load_dotenv()
api_key = os.getenv('KEY')

agents = g.main.personality_init(personalities, context, api_key)
print(agents)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Landing page 
@app.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/select")
def selection(request: Request, selection: str):
    global active_agent 
    active_agent = agents[selection]
    html = f"<pre> {selection}</pre>"
    return HTMLResponse(html)

@app.post("/send")
async def chat(request: Request, query: str = Form(...)):
    try:
        response = g.main.run(active_agent, query)
        message = "User: " + "".join(list(query)) + "<br> <br>" \
            + f"{active_agent.name}: " + response + "<br> <br>"
    except NameError:  
         message = "Please select a bot. <br>"
    return HTMLResponse(message)

@app.get("/finish")
def close(request: Request):
    global active_agent
    active_agent = agents['Error']
    message = "Session ended."
    return HTMLResponse(message)

if __name__ == "__main__":
    #print(agents)
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    # port = int(os.environ.get("PORT", 10000))
    # uvicorn.run("app:app", host="0.0.0.0", port=port)
