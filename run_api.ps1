# Recipe Intelligence API - Start script
# IMPORTANT: If you already have the API running, stop it first (Ctrl+C) so this loads the latest code.

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Using Python: $(Get-Command python | Select-Object -ExpandProperty Source)"
Write-Host "Starting API at http://127.0.0.1:8001 (avoids port 8000 in use) ..."
Write-Host ""

python -m uvicorn src.api:app --reload --host 127.0.0.1 --port 8001
