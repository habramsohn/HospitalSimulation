import os
from dotenv import load_dotenv
from gemini.compile import *
import gemini as g
from gemini import main
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

load_dotenv()
api_key = os.getenv('KEY')

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Landing page 
@app.get("/", response_class=HTMLResponse)
def landing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    agents = g.main.personality_init(personalities, context, api_key)
    #g.main.run(agents)
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    # port = int(os.environ.get("PORT", 10000))
    # uvicorn.run("app:app", host="0.0.0.0", port=port)
