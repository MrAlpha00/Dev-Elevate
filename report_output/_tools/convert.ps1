# Convert the report DOCX to PDF and to a genuine Word 97-2003 .doc using Word COM.
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$docPath = Join-Path $root 'report_output\ElevoraAI_Final_Report.docx'
$pdfPath = Join-Path $root 'report_output\ElevoraAI_Final_Report.pdf'
$doc97Path = Join-Path $root 'report_output\ElevoraAI_Final_Report.doc'
$logPath = Join-Path $root 'report_output\_tools\convert.log'

function Log($m) {
    $line = (Get-Date -Format 'HH:mm:ss') + '  ' + $m
    Add-Content -Path $logPath -Value $line
    Write-Output $line
}

Set-Content -Path $logPath -Value ''

Log 'creating Word application'
$wd = New-Object -ComObject Word.Application
$wd.Visible = $false
$wd.DisplayAlerts = 0
$wd.AutomationSecurity = 3
Log 'Word started, version ' + $wd.Version

try {
    Log 'opening document'
    $doc = $wd.Documents.Open($docPath, $false, $false, $false)
    Log ('opened, pages = ' + $doc.ComputeStatistics(2))

    Log 'updating fields'
    $doc.Fields.Update() | Out-Null
    Log 'repaginating'
    $doc.Repaginate()
    Log ('pages after repaginate = ' + $doc.ComputeStatistics(2))

    Log 'exporting PDF'
    $doc.ExportAsFixedFormat($pdfPath, 17, $false, 0, 0, 1, 1, 0, $true, $true, 0)
    Log 'PDF written'

    Log 'saving Word 97-2003 .doc'
    $doc.SaveAs2($doc97Path, 0)
    Log 'doc written'
    $doc.Close(0)
    Log 'closed'
} catch {
    Log ('ERROR: ' + $_.Exception.Message)
} finally {
    try { $wd.Quit(0) } catch {}
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($wd) | Out-Null
    Log 'done'
}
