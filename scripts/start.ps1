param([string]$TomcatHome='C:\apache-tomcat-10.1.59',[int]$Port=8088)
$ErrorActionPreference='Stop'
$project = Split-Path $PSScriptRoot -Parent
$base = Join-Path $project '.runtime\tomcat'
$config = Join-Path $project 'config\local.properties'
if (!(Test-Path $config)) { throw 'Configure config/local.properties antes de iniciar.' }
if (!(Test-Path "$project\target\matricula.war")) { throw 'Compile primero con Maven: mvn clean package' }
if (Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue) { throw "El puerto $Port ya está en uso." }
foreach($dir in @('conf','logs','temp','webapps','work')) { New-Item -ItemType Directory -Force -Path "$base\$dir" | Out-Null }
Copy-Item "$TomcatHome\conf\*" "$base\conf" -Force
$server = @"
<Server port="-1"><Service name="Catalina"><Connector address="127.0.0.1" port="$Port" protocol="HTTP/1.1" connectionTimeout="20000" URIEncoding="UTF-8"/><Engine name="Catalina" defaultHost="localhost"><Host name="localhost" appBase="webapps" unpackWARs="true" autoDeploy="true"/></Engine></Service></Server>
"@
[IO.File]::WriteAllText("$base\conf\server.xml",$server)
Copy-Item "$project\target\matricula.war" "$base\webapps\ROOT.war" -Force
$env:CATALINA_HOME=$TomcatHome
$env:CATALINA_BASE=$base
$env:MATRICULA_CONFIG=$config
$env:JAVA_HOME=Split-Path (Split-Path (Get-Command java).Source -Parent) -Parent
$java=Join-Path $env:JAVA_HOME 'bin\java.exe'
$arguments=@('-Dcatalina.home="'+$TomcatHome+'"','-Dcatalina.base="'+$base+'"','-Djava.io.tmpdir="'+$base+'\temp"','-Djava.util.logging.config.file="'+$base+'\conf\logging.properties"','-classpath','"'+$TomcatHome+'\bin\bootstrap.jar;'+$TomcatHome+'\bin\tomcat-juli.jar"','org.apache.catalina.startup.Bootstrap','start')
$proc=Start-Process -FilePath $java -ArgumentList $arguments -WindowStyle Hidden -PassThru -RedirectStandardOutput "$base\logs\stdout.log" -RedirectStandardError "$base\logs\stderr.log"
$proc.Id | Set-Content "$base\server.pid"
Write-Output "Tomcat iniciado (PID $($proc.Id)): http://localhost:$Port/"
