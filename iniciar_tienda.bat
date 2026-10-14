@echo off
setlocal
title Fashion Glam Stylee - Servidor
echo ==========================================
echo    Iniciando Fashion Glam Stylee...
echo ==========================================

cd /d "%~dp0"
if not exist "manage.py" (
    echo No se encontro manage.py. Este archivo debe estar en la carpeta del proyecto.
    pause
    exit /b 1
)

if not exist "venv\Scripts\python.exe" (
    echo Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 goto error
)

set "PYTHON=venv\Scripts\python.exe"
echo Instalando dependencias...
"%PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 goto error

echo Preparando base de datos...
"%PYTHON%" manage.py migrate
if errorlevel 1 goto error

echo Cargando productos de muestra...
"%PYTHON%" populate_db.py
if errorlevel 1 goto error

start "" cmd /c "timeout /t 3 /nobreak >nul & start http://127.0.0.1:8000"
echo Servidor disponible en http://127.0.0.1:8000
"%PYTHON%" manage.py runserver
pause
exit /b 0

:error
echo Ocurrio un error al preparar o iniciar la tienda.
pause
exit /b 1
