from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import openai
import os

app = FastAPI()

# Configurações
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Pastas
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/enviar", response_class=HTMLResponse)
async def enviar(request: Request):
    form = await request.form()
    mensagem = form.get("mensagem")

    resposta = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é a Cogni IA, uma inteligência artificial amigável, humana, capaz de conversar e responder sobre qualquer assunto."},
            {"role": "user", "content": mensagem},
        ]
    )

    resposta_texto = resposta.choices[0].message.content

    return templates.TemplateResponse("index.html", {"request": request, "mensagem_usuario": mensagem, "resposta": resposta_texto})
