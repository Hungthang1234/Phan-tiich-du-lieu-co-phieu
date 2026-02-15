@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ================================================================================
echo        KHOI DONG CUNG CAP CAN THIET VA CHAY PIPELINE
echo ================================================================================
echo.

cd /d "%~dp0"

echo [1/3] Kiem tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo LBAO: Python khong duoc cai dat!
    echo Tai Python tu https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ^✓ Python da duoc cai dat
echo.

echo [2/3] Cai dat cac goi thu vien...
echo Dang cai dat: pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn, openpyxl, Flask, Flask-CORS
echo (Dieu nay co the mat 3-5 phut, vui long doi...)
echo.
pip install --upgrade pip setuptools wheel
pip install --default-timeout=1000 --only-binary=:all: -r requirements.txt
if errorlevel 1 (
    echo.
    echo LBAO: Co loi khi cai dat packages!
    echo Thử lại bằng tay:
    echo   pip install --default-timeout=1000 pandas numpy scikit-learn xgboost matplotlib seaborn openpyxl
    pause
    exit /b 1
)
echo ^✓ Cac goi thu vien da duoc cai dat thanh cong
echo.

echo [3/3] Chay Pipeline...
echo.
python run_pipeline.py

echo.
echo ================================================================================
echo        HOAN TAT!
echo ================================================================================
pause
