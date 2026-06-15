$ErrorActionPreference = "Continue"

function Wait-ForNext {
    Write-Host "`nPress Enter to continue to the next synthetic test..." -ForegroundColor Yellow
    $null = Read-Host
    Clear-Host
}

Clear-Host
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host " Synthetics Test Demo (Reliability Montage)        " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Wait-ForNext

Write-Host "1. Valid Evidence" -ForegroundColor Green
Write-Host "> grc-validate samples/valid.json" -ForegroundColor DarkGray
Write-Host "---------------------------------------------------"
grc-validate samples/valid.json
Wait-ForNext

Write-Host "2. Missing Evidence" -ForegroundColor Yellow
Write-Host "> grc-validate samples/missing-fields.json" -ForegroundColor DarkGray
Write-Host "---------------------------------------------------"
grc-validate samples/missing-fields.json
Wait-ForNext

Write-Host "3. Invalid/Failed Evidence" -ForegroundColor Red
Write-Host "> grc-validate samples/rejected.json" -ForegroundColor DarkGray
Write-Host "---------------------------------------------------"
grc-validate samples/rejected.json
Wait-ForNext

Write-Host "4. Duplicate Evidence" -ForegroundColor Magenta
Write-Host "> grc-validate --registry accepted-hashes.json samples/duplicate.json" -ForegroundColor DarkGray
Write-Host "---------------------------------------------------"
grc-validate --registry accepted-hashes.json samples/duplicate.json
Write-Host "`n===================================================" -ForegroundColor Cyan
Write-Host " End of Synthetics Test Demo                       " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
