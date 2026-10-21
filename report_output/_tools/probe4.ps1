$ErrorActionPreference = 'Continue'
$root = (Get-Location).Path
$logPath = Join-Path $root 'report_output\_tools\probe.log'
function Log($m) { $l = (Get-Date -Format 'HH:mm:ss') + '  ' + $m; Add-Content $logPath $l; Write-Output $l }
Set-Content -Path $logPath -Value ''

$probe = Join-Path $root 'report_output\_tools\probe.docx'

function Try-Export([string]$tag, [scriptblock]$body) {
    $j = Start-Job -ScriptBlock {
        param($tag, $bodyText, $probe)
        $ErrorActionPreference = 'Stop'
        $wd = New-Object -ComObject Word.Application
        $wd.Visible = $false
        $wd.DisplayAlerts = 0
        try {
            $wd.Options.SaveInterval = 0
            $wd.Options.BackgroundSave = $false
            $wd.Options.UpdateLinksAtOpen = $false
            $doc = $wd.Documents.Open($probe, $false, $false)
            $out = "report_output\_tools\probe_$tag.pdf"
            $full = Join-Path (Get-Location).Path $out
            & ([scriptblock]::Create($bodyText)) $doc $full
            "OK"
        } catch { "ERR: " + $_.Exception.Message }
        finally { try { $wd.Quit(0) } catch {} }
    } -ArgumentList $tag, $body.ToString(), $probe
    $done = Wait-Job $j -Timeout 60
    if ($done) { Log ("$tag -> " + (Receive-Job $j)) } else { Log "$tag -> TIMEOUT"; Stop-Job $j }
    Remove-Job $j -Force
}

Try-Export 'A' { param($doc, $full) $doc.ExportAsFixedFormat($full, 17) }
Try-Export 'B' { param($doc, $full) $doc.ExportAsFixedFormat($full, 17, $false, 0, 0, 1, 1, 0, $false, $false, 0, $false) }
Try-Export 'C' { param($doc, $full)
    $wd = [Runtime.InteropServices.Marshal]::GetActiveObject('Word.Application')
    $wd.ActivePrinter = 'Microsoft Print to PDF'
    $doc.PrintOut($false, $false, 0, $full)
}
Log 'done'
