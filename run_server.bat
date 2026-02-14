@echo off
:: Activate virtual environment and start the API server
cd /d "%~dp0"

if exist .venv (
    call .venv\Scripts\activate.bat
    echo Starting UPI Payment Simulation System...
    echo.
    echo Server running at: http://localhost:8000
    echo API Documentation: http://localhost:8000/docs
    echo.
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
) else (
    echo Virtual environment not found!
    echo Please run: pip install -r requirements.txt
    pause
)
