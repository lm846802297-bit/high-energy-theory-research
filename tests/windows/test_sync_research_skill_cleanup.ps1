[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '..\..\scripts\research-skill-installer.helpers.ps1')

$cases = @(
    @{ Name = 'successful install with destination and previous backup'; InstallSucceeded = $true; DestinationExists = $true; BackupExists = $true; Expected = $true },
    @{ Name = 'successful install but destination disappeared'; InstallSucceeded = $true; DestinationExists = $false; BackupExists = $true; Expected = $false },
    @{ Name = 'failed install and rollback failed with destination absent'; InstallSucceeded = $false; DestinationExists = $false; BackupExists = $true; Expected = $false },
    @{ Name = 'failed install and rollback failed with destination occupied'; InstallSucceeded = $false; DestinationExists = $true; BackupExists = $true; Expected = $false },
    @{ Name = 'failed install before backup was created'; InstallSucceeded = $false; DestinationExists = $false; BackupExists = $false; Expected = $true },
    @{ Name = 'failed install but rollback restored old destination'; InstallSucceeded = $false; DestinationExists = $true; BackupExists = $false; Expected = $true }
)

foreach ($case in $cases) {
    $actual = Test-ResearchSkillScratchCleanupAllowed -InstallSucceeded $case.InstallSucceeded -DestinationExists $case.DestinationExists -BackupExists $case.BackupExists
    if ($actual -ne $case.Expected) {
        throw ("{0}: expected cleanup={1}, actual={2}" -f $case.Name, $case.Expected, $actual)
    }
    Write-Output ("PASS: {0}" -f $case.Name)
}

Write-Output ("PASS: {0} rollback-cleanup cases" -f $cases.Count)
