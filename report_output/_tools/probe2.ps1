$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$logPath = Join-Path $root 'report_output\_tools\probe.log'
function Log($m) { $l = (Get-Date -Format 'HH:mm:ss') + '  ' + $m; Add-Content $logPath $l; Write-Output $l }
Set-Content -Path $logPath -Value ''

$wd = New-Object -ComObject Word.Application
$wd.Visible = $false
$wd.DisplayAlerts = 0
try {
    $doc = $wd.Documents.Open((Join-Path $root 'report_output\_tools\probe.docx'), $false, $false)
    Log 'opened tiny'
    Log 'SaveAs2 pdf'
    $doc.SaveAs2((Join-Path $root 'report_output\_tools\probe2.pdf'), 17)
    Log 'SaveAs2 pdf done'
    $doc.Close(0)
} catch { Log ('ERR ' + $_.Exception.Message) }
finally { try { $wd.Quit(0) } catch {} }
Log 'end'
