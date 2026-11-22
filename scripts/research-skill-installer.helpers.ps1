function Test-ResearchSkillScratchCleanupAllowed {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][bool]$InstallSucceeded,
        [Parameter(Mandatory = $true)][bool]$DestinationExists,
        [Parameter(Mandatory = $true)][bool]$BackupExists
    )

    # A backup may be discarded only after a successful install is present,
    # or when no previous installation remains to recover.
    return (($InstallSucceeded -and $DestinationExists) -or -not $BackupExists)
}

function Test-ResearchSkillManifestIntegrity {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)][AllowNull()][object]$Manifest,
        [Parameter(Mandatory = $true)][string]$SourceRepository,
        [Parameter(Mandatory = $true)][object[]]$ActualFiles,
        [Parameter(Mandatory = $true)][string[]]$RequiredFiles
    )

    if ($null -eq $Manifest -or $Manifest.source_repository -cne $SourceRepository) {
        return $false
    }
    if ([string]$Manifest.source_commit -cnotmatch '^[0-9a-f]{40}$' -or $null -eq $Manifest.files) {
        return $false
    }

    $recordedFiles = @($Manifest.files)
    if ($recordedFiles.Count -eq 0) {
        return $false
    }
    $recordedPaths = @($recordedFiles | ForEach-Object { [string]$_.path })
    if (@($RequiredFiles | Where-Object { $_ -cnotin $recordedPaths }).Count -gt 0) {
        return $false
    }
    if (@($recordedFiles | Where-Object {
        [string]::IsNullOrWhiteSpace([string]$_.path) -or
        [string]$_.sha256 -cnotmatch '^[0-9a-f]{64}$'
    }).Count -gt 0) {
        return $false
    }

    $recorded = @($recordedFiles | ForEach-Object { "$($_.path) $($_.sha256)" } | Sort-Object)
    $actual = @($ActualFiles | ForEach-Object { "$($_.path) $($_.sha256)" } | Sort-Object)
    return (@(Compare-Object -ReferenceObject $recorded -DifferenceObject $actual -CaseSensitive).Count -eq 0)
}
