<#
.SYNOPSIS
  Enable BrowserOS Remote Hermes by setting AGENT_RUNNER_JWT_SECRET,
  flipping allow_remote_in_mcp to true, and restarting BrowserOS.
.DESCRIPTION
  This script is reversible. It saves the original state, applies changes,
  verifies them, and can roll back if needed.
.NOTES
  Run in an elevated PowerShell if you need to restart the BrowserOS service/process.
#>

param(
    [switch]$Rollback,
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"

# Paths
$ConfigPath = "C:\Users\asus\AppData\Local\BrowserOS\User Data\.browseros\config.json"
$BackupPath = "$ConfigPath.bak"
$ProcessName = "browseros-claw-server"
$ExecutablePath = "C:\Users\asus\AppData\Local\BrowserClaw\User Data\.browseros\BrowserClawServer\versions\0.0.44\resources\bin\browseros-claw-server.exe"
$EnvVarName = "AGENT_RUNNER_JWT_SECRET"

# Helper: log
function Write-Log {
    param([string]$Message)
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] $Message"
}

# Helper: generate strong random base64 secret (32 bytes = 256 bits)
function New-StrongJwtSecret {
    $bytes = New-Object byte[] 32
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    return [Convert]::ToBase64String($bytes)
}

# Helper: verify JSON is valid
function Test-JsonFile {
    param([string]$Path)
    try {
        $null = Get-Content -Path $Path -Raw | ConvertFrom-Json
        return $true
    } catch {
        return $false
    }
}

# Rollback logic
if ($Rollback) {
    Write-Log "=== ROLLBACK MODE ==="

    if (-not (Test-Path $BackupPath)) {
        Write-Log "ERROR: Backup file not found at $BackupPath. Cannot rollback."
        exit 1
    }

    # Restore config
    Write-Log "Restoring config from backup..."
    Copy-Item -Path $BackupPath -Destination $ConfigPath -Force
    Write-Log "Config restored."

    # Remove env var
    Write-Log "Removing user environment variable $EnvVarName..."
    [System.Environment]::SetEnvironmentVariable($EnvVarName, $null, "User")
    Write-Log "Environment variable removed."

    # Restart BrowserOS
    Write-Log "Restarting BrowserOS..."
    if (Get-Process -Name $ProcessName -ErrorAction SilentlyContinue) {
        Stop-Process -Name $ProcessName -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 3
    }
    if (Test-Path $ExecutablePath) {
        Start-Process -FilePath $ExecutablePath -WindowStyle Hidden
        Write-Log "BrowserOS started."
    } else {
        Write-Log "WARNING: Executable not found at $ExecutablePath. Please start BrowserOS manually."
    }

    Write-Log "=== ROLLBACK COMPLETE ==="
    exit 0
}

# MAIN ENABLE LOGIC

# Step 0: Pre-flight checks
Write-Log "=== PRE-FLIGHT CHECKS ==="

if (-not (Test-Path $ConfigPath)) {
    Write-Log "ERROR: Config file not found at $ConfigPath"
    exit 1
}

if (-not (Test-JsonFile -Path $ConfigPath)) {
    Write-Log "ERROR: Config file is not valid JSON."
    exit 1
}

if (-not (Test-Path $ExecutablePath)) {
    Write-Log "WARNING: BrowserOS executable not found at $ExecutablePath."
    Write-Log "The script will attempt to restart the process if it is already running, but cannot start it if stopped."
}

# Step 1: Backup current state
Write-Log "Backing up current config to $BackupPath ..."
Copy-Item -Path $ConfigPath -Destination $BackupPath -Force
Write-Log "Backup complete."

# Step 2: Generate and set JWT secret
Write-Log "Generating strong JWT secret..."
$newSecret = New-StrongJwtSecret
Write-Log "Setting user environment variable $EnvVarName ..."
[System.Environment]::SetEnvironmentVariable($EnvVarName, $newSecret, "User")
Write-Log "Environment variable set."

# Step 3: Flip allow_remote_in_mcp to true
Write-Log "Updating config: allow_remote_in_mcp -> true ..."
$config = Get-Content -Path $ConfigPath -Raw | ConvertFrom-Json
$config.flags.allow_remote_in_mcp = $true
$config | ConvertTo-Json -Depth 10 | Set-Content -Path $ConfigPath -Encoding UTF8
Write-Log "Config updated."

# Step 4: Restart BrowserOS
Write-Log "Restarting BrowserOS..."
$proc = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue
if ($proc) {
    Write-Log "Stopping existing $ProcessName process(es)..."
    Stop-Process -Name $ProcessName -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 3
} else {
    Write-Log "No running $ProcessName process found."
}

if (Test-Path $ExecutablePath) {
    Write-Log "Starting BrowserOS..."
    Start-Process -FilePath $ExecutablePath -WindowStyle Hidden
    Start-Sleep -Seconds 5
    Write-Log "BrowserOS started."
} else {
    Write-Log "WARNING: Executable not found at $ExecutablePath. Please start BrowserOS manually."
}

# Step 5: Verification
Write-Log "=== VERIFICATION ==="

# Verify env var
$verifyEnv = [System.Environment]::GetEnvironmentVariable($EnvVarName, "User")
if ($verifyEnv -eq $newSecret) {
    Write-Log "PASS: $EnvVarName is set in user environment."
} else {
    Write-Log "FAIL: $EnvVarName verification failed."
}

# Verify config
if (Test-JsonFile -Path $ConfigPath) {
    $verifyConfig = Get-Content -Path $ConfigPath -Raw | ConvertFrom-Json
    if ($verifyConfig.flags.allow_remote_in_mcp -eq $true) {
        Write-Log "PASS: allow_remote_in_mcp is true in config."
    } else {
        Write-Log "FAIL: allow_remote_in_mcp is not true."
    }
} else {
    Write-Log "FAIL: Config file is not valid JSON after update."
}

# Verify process running
$verifyProc = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue
if ($verifyProc) {
    Write-Log "PASS: $ProcessName is running (PID $($verifyProc.Id))."
} else {
    Write-Log "WARNING: $ProcessName is not running. BrowserOS may need to be started manually."
}

Write-Log "=== ENABLE COMPLETE ==="
Write-Log "To rollback, run this script with -Rollback:"
Write-Log "  powershell -ExecutionPolicy Bypass -File `"$PSCommandPath`" -Rollback"
