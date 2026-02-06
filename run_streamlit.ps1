# Recipe Intelligence Chatbot - Start Streamlit
# Start the API first (run_api.ps1) in another terminal.

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Using Python: $(Get-Command python | Select-Object -ExpandProperty Source)"
Write-Host "Starting Streamlit. Open the URL shown (e.g. http://localhost:8501)"
Write-Host ""

python -m streamlit run src/bot.py
