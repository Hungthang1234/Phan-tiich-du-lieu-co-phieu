@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo                        HUONG DAN SU DUNG DU AN
echo ================================================================================
echo.
echo Dự án gồm 3 bước chính:
echo.
echo 1. LAN DAU TIEN / KHONG CON PACKAGE
echo    ========================================
echo    Double-click: setup_and_run.bat
echo    (Tự động cài packages + chạy pipeline + mở dashboard)
echo.
echo 2. CHAY PIPELINE (dữ liệu + mô hình + backtest)
echo    ========================================
echo    Double-click: run.bat
echo    hoặc: python run_pipeline.py
echo    (Mất ~2-5 phút)
echo.
echo 3. XEM KET QUA TREN WEB DASHBOARD
echo    ========================================
echo    Double-click: run_dashboard.bat
echo    hoặc: python dashboard_server.py
echo    Rồi mở trình duyệt vào: http://localhost:5000
echo.
echo TONG QUAT:
echo   run.bat               = Chạy pipeline (8 bước)
echo   run_dashboard.bat     = Chạy web dashboard
echo   setup_and_run.bat     = Cài packages + chạy pipeline
echo   install_packages.bat  = Chỉ cài packages
echo.
echo Xem thêm: README.md
echo.
echo ================================================================================
echo.
pause
