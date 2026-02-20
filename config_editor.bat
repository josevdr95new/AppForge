@echo off
title AppForge - Editor de Configuracion
cd /d "%~dp0"
py config_editor.py
if errorlevel 1 (
    echo.
    echo Error: Python no esta instalado o no esta en el PATH.
    echo Descarga Python desde: https://www.python.org/downloads/
    echo.
    pause
)
