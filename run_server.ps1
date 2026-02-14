# PowerShell script to start the UPI Payment Simulation System

Write-Host "Starting UPI Payment Simulation System..." -ForegroundColor Green
Write-Host ""

$venvPath = ".\.venv\Scripts\Activate.ps1"

if (Test-Path $venvPath) {
    # Activate virtual environment
    & $venvPath
    
    Write-Host "Server running at: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host ""
    
    # Start the server
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
} else {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: pip install -r requirements.txt" -ForegroundColor Yellow
}
