$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$logPath = Join-Path $root 'report_output\_tools\probe.log'
function Log($m) { $l = (Get-Date -Format 'HH:mm:ss') + '  ' + $m; Add-Content $logPath $l; Write-Output $l }
Set-Content -Path $logPath -Value ''

# build a tiny 3 page docx with python-docx first
Log 'creating tiny docx'
python -c "from docx import Document; d=Document(); [d.add_paragraph('probe page %d'%i) for i in range(1,200)]; d.save('report_output/_tools/probe.docx')"
Log 'tiny docx ready'

$wd = New-Object -ComObject Word.Application
$wd.Visible = $false
$wd.DisplayAlerts = 0
try {
    $doc = $wd.Documents.Open((Join-Path $root 'report_output\_tools\probe.docx'), $false, $true)
    Log ('opened tiny, pages=' + $doc.ComputeStatistics(2))
    $doc.ExportAsFixedFormat((Join-Path $root 'report_output\_tools\probe.pdf'), 17, $false, 0, 0, 1, 1, 0, $true, $true, 0)
    Log 'tiny export done'
    $doc.Close(0)
} catch { Log ('ERR ' + $_.Exception.Message) }
finally { try { $wd.Quit(0) } catch {} }
Log 'end'
