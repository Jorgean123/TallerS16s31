$ErrorActionPreference='Stop'
$project=Split-Path $PSScriptRoot -Parent
$env:JAVA_HOME=Split-Path (Split-Path (Get-Command java).Source -Parent) -Parent
$env:MAVEN_OPTS='-Djavax.net.ssl.trustStoreType=Windows-ROOT -Djavax.net.ssl.trustStore=NUL'
$maven=Get-Command mvn -ErrorAction SilentlyContinue
if($maven) {$maven=$maven.Source} else {$maven=(Get-ChildItem "$env:USERPROFILE\.m2\wrapper" -Filter mvn.cmd -Recurse | Select-Object -First 1).FullName}
if(!$maven) {throw 'Instale Maven 3.9 y agréguelo al PATH.'}
Push-Location $project
try { $ErrorActionPreference='Continue'; & $maven -B clean package; $code=$LASTEXITCODE; $ErrorActionPreference='Stop'; if($code -ne 0){throw 'La compilación falló.'} } finally {Pop-Location}
