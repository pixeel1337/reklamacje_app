@echo off
title Rejestr Reklamacji - Uruchamianie
echo ===================================================
echo   Przygotowywanie srodowiska dla aplikacji...
echo ===================================================

:: 1. Sprawdzanie czy istnieje wirtualne srodowisko venv
if not exist "venv" (
    echo [INFO] Tworzenie wirtualnego srodowiska venv...
    python -m venv venv
)

:: 2. Aktywacja srodowiska
call venv\Scripts\activate

:: 3. Instalacja/Aktualizacja paczek z requirements.txt
echo [INFO] Sprawdzanie i instalacja wymaganych bibliotek...
pip install -r requirements.txt --quiet

:: 4. Uruchomienie programu
echo [INFO] Uruchamianie aplikacji Rejestr Reklamacji...
python main.py

pause