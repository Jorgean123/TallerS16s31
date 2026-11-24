param([string]$ApacheHome='C:\xampp\apache')
$ErrorActionPreference='Stop'
$project=Split-Path $PSScriptRoot -Parent
$base=Join-Path $project '.runtime\apache'
New-Item -ItemType Directory -Force $base | Out-Null
$ah=$ApacheHome.Replace('\','/'); $ab=$base.Replace('\','/')
$conf=@"
ServerRoot "$ah"
Listen 127.0.0.1:8089
ServerName localhost
LoadModule authz_core_module modules/mod_authz_core.so
LoadModule authz_host_module modules/mod_authz_host.so
LoadModule proxy_module modules/mod_proxy.so
LoadModule proxy_http_module modules/mod_proxy_http.so
ErrorLog "$ab/error.log"
PidFile "$ab/httpd.pid"
LogLevel warn
ProxyRequests Off
ProxyPreserveHost On
ProxyPass / http://127.0.0.1:8088/
ProxyPassReverse / http://127.0.0.1:8088/
<Location />
Require local
</Location>
"@
[IO.File]::WriteAllText("$base\httpd.conf",$conf)
& "$ApacheHome\bin\httpd.exe" -t -f "$base\httpd.conf"
if($LASTEXITCODE -ne 0) { throw 'Configuración Apache inválida.' }
if(Get-NetTCPConnection -LocalPort 8089 -State Listen -ErrorAction SilentlyContinue) { throw 'El puerto 8089 ya está en uso.' }
$p=Start-Process "$ApacheHome\bin\httpd.exe" -ArgumentList @('-f',('"'+$base+'\httpd.conf"')) -WindowStyle Hidden -PassThru
$p.Id | Set-Content "$base\parent.pid"
Write-Output 'Apache HTTP Server: http://localhost:8089/'
