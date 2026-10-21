# Convert the report DOCX to PDF and to a genuine Word 97-2003 .doc using Word COM.
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$docPath = Join-Path $root 'report_output\ElevoraAI_Final_Report.docx'
$pdfPath = Join-Path $root 'report_output\ElevoraAI_Final_Report.pdf'
$doc97Path = Join-Path $root 'report_output\ElevoraAI_Final_Report.doc'

$wd = New-Object -ComObject Word.Application
$wd.Visible = $false
$wd.DisplayAlerts = 0

try {
    $doc = $wd.Documents.Open($docPath, $false, $false)

    # refresh every field (PAGE / STYLEREF) and re-paginate
    $doc.Fields.Update() | Out-Null
    foreach ($sec in $doc.Sections) {
        foreach ($hf in $sec.Headers) { $hf.Range.Fields.Update() | Out-Null }
        foreach ($hf in $sec.Footers) { $hf.Range.Fields.Update() | Out-Null }
    }
    $doc.Repaginate()

    # 17 = wdExportFormatPDF
    $doc.ExportAsFixedFormat($pdfPath, 17, $false, 0, 0, 1, 1, 0, $true, $true, 0)
    Write-Output ("pdf pages: " + $doc.ComputeStatistics(2))

    # 0 = wdFormatDocument (Word 97-2003 binary .doc)
    $doc.SaveAs2($doc97Path, 0)
    $doc.Close($false)
} finally {
    $wd.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($wd) | Out-Null
}
Write-Output 'done'
