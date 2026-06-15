BeforeAll {
    $script:RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
    $script:ModulePath = Join-Path $RepoRoot 'src/SubmitBpaReleaseChange/SubmitBpaReleaseChange.psd1'
    $script:SamplePath = Join-Path $RepoRoot 'samples/valid.json'
    Import-Module $ModulePath -Force

    function Start-LocalMock {
        param([int]$Status = 202)

        $capture = Join-Path $TestDrive "capture-$([guid]::NewGuid().ToString('N')).json"
        $portFile = Join-Path $TestDrive "port-$([guid]::NewGuid().ToString('N')).txt"
        $scriptPath = Join-Path $RepoRoot 'tests/helpers/mock_trigger.py'
        $python = (Get-Command python -ErrorAction Stop).Source
        $startInfo = [Diagnostics.ProcessStartInfo]::new()
        $startInfo.FileName = $python
        $startInfo.UseShellExecute = $false
        $startInfo.CreateNoWindow = $true
        $startInfo.RedirectStandardOutput = $true
        $startInfo.RedirectStandardError = $true
        foreach ($argument in @(
            $scriptPath,
            '--capture', $capture,
            '--port-file', $portFile,
            '--status', "$Status"
        )) {
            $startInfo.ArgumentList.Add($argument)
        }
        $process = [Diagnostics.Process]::Start($startInfo)

        for ($attempt = 0; $attempt -lt 100; $attempt++) {
            if (Test-Path -LiteralPath $portFile) {
                break
            }
            Start-Sleep -Milliseconds 50
        }
        if (-not (Test-Path -LiteralPath $portFile)) {
            $errorText = $process.StandardError.ReadToEnd()
            Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
            throw "Local mock did not start. $errorText"
        }

        [pscustomobject]@{
            Process = $process
            CapturePath = $capture
            Url = "http://127.0.0.1:$((Get-Content -LiteralPath $portFile -Raw).Trim())/release"
        }
    }

    function New-TestPayload {
        param([scriptblock]$Edit)

        $payload = Get-Content -LiteralPath $SamplePath -Raw | ConvertFrom-Json
        & $Edit $payload
        $path = Join-Path $TestDrive "payload-$([guid]::NewGuid().ToString('N')).json"
        $payload | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $path -Encoding utf8
        return $path
    }
}

Describe 'Submit-BpaReleaseChange' {
    It 'posts a valid payload to the loopback mock' {
        $mock = Start-LocalMock
        try {
            $result = Submit-BpaReleaseChange `
                -PayloadPath $SamplePath `
                -TriggerUrl $mock.Url `
                -Headers @{ 'X-Demo-Key' = 'synthetic-value' }

            $result.Accepted | Should -BeTrue
            $result.StatusCode | Should -Be 202
            $mock.Process.WaitForExit(5000) | Should -BeTrue
            $captured = Get-Content -LiteralPath $mock.CapturePath -Raw | ConvertFrom-Json
            $captured.body.releaseId | Should -Be 'RN-SYNTH-0001'
            $captured.demoHeader | Should -Be 'synthetic-value'
        }
        finally {
            Stop-Process -Id $mock.Process.Id -Force -ErrorAction SilentlyContinue
        }
    }

    It 'blocks invalid input before any POST' {
        $path = New-TestPayload { param($payload) $payload.environment = 'invalid' }
        {
            Submit-BpaReleaseChange -PayloadPath $path -TriggerUrl 'http://127.0.0.1:9/release'
        } | Should -Throw '*validation failed*'
    }

    It 'blocks missing evidence before any POST' {
        $path = New-TestPayload {
            param($payload)
            $payload.PSObject.Properties.Remove('afterEvidence')
        }
        {
            Submit-BpaReleaseChange -PayloadPath $path -TriggerUrl 'http://127.0.0.1:9/release'
        } | Should -Throw '*validation failed*'
    }

    It 'rejects non-loopback HTTP endpoints' {
        {
            Submit-BpaReleaseChange -PayloadPath $SamplePath -TriggerUrl 'http://example.invalid/release'
        } | Should -Throw '*must use HTTPS*'
    }

    It 'returns a bounded error for an unsuccessful HTTP response' {
        $mock = Start-LocalMock -Status 500
        try {
            {
                Submit-BpaReleaseChange -PayloadPath $SamplePath -TriggerUrl $mock.Url
            } | Should -Throw '*HTTP status 500*'
        }
        finally {
            Stop-Process -Id $mock.Process.Id -Force -ErrorAction SilentlyContinue
        }
    }

    It 'writes the accepted hash to an optional registry' {
        $mock = Start-LocalMock
        $registry = Join-Path $TestDrive 'registry.json'
        try {
            Submit-BpaReleaseChange `
                -PayloadPath $SamplePath `
                -TriggerUrl $mock.Url `
                -HashRegistryPath $registry | Out-Null
            $hashes = @(Get-Content -LiteralPath $registry -Raw | ConvertFrom-Json)
            $hashes | Should -Contain (
                Get-Content -LiteralPath $SamplePath -Raw | ConvertFrom-Json
            ).changeHash
        }
        finally {
            Stop-Process -Id $mock.Process.Id -Force -ErrorAction SilentlyContinue
        }
    }

    It 'blocks duplicate hashes before any POST when a registry is supplied' {
        $registry = Join-Path $TestDrive 'registry.json'
        $hash = (Get-Content -LiteralPath $SamplePath -Raw | ConvertFrom-Json).changeHash
        @($hash) | ConvertTo-Json | Set-Content -LiteralPath $registry -Encoding utf8
        {
            Submit-BpaReleaseChange `
                -PayloadPath $SamplePath `
                -TriggerUrl 'http://127.0.0.1:9/release' `
                -HashRegistryPath $registry
        } | Should -Throw '*validation failed*'
    }
}
