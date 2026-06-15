[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $repoRoot
try {
    $requiredFiles = @(
        'README.md',
        'DECISIONS.md',
        'accepted-hashes.json',
        'docs/architecture.mmd',
        'docs/architecture.png',
        'docs/evidence-matrix.md',
        'docs/submission.md',
        'docs/project-overview.md',
        'docs/FEATURES.md',
        'docs/RELEASECHANGEV1-CONTRACT.md',
        'docs/STATE-MODEL.md',
        'docs/PRIVACY-SCAN-RULES.md',
        'docs/PR-CHECKLIST.md',
        'docs/flow-contract.md',
        'docs/demo-runsheet.md',
        'docs/judging-evidence-matrix.md',
        'docs/microsoft-iq.md',
        'docs/agent-instructions.md',
        'docs/video/README.md',
        'schema/ReleaseChangeV1.schema.json',
        'src/SubmitBpaReleaseChange/SubmitBpaReleaseChange.psd1',
        'src/SubmitBpaReleaseChange/SubmitBpaReleaseChange.psm1',
        'tests/helpers/mock_trigger.py',
        'tests/powershell/SubmitBpaReleaseChange.Tests.ps1'
    )

    foreach ($file in $requiredFiles) {
        if (-not (Test-Path -LiteralPath $file -PathType Leaf)) {
            throw "Required file is missing: $file"
        }
    }

    python scripts/verify.py
    if ($LASTEXITCODE -ne 0) {
        throw 'Python verification gate failed.'
    }

    Write-Host 'PowerShell verification wrapper passed.' -ForegroundColor Green
}
finally {
    Pop-Location
}
