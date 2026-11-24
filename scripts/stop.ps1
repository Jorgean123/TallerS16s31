$base=Join-Path (Split-Path $PSScriptRoot -Parent) '.runtime\tomcat'
if(Test-Path "$base\server.pid") {
  $serverPid=[int](Get-Content "$base\server.pid")
  $p=Get-CimInstance Win32_Process -Filter "ProcessId=$serverPid"
  if($p -and $p.CommandLine.Contains($base) -and $p.CommandLine.Contains('org.apache.catalina.startup.Bootstrap')) { Stop-Process -Id $serverPid }
}
