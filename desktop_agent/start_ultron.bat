@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo Ambiente Python nao encontrado.
  echo Execute: py -m venv .venv
  echo Depois: .venv\Scripts\pip install -r requirements.txt
  pause
  exit /b 1
)
call .venv\Scripts\activate.bat
python run.py
