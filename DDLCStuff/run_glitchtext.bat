@echo off
REM Double-click this file to run glitchtext_hell.py without opening a
REM terminal yourself. Requires Python 3 to be installed and on PATH.
python "%~dp0glitchtext_hell.py"
if errorlevel 1 (
    echo.
    echo Something went wrong. Is Python 3 installed and on your PATH?
    pause
)
