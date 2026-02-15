@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo.
echo ================================================================================
echo                    THONG BAO QUAN TRONG - VUI LONG DOC
echo ================================================================================
echo.

echo 1. LAN DAU TIEN CHAY DU AN?
echo    - Vui long chay "setup_and_run.bat" hoac "install_packages.bat" TRUOC
echo    - Cac file nay se cai dat cac thu vien can thiet
echo    - Chi can chay 1 lan, lan sau khong can chay lai
echo.

echo 2. MO HINH NAY CO HAN CHE GI?
echo    - Mo hinh du bao XU HUONG (tang/giam), KHONG phai du bao GIA chinh xac
echo    - Do chinh xac: ~39%% - tuc la co the sai 61%% trong so tro
echo    - Chi dung cho muc dich HOC TAP va NGHIEN CUU
echo    - KHONG nen dung cho giao dich that
echo.

echo 3. KET QUA BACKTEST
echo    - Chi tien trong qua khu, khong dam bao tuong lai
echo    - Chien luoc nay KHONG luon thang hon "mua ^& nam giu"
echo    - Co the mat tien, khong co duoc bao hanh trom
echo.

echo 4. CAC FILE DE CHAY
echo    - project\setup_and_run.bat: Cai packages + chay pipeline (LAN DAU)
echo    - project\install_packages.bat: Chi cai packages (neu muon tach)
echo    - project\run.bat: Chay pipeline (sau khi packages da cai)
echo    - python project\run_pipeline.py: Chay truc tiep bang Python
echo.

echo 5. CAN GI THEM TRO GIUP?
echo    - Xem file project\README.md de biet chi tiet
echo    - Hay xem cac file log trong thu muc "project\logs"
echo.

echo ================================================================================
echo                        FIRST TIME SETUP REQUIRED!
echo ================================================================================
echo.

echo Please run one of these files FIRST:
echo   * project\setup_and_run.bat (recommended - installs packages + runs pipeline)
echo   * project\install_packages.bat (install packages only)
echo.

echo After that, you can use project\run.bat or python project\run_pipeline.py for next runs.
echo.

echo ================================================================================
echo.

pause
