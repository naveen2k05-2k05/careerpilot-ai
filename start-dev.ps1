# CareerPilot AI - Development Server Launcher
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CareerPilot AI - Starting Servers" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start Backend Server
Write-Host "[1/2] Starting Backend Server..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\Asus\OneDrive\Desktop\careerpilot-ai\backend"
    & .\venv\Scripts\Activate.ps1
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
}

Start-Sleep -Seconds 3

# Start Frontend Server
Write-Host "[2/2] Starting Frontend Server..." -ForegroundColor Yellow
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\Asus\OneDrive\Desktop\careerpilot-ai\frontend"
    npm run dev
}

Start-Sleep -Seconds 5

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Servers Started Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Frontend:  http://127.0.0.1:5173" -ForegroundColor Cyan
Write-Host "  Backend:   http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "  API Docs:  http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Demo Mode: Click 'Continue as Demo User'" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop all servers" -ForegroundColor Gray
Write-Host ""

# Monitor jobs
try {
    while ($true) {
        Start-Sleep -Seconds 2
        
        # Check if jobs are still running
        if ($backendJob.State -ne 'Running') {
            Write-Host "Backend server stopped!" -ForegroundColor Red
            break
        }
        if ($frontendJob.State -ne 'Running') {
            Write-Host "Frontend server stopped!" -ForegroundColor Red
            break
        }
    }
}
finally {
    Write-Host "Stopping servers..." -ForegroundColor Yellow
    Stop-Job -Job $backendJob, $frontendJob
    Remove-Job -Job $backendJob, $frontendJob
    Write-Host "Servers stopped." -ForegroundColor Green
}
