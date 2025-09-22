@echo off
echo.
echo ===============================================
echo    AI Model Visualization Dashboard
echo ===============================================
echo.
echo Dang khoi dong ung dung...
echo.

REM Change to app directory
cd /d "e:\HAKATHON\app_python"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run streamlit app
echo Ung dung se mo tai: http://localhost:8501
echo Nhan Ctrl+C de dung server
echo.
.venv\Scripts\streamlit.exe run app.py --server.port 8501 --server.address localhost

echo.
echo Cam on ban da su dung ung dung!
pause