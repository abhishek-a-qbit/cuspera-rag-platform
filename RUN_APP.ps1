# Quick startup script for Cuspera RAG application

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Cuspera RAG - Application Launcher" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "Please ensure .env has your GOOGLE_API_KEY" -ForegroundColor Yellow
    exit 1
}

# Start the application
Write-Host "🚀 Starting Cuspera RAG Application..." -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

# Change to app directory and run streamlit
cd app
streamlit run streamlit_app.py
