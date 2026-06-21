@echo off
REM ==========================================================================
REM  Cria um novo projeto a partir do template (Windows).
REM  Precisa apenas de Python 3.11+ instalado. Nao usa uv.
REM
REM  Uso:
REM    novo-projeto.cmd                 -> abre o assistente interativo
REM    novo-projeto.cmd --list          -> lista os profiles
REM    novo-projeto.cmd --profile ...   -> repassa argumentos ao script
REM ==========================================================================
setlocal

REM Prefere o Python Launcher (py), que escolhe a versao mais nova instalada.
where py >nul 2>nul
if %errorlevel%==0 (
    set "PYBIN=py -3"
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set "PYBIN=python"
    ) else (
        echo.
        echo Python nao encontrado. Instale o Python 3.11 ou superior:
        echo    https://www.python.org/downloads/
        echo Na instalacao, marque "Add Python to PATH".
        echo.
        exit /b 1
    )
)

%PYBIN% "%~dp0scripts\new_project.py" %*
exit /b %errorlevel%
