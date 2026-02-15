@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ========================================
echo DASHBOARD - VN30 STOCK ANALYSIS
echo ========================================

REM Kiem tra Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Loi: Python chua duoc cai dat
    pause
    exit /b 1
)

REM Kiem tra Flask va Flask-CORS
python -c "import flask" > nul 2>&1
if %errorlevel% neq 0 (
    echo Dang cai dat Flask va Flask-CORS...
    pip install Flask Flask-CORS --only-binary=:all: --default-timeout=1000
    if %errorlevel% neq 0 (
        echo Loi cai dat Flask
        pause
        exit /b 1
    )
)

REM Kiem tra pandas
python -c "import pandas" > nul 2>&1
if %errorlevel% neq 0 (
    echo Dang cai dat pandas...
    pip install pandas --only-binary=:all: --default-timeout=1000
    if %errorlevel% neq 0 (
        echo Loi cai dat pandas
        pause
        exit /b 1
    )
)

echo.
echo Dang khoi dong dashboard server...
echo Mo trinh duyet tai: http://localhost:5000
echo.
echo Nhan Ctrl+C de dung server
echo.

REM Start server in background and open browser
start python dashboard_server.py
timeout /t 2 /nobreak
start http://localhost:5000

REM Keep window open
echo.
echo Server dang chay...
echo Dong cua so nay de dung server
pause
