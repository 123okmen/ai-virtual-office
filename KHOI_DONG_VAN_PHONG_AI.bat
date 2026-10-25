@echo off
chcp 65001 >nul
title VAN PHONG AO AI 24/7 - QUAN LY CHUOI QUAN
echo ============================================================================
echo    KHOI DONG HE THONG VAN PHONG AO AI 24/24 (MULTI-AGENT COMMAND CENTER)
echo ============================================================================
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel%==0 (
    echo [OK] Dang khoi chay Server 24/24 va mo giao dien dieu hanh...
    python office_daemon_247.py
) else (
    echo [INFO] Mo truc tiep Giao dien Van Phong Ao AI 24/24 tren trinh duyet...
    start "" "%~dp0index.html"
)
pause
