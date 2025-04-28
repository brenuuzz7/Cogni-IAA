@echo off
cd /d %~dp0

:: Ativar o ambiente virtual
call venv\Scripts\activate.bat

:: Rodar o servidor FastAPI
uvicorn app:app --reload

pause
