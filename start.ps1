param([ValidateRange(1024,65535)][int]$Port = 5000)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
& '.\.venv\Scripts\python.exe' -m flask --app app:create_app run --host 127.0.0.1 --port $Port
