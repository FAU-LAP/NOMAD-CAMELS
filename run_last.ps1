# run_last.ps1
if (Test-Path .last) {
    python (Get-Content .last)
} else {
    Write-Output "No last file to run"
}