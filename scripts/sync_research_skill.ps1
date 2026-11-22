[CmdletBinding()]
param(
    [string]$RepositoryRoot = (Join-Path $PSScriptRoot '..'),
    [string]$SkillsRoot = (Join-Path $env:USERPROFILE '.agents\skills')
)

$ErrorActionPreference = 'Stop'
$sourceRepository = 'https://github.com/lm846802297-bit/high-energy-theory-research.git'
$skillName = 'high-energy-theory-research'
$skillPath = "skills/$skillName"
$repository = (Resolve-Path -LiteralPath $RepositoryRoot).Path

function Invoke-Git {
    param([string[]]$GitArguments)
    $output = & git -C $repository @GitArguments
    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed: $($GitArguments[0])"
    }
    $output
}

function Get-Inventory {
    param([string]$Directory)
    $root = [IO.Path]::GetFullPath($Directory).TrimEnd('\', '/')
    Get-ChildItem -LiteralPath $root -Recurse -File -Force |
        Where-Object { $_.FullName -ne (Join-Path $root 'skill-install-manifest.json') } |
        Sort-Object FullName |
        ForEach-Object {
            [ordered]@{
                path = $_.FullName.Substring($root.Length + 1).Replace('\', '/')
                sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            }
        }
}

# Fetch the publication branch directly. Local branches and working-tree files
# are never used as installation inputs.
$publication = Invoke-Git @('ls-remote', '--exit-code', $sourceRepository, 'refs/heads/main')
$commit = ($publication -split '\s+')[0]
if ($commit -cnotmatch '^[0-9a-f]{40}$') {
    throw 'Could not resolve the published main commit.'
}
Invoke-Git @('fetch', '--no-tags', '--no-write-fetch-head', $sourceRepository, $commit) | Out-Null
$required = @(
    'SKILL.md',
    'references/task-router.md',
    'references/evidence-and-claim-gates.md',
    'references/source-and-version-audit.md',
    'references/symbolic-calculation.md',
    'references/numerical-scans-and-uncertainty.md',
    'references/scientific-figure-audit.md',
    'references/paper-reading.md',
    'references/optional-tooling.md',
    'scripts/check_codex_skill_discovery.ps1'
)
$tracked = Invoke-Git @('ls-tree', '-r', '--name-only', $commit, '--', $skillPath)
$missing = @($required | Where-Object { "$skillPath/$_" -cnotin $tracked })
if ($missing.Count -gt 0) {
    throw "Published main at $commit does not contain the complete Skill. Missing: $($missing -join ', ')"
}

$root = [IO.Path]::GetFullPath($SkillsRoot)
[IO.Directory]::CreateDirectory($root) | Out-Null
$destination = Join-Path $root $skillName
$scratch = Join-Path $root ('.install-' + [guid]::NewGuid().ToString('N'))
$backup = Join-Path $scratch 'previous'
$lock = [IO.File]::Open((Join-Path $root ".$skillName.lock"), 'OpenOrCreate', 'ReadWrite', 'None')
try {
    if (Test-Path -LiteralPath $destination) {
        $existing = Get-Item -LiteralPath $destination -Force
        $oldManifest = Join-Path $destination 'skill-install-manifest.json'
        if (-not $existing.PSIsContainer -or ($existing.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
            -not (Test-Path -LiteralPath $oldManifest -PathType Leaf)) {
            throw "Existing Skill is not managed by this installer: $destination"
        }
        $old = Get-Content -LiteralPath $oldManifest -Raw -Encoding UTF8 | ConvertFrom-Json
        $recorded = @($old.files | ForEach-Object { "$($_.path) $($_.sha256)" } | Sort-Object)
        $actual = @(Get-Inventory $destination | ForEach-Object { "$($_.path) $($_.sha256)" } | Sort-Object)
        if ($old.source_repository -cne $sourceRepository -or (($recorded -join "`n") -cne ($actual -join "`n"))) {
            throw "The existing Skill differs from its installation manifest: $destination"
        }
    }

    [IO.Directory]::CreateDirectory($scratch) | Out-Null
    $archive = Join-Path $scratch 'skill.zip'
    $export = Join-Path $scratch 'export'
    Invoke-Git @('archive', '--format=zip', "--output=$archive", $commit, '--', $skillPath) | Out-Null
    Expand-Archive -LiteralPath $archive -DestinationPath $export
    $staged = Join-Path $export $skillPath
    $manifest = [ordered]@{
        source_repository = $sourceRepository
        source_commit = $commit
        installed_at_utc = [DateTime]::UtcNow.ToString('o')
        files = @(Get-Inventory $staged)
    }
    $exported = @($manifest.files | ForEach-Object { "$skillPath/$($_.path)" })
    if (@(Compare-Object -ReferenceObject $tracked -DifferenceObject $exported -CaseSensitive).Count -ne 0) {
        throw 'The exported Skill differs from the published file list.'
    }
    $manifestPath = Join-Path $staged 'skill-install-manifest.json'
    [IO.File]::WriteAllText($manifestPath, ($manifest | ConvertTo-Json -Depth 5))
    if (Test-Path -LiteralPath $destination) {
        [IO.Directory]::Move($destination, $backup)
    }
    try {
        [IO.Directory]::Move($staged, $destination)
    } catch {
        if (Test-Path -LiteralPath $backup) {
            [IO.Directory]::Move($backup, $destination)
        }
        throw
    }
    $manifest | ConvertTo-Json -Depth 5
} finally {
    $lock.Dispose()
    # Retain the backup if restoration failed. Scratch is a direct child created
    # by this invocation and contains only the exported Skill and any backup.
    if ((Test-Path -LiteralPath $scratch) -and
        ((Test-Path -LiteralPath $destination) -or -not (Test-Path -LiteralPath $backup))) {
        $resolvedScratch = (Resolve-Path -LiteralPath $scratch).ProviderPath
        if ([IO.Path]::GetDirectoryName($resolvedScratch) -eq $root.TrimEnd('\', '/')) {
            Remove-Item -LiteralPath $resolvedScratch -Recurse -Force
        }
    }
}
