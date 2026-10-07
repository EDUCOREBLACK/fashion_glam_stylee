@echo off
title Fashion Glam Stylee - Servidor
echo ==========================================
echo    Iniciando Fashion Glam Stylee...
echo ==========================================

cd /d C:\Users\ReneVillegasCarreño\Proyectos\fashion_glam_stylee

:: Esperar 3 segundos e iniciar el navegador de forma asincrona
start "" cmd /c "timeout /t 3 /nobreak >nul & start http://127.0.0.1:8000"

:: Activar entorno virtual e iniciar Django
echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Levantando servidor local...
python manage.py runserver

pause
