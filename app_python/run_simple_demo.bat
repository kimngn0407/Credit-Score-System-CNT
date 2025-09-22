@echo off
echo.
echo ===============================================
echo      Demo Du Doan Rui Ro Vay Von
echo ===============================================
echo.
echo Dang khoi dong demo don gian...
echo.

REM Change to app directory
cd /d "e:\HAKATHON\app_python"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run simple demo
echo Demo se mo tai: http://localhost:8502
echo Nhan Ctrl+C de dung server
echo.
.venv\Scripts\streamlit.exe run simple_demo.py --server.port 8502 --server.address localhost

echo.
echo Cam on ban da su dung demo!
pause