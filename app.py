from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

historico = [
    {"role": "system", "content": "Você é a Cogni IA, uma inteligência artificial moderna e amigável. Você responde qualquer tipo de pergunta (acadêmica, emocional, informativa, tecnológica, etc.) de forma humana, educada e clara."}
]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "historico": historico[1:]})

@app.post("/enviar", response_class=HTMLResponse)
async def enviar(request: Request, pergunta: str = Form(...)):
    historico.append({"role": "user", "content": pergunta})

    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=historico,
        temperature=0.7,
        max_tokens=500,
    )

    mensagem = resposta.choices[0].message.content
    historico.append({"role": "assistant", "content": mensagem})

    return templates.TemplateResponse("index.html", {"request": request, "historico": historico[1:]})
