from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import wikipedia
import sympy
import datetime
import re

app = FastAPI()

# Corrigido: considerar que estamos dentro da pasta 'bot'
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="bot/templates")

# Histórico de perguntas
historico = []

# Definir idioma do Wikipedia
wikipedia.set_lang('pt')

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "historico": historico})

@app.post("/perguntar", response_class=HTMLResponse)
async def perguntar(request: Request, pergunta: str = Form(...)):
    resposta = gerar_resposta(pergunta)
    historico.append({"pergunta": pergunta, "resposta": resposta})
    return templates.TemplateResponse("index.html", {"request": request, "resposta": resposta, "historico": historico})

def gerar_resposta(pergunta):
    pergunta_lower = pergunta.lower()

    # Se for uma operação matemática
    if any(op in pergunta_lower for op in ["+", "-", "*", "/", "x", "dividido", "multiplicado", "somado", "subtraído"]):
        try:
            expressao = pergunta_lower
            expressao = expressao.replace('x', '*').replace('dividido por', '/').replace('multiplicado por', '*').replace('mais', '+').replace('menos', '-')
            resultado = sympy.sympify(expressao)
            return f"O resultado é: {resultado}"
        except:
            return "Não consegui entender sua operação matemática."

    # Datas de eventos famosos
    if "copa do mundo" in pergunta_lower:
        return "A próxima Copa do Mundo de Futebol Masculino será em 2026, sediada nos EUA, Canadá e México."
    if "olimpíadas" in pergunta_lower:
        return "As próximas Olimpíadas de Verão serão em Paris, em 2024."

    # Consultar Wikipedia
    try:
        resumo = wikipedia.summary(pergunta, sentences=2)
        return resumo
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Seja mais específico. Você quis dizer: {', '.join(e.options[:5])}?"
    except wikipedia.exceptions.PageError:
        pass

    # Respostas padrões
    return "Desculpe, não encontrei uma resposta precisa para isso."
    # Atualização manual para forçar push

