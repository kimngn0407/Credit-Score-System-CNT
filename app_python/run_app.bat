@echo off
echo Starting AI Model Visualization Dashboard...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run Streamlit app
echo Running Streamlit app on http://localhost:8501
echo.
streamlit run app.py --server.port 8501 --server.address localhost

pause