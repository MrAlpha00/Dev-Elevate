$wd = New-Object -ComObject Word.Application
$wd.Visible = $false
$docPath = Join-Path -Path (Get-Location) -ChildPath 'report_output\ElevoraAI_Final_Report.docx'
$pdfPath = Join-Path -Path (Get-Location) -ChildPath 'report_output\ElevoraAI_Final_Report.pdf'
$docPath2 = Join-Path -Path (Get-Location) -ChildPath 'report_output\ElevoraAI_Final_Report.doc'
$doc = $wd.Documents.Open($docPath)
$doc.SaveAs([ref]$pdfPath, [ref]17)
$doc.SaveAs([ref]$docPath2, [ref]0)
$doc.Close($false)
$wd.Quit()
Write-Output 'done'
