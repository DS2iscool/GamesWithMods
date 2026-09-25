@echo off
REM build_exe.bat
REM Builds glitchtext_hell.exe using PyInstaller.
REM Run this ONCE, on Windows, with Python 3 installed.

echo Installing PyInstaller (skips if already installed)...
python -m pip install --upgrade pyinstaller

echo.
echo Building glitchtext_hell.exe ...
python -m PyInstaller --onefile --console --name glitchtext_hell glitchtext_hell.py

echo.
echo Done. Your exe is at: dist\glitchtext_hell.exe
echo You can move/copy that single file anywhere and run it directly
echo -- no Python installation needed on the machine that runs it.
pause
