@echo off
cd /d "%~dp0"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller
pyinstaller --clean ULTRON.spec
echo Build concluido. Arquivo: dist\ULTRON.exe
pause
