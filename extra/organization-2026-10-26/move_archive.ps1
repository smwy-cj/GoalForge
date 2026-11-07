$ErrorActionPreference = 'Stop'
$taskRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
$taskPrefix = $taskRoot.TrimEnd('\') + '\'
$taskPlan = Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'move-plan.json') | ConvertFrom-Json
if ($taskPlan.root -ne $taskRoot) { throw 'Workspace root mismatch' }
$taskActions = foreach ($taskEntry in $taskPlan.actions) {
    $taskSource = [IO.Path]::GetFullPath((Join-Path $taskRoot $taskEntry.source))
    $taskDestination = [IO.Path]::GetFullPath((Join-Path $taskRoot $taskEntry.destination))
    if (-not $taskSource.StartsWith($taskPrefix, [StringComparison]::OrdinalIgnoreCase) -or
        -not $taskDestination.StartsWith($taskPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Move target escapes workspace'
    }
    if (-not (Test-Path -LiteralPath $taskSource) -or (Test-Path -LiteralPath $taskDestination)) {
        throw ('Missing source or occupied destination: ' + $taskEntry.source)
    }
    [PSCustomObject]@{ Source = $taskSource; Destination = $taskDestination }
}
foreach ($taskAction in $taskActions) {
    $taskParent = Split-Path -Parent $taskAction.Destination
    New-Item -ItemType Directory -Path $taskParent -Force | Out-Null
    Move-Item -LiteralPath $taskAction.Source -Destination $taskAction.Destination
}
Write-Output ('Moved ' + $taskActions.Count + ' checked paths; no files deleted.')
