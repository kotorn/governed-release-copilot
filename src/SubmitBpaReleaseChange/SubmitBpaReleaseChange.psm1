Set-StrictMode -Version Latest

function Test-BpaTriggerUri {
    param([Parameter(Mandatory)][uri]$Uri)

    if ($Uri.Scheme -eq 'https') {
        return
    }
    if ($Uri.Scheme -eq 'http' -and $Uri.IsLoopback) {
        return
    }
    throw 'Trigger URL must use HTTPS unless the host is loopback.'
}

function Get-GrcRepositoryRoot {
    return (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
}

function Invoke-GrcPayloadValidation {
    param(
        [Parameter(Mandatory)][string]$PayloadPath,
        [string]$HashRegistryPath
    )

    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        throw 'Python is required to validate ReleaseChangeV1 payloads.'
    }

    $repoRoot = Get-GrcRepositoryRoot
    $schemaPath = Join-Path $repoRoot 'schema/ReleaseChangeV1.schema.json'
    $arguments = @(
        '-m', 'governed_release_copilot',
        '--schema', $schemaPath,
        $PayloadPath
    )
    if ($HashRegistryPath -and (Test-Path -LiteralPath $HashRegistryPath)) {
        $arguments += @('--registry', $HashRegistryPath)
    }

    $previousPythonPath = $env:PYTHONPATH
    try {
        $sourcePath = Join-Path $repoRoot 'src'
        $env:PYTHONPATH = if ($previousPythonPath) {
            "$sourcePath$([IO.Path]::PathSeparator)$previousPythonPath"
        } else {
            $sourcePath
        }
        & $python.Source @arguments 2>&1 | Out-Null
        $exitCode = $LASTEXITCODE
    }
    finally {
        $env:PYTHONPATH = $previousPythonPath
    }

    if ($exitCode -ne 0) {
        throw "Payload validation failed with exit code $exitCode."
    }
}

function Add-BpaHashToRegistry {
    param(
        [Parameter(Mandatory)][string]$HashRegistryPath,
        [Parameter(Mandatory)][string]$ChangeHash
    )

    $registry = @()
    if (Test-Path -LiteralPath $HashRegistryPath) {
        $parsed = Get-Content -LiteralPath $HashRegistryPath -Raw | ConvertFrom-Json
        $registry = @($parsed)
    }
    if ($registry -notcontains $ChangeHash) {
        $registry += $ChangeHash
        $registry | ConvertTo-Json | Set-Content -LiteralPath $HashRegistryPath -Encoding utf8
    }
}

function Submit-BpaReleaseChange {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$PayloadPath,
        [Parameter(Mandatory)][uri]$TriggerUrl,
        [hashtable]$Headers = @{},
        [string]$HashRegistryPath,
        [ValidateRange(1, 300)][int]$TimeoutSec = 30
    )

    $resolvedPayload = (Resolve-Path -LiteralPath $PayloadPath -ErrorAction Stop).Path
    Test-BpaTriggerUri -Uri $TriggerUrl
    Invoke-GrcPayloadValidation -PayloadPath $resolvedPayload -HashRegistryPath $HashRegistryPath

    $body = Get-Content -LiteralPath $resolvedPayload -Raw
    try {
        $response = Invoke-WebRequest `
            -Uri $TriggerUrl `
            -Method Post `
            -Headers $Headers `
            -ContentType 'application/json' `
            -Body $body `
            -TimeoutSec $TimeoutSec `
            -SkipHttpErrorCheck
    }
    catch {
        throw 'Release change submission failed before an HTTP response was received.'
    }

    if ($response.StatusCode -lt 200 -or $response.StatusCode -ge 300) {
        throw "Release change submission failed with HTTP status $($response.StatusCode)."
    }

    $payload = $body | ConvertFrom-Json
    if ($HashRegistryPath) {
        Add-BpaHashToRegistry -HashRegistryPath $HashRegistryPath -ChangeHash $payload.changeHash
    }

    [pscustomobject]@{
        Accepted = $true
        StatusCode = [int]$response.StatusCode
        ReleaseId = [string]$payload.releaseId
        ChangeHash = [string]$payload.changeHash
    }
}

Export-ModuleMember -Function Submit-BpaReleaseChange
