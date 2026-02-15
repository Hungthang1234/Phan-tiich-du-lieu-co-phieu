@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ================================================================================
echo        CAI DAT CAC GOI THU VIEN CAN THIET
echo ================================================================================
echo.

cd /d "%~dp0"

echo Kiem tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo LBAO: Python khong duoc cai dat!
    pause
    exit /b 1
)
echo.

echo Nang cap pip...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Cai dat cac packages (co the mat 3-5 phut)...
echo Dang cai: pandas, numpy, scikit-learn, xgboost, matplotlib, seaborn, openpyxl, Flask, Flask-CORS
echo.

pip install --default-timeout=1000 --only-binary=:all: pandas numpy scikit-learn xgboost matplotlib seaborn openpyxl Flask Flask-CORS

if errorlevel 1 (
    echo.
    echo LBAO: Co loi khi cai dat!
    echo Thử lại bằng lệnh riêng:
    echo   pip install --default-timeout=1000 pandas
    echo   pip install --default-timeout=1000 numpy
    echo   ... v.v
) else (
    echo.
    echo ^✓ THANH CONG! Cac packages da duoc cai dat.
    echo Chay "run.bat" hoac "python run_pipeline.py" de bat dau pipeline
)

pause
