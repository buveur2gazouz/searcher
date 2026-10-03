@echo off
title Multi Tools BY YS
cd /d "%~dp0"

echo.
echo ==============================
echo       MULTI TOOLS BY YS
echo ==============================
echo.

if not exist "multi_tools.py" (
    echo [!] multi_tools.py introuvable.
    pause
    exit /b 1
)

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [!] Installation des dependances echouee.
    pause
    exit /b 1
)

echo.
echo [+] Lancement...
echo.
python multi_tools.py

echo.
pause
