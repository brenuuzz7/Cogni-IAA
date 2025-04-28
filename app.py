from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import random

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Histórico das mensagens
historico = []

# Função para gerar respostas emocionais
def gerar_resposta(pergunta):
    respostas_positivas = [
        "Entendo como você se sente. 💬",
        "Estou aqui para te ouvir, conte comigo! 🤗",
        "Pode falar, estou te acompanhando. ✨",
        "Se precisar desabafar, estou aqui. 💖",
        "Você é mais forte do que imagina. 🌟"
    ]
    respostas_gerais = [
        "Que interessante! Me fale mais sobre isso. 😊",
        "E como isso faz você se sentir?",
        "Estou curioso para saber mais.",
        "Isso parece importante para você."
    ]
    respostas = respostas_positivas + respostas_gerais
    return random.choice(respostas)

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "historico": historico})

@app.post("/send")
async def send_message(request: Request, pergunta: str = Form(...)):
    pergunta = pergunta.strip()
    if pergunta:
        historico.append({"texto": pergunta, "tipo": "usuario"})
        resposta = gerar_resposta(pergunta)
        historico.append({"texto": resposta, "tipo": "bot"})
    return RedirectResponse("/", status_code=303)
