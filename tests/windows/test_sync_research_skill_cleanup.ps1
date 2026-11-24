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


$source = 'https://github.com/lm846802297-bit/high-energy-theory-research.git'
$commit = 'a' * 40
$hashA = 'b' * 64
$hashB = 'c' * 64
$requiredFiles = @('SKILL.md', 'references/task-router.md')
$validFiles = @(
    [PSCustomObject]@{ path = 'SKILL.md'; sha256 = $hashA },
    [PSCustomObject]@{ path = 'references/task-router.md'; sha256 = $hashB }
)
$actualFiles = @($validFiles)
$validManifest = [PSCustomObject]@{ source_repository = $source; source_commit = $commit; files = $validFiles }
$extraFiles = @($validFiles)
$extraFiles += [PSCustomObject]@{ path = 'extra.txt'; sha256 = $hashA }
$manifestCases = @(
    @{ Name = 'valid manifest and exact file inventory'; Manifest = $validManifest; Actual = $actualFiles; Required = $requiredFiles; Expected = $true },
    @{ Name = 'wrong source repository'; Manifest = [PSCustomObject]@{ source_repository = 'https://example.invalid/repo.git'; source_commit = $commit; files = $validFiles }; Actual = $actualFiles; Required = $requiredFiles; Expected = $false },
    @{ Name = 'malformed source commit'; Manifest = [PSCustomObject]@{ source_repository = $source; source_commit = 'not-a-commit'; files = $validFiles }; Actual = $actualFiles; Required = $requiredFiles; Expected = $false },
    @{ Name = 'missing required Skill file'; Manifest = [PSCustomObject]@{ source_repository = $source; source_commit = $commit; files = @($validFiles[0]) }; Actual = @($validFiles[0]); Required = $requiredFiles; Expected = $false },
    @{ Name = 'modified installed file hash'; Manifest = $validManifest; Actual = @([PSCustomObject]@{ path = 'SKILL.md'; sha256 = $hashB }, $validFiles[1]); Required = $requiredFiles; Expected = $false },
    @{ Name = 'empty manifest file list'; Manifest = [PSCustomObject]@{ source_repository = $source; source_commit = $commit; files = @() }; Actual = @(); Required = $requiredFiles; Expected = $false },
    @{ Name = 'unrecorded extra installed file'; Manifest = $validManifest; Actual = $extraFiles; Required = $requiredFiles; Expected = $false }
)

foreach ($case in $manifestCases) {
    $actual = Test-ResearchSkillManifestIntegrity -Manifest $case.Manifest -SourceRepository $source -ActualFiles $case.Actual -RequiredFiles $case.Required
    if ($actual -ne $case.Expected) {
        throw ("{0}: expected integrity={1}, actual={2}" -f $case.Name, $case.Expected, $actual)
    }
    Write-Output ("PASS: {0}" -f $case.Name)
}

Write-Output ("PASS: {0} rollback-cleanup and {1} manifest-integrity cases" -f $cases.Count, $manifestCases.Count)
