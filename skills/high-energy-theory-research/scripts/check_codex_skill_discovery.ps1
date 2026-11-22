[CmdletBinding()]
param(
    [string]$ProjectRoot = ""
)

$ErrorActionPreference = "Stop"
$SkillName = "high-energy-theory-research"
$RequiredReferences = @(
    "task-router.md",
    "evidence-and-claim-gates.md",
    "source-and-version-audit.md",
    "symbolic-calculation.md",
    "numerical-scans-and-uncertainty.md",
    "scientific-figure-audit.md",
    "paper-reading.md",
    "optional-tooling.md"
)

if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
    $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
} else {
    $ProjectRoot = (Resolve-Path $ProjectRoot).Path
}

function Get-SkillPathStatus {
    param([string]$Path)

    $manifest = Join-Path $Path "SKILL.md"
    $missing = @()
    foreach ($reference in $RequiredReferences) {
        if (-not (Test-Path -LiteralPath (Join-Path $Path "references\$reference") -PathType Leaf)) {
            $missing += $reference
        }
    }

    [PSCustomObject]@{
        path = $Path
        directory_present = Test-Path -LiteralPath $Path -PathType Container
        manifest_present = Test-Path -LiteralPath $manifest -PathType Leaf
        missing_references = $missing
        structurally_complete = (
            (Test-Path -LiteralPath $manifest -PathType Leaf) -and
            ($missing.Count -eq 0)
        )
    }
}

$sourcePath = Join-Path $ProjectRoot "skills\$SkillName"
$projectPath = Join-Path $ProjectRoot ".agents\skills\$SkillName"
$userPath = Join-Path $HOME ".agents\skills\$SkillName"
$legacyPath = Join-Path $HOME ".codex\skills\$SkillName"

$codexCommand = Get-Command codex -ErrorAction SilentlyContinue
$codexVersion = $null
if ($null -ne $codexCommand) {
    try {
        $codexVersion = (& $codexCommand.Source --version 2>&1 | Out-String).Trim()
    } catch {
        $codexVersion = "version query failed: $($_.Exception.Message)"
    }
}

$report = [PSCustomObject]@{
    skill_name = $SkillName
    project_root = $ProjectRoot
    source = Get-SkillPathStatus -Path $sourcePath
    codex_project_scope = Get-SkillPathStatus -Path $projectPath
    codex_user_scope = Get-SkillPathStatus -Path $userPath
    legacy_codex_user_path = Get-SkillPathStatus -Path $legacyPath
    codex_cli_available = ($null -ne $codexCommand)
    codex_cli_path = if ($null -ne $codexCommand) { $codexCommand.Source } else { $null }
    codex_cli_version = $codexVersion
    current_documented_project_scope = ".agents/skills/$SkillName"
    current_documented_user_scope = "~/.agents/skills/$SkillName"
    runtime_discovery_confirmed = $false
    known_windows_desktop_issue = "https://github.com/openai/codex/issues/40458 (open as of 2026-11-22; repository-local discovery may be missing in Windows Desktop)"
    manual_runtime_check = "Test the exact host in a fresh session. In Codex CLI inspect /skills; in Windows Codex Desktop inspect the native Available skills list. Then explicitly invoke the Skill by name and confirm its task-specific references can be read."
    note = "This script is read-only. It checks files on disk; it cannot prove runtime discovery. A user-scope copy is global across projects and is diagnostic only, not a project-isolated fix."
}

$report | ConvertTo-Json -Depth 6

if (-not $report.source.manifest_present) {
    exit 2
}
if (-not $report.codex_project_scope.structurally_complete -and
    -not $report.codex_user_scope.structurally_complete) {
    exit 1
}
exit 0
