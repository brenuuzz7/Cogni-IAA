from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import wikipedia
import sympy
import datetime

# Configurações básicas
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Função para gerar resposta manual quando Wikipedia não encontrar
def gerar_resposta_manual(pergunta):
    pergunta = pergunta.lower()

    if "planetas do sistema solar" in pergunta:
        return "Os planetas do sistema solar são: Mercúrio, Vênus, Terra, Marte, Júpiter, Saturno, Urano e Netuno."

    if "copa do mundo" in pergunta:
        return "A próxima Copa do Mundo será em 2026, sediada pelos Estados Unidos, Canadá e México."

    if "hoje" in pergunta and "data" in pergunta:
        return f"A data de hoje é {datetime.datetime.now().strftime('%d/%m/%Y')}."

    if "que dia é hoje" in pergunta:
        return f"Hoje é {datetime.datetime.now().strftime('%d/%m/%Y')}."

    if "qual é o ano" in pergunta:
        return f"O ano atual é {datetime.datetime.now().year}."

    # Resposta genérica
    return "Desculpe, não encontrei uma resposta precisa, mas estou sempre aprendendo!"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "resposta": None, "historico": [], "tema": "light-mode"})

@app.post("/perguntar", response_class=HTMLResponse)
async def perguntar(request: Request, pergunta: str = Form(...), tema: str = Form('light-mode')):
    pergunta_original = pergunta
    resposta = ""
    historico = []

    # Primeiro tenta resolver como operação matemática
    try:
        resultado = sympy.sympify(pergunta)
        resposta = f"O resultado é: {resultado}"
    except:
        # Se não for conta, tenta Wikipedia
        try:
            wikipedia.set_lang("pt")
            resposta = wikipedia.summary(pergunta, sentences=2)
        except wikipedia.exceptions.DisambiguationError as e:
            try:
                resposta = wikipedia.summary(e.options[0], sentences=2)
            except:
                resposta = gerar_resposta_manual(pergunta)
        except wikipedia.exceptions.PageError:
            resposta = gerar_resposta_manual(pergunta)
        except:
            resposta = gerar_resposta_manual(pergunta)

    historico.append((pergunta_original, resposta))

    return templates.TemplateResponse("index.html", {"request": request, "pergunta": pergunta_original, "resposta": resposta, "historico": historico, "tema": tema})
