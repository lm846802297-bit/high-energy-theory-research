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
