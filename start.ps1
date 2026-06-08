# CareerPilot AI - Start both servers
Write-Host "Starting CareerPilot AI..." -ForegroundColor Cyan

$backend = Start-Process powershell -ArgumentList @(
    "-NoExit", "-Command",
    "cd '$PSScriptRoot\backend'; .\venv\Scripts\activate; python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
) -PassThru

Start-Sleep -Seconds 2

$frontend = Start-Process powershell -ArgumentList @(
    "-NoExit", "-Command",
    "cd '$PSScriptRoot\frontend'; npm run dev"
) -PassThru

Write-Host ""
Write-Host "  Frontend:  http://127.0.0.1:5173" -ForegroundColor Green
Write-Host "  API Docs:  http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "  Demo login: Click 'Continue as Demo User' on login page" -ForegroundColor Yellow
Write-Host ""
