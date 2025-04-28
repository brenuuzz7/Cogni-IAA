from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import wikipedia
import sympy
import datetime
import re

app = FastAPI()

# Montar pastas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Histórico de pesquisa
history = []

# Função de consulta inteligente
def obter_resposta(pergunta):
    pergunta = pergunta.lower()

    # Resolver expressões matemáticas
    expressao = re.findall(r"[-+*/().\d\s]+", pergunta)
    if expressao:
        try:
            resultado = sympy.sympify("".join(expressao)).evalf()
            return f"O resultado é: {resultado}"
        except:
            pass

    # Verificar datas importantes
    eventos = {
        "copa do mundo": "A próxima Copa do Mundo será em 2026.",
        "olimpíadas": "As próximas Olimpíadas serão em Paris em 2024.",
        "natal": "O Natal é comemorado no dia 25 de dezembro."
    }
    for evento, resposta in eventos.items():
        if evento in pergunta:
            return resposta

    # Consulta no Wikipedia
    try:
        wikipedia.set_lang("pt")
        resultado = wikipedia.summary(pergunta, sentences=2)
        return resultado
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Seja mais específico: {e.options}"
    except wikipedia.exceptions.PageError:
        return "Desculpe, não encontrei uma resposta específica. Mas estou aprendendo!"

# 🛠️ Aqui corrigimos: Criar a rota principal (/) para o site carregar!
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "history": history})

@app.post("/perguntar", response_class=HTMLResponse)
async def perguntar(request: Request, pergunta: str = Form(...)):
    resposta = obter_resposta(pergunta)
    history.append({"pergunta": pergunta, "resposta": resposta})
    return templates.TemplateResponse("index.html", {"request": request, "resposta": resposta, "history": history})
