"""Importa la base del laboratorio sin perder caracteres UTF-8."""
from pathlib import Path
import subprocess,os,sys
root=Path(__file__).resolve().parents[1]
config=dict(line.split('=',1) for line in (root/'config/local.properties').read_text().splitlines() if '=' in line)
mysql=sys.argv[1] if len(sys.argv)>1 else r'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe'
env=os.environ.copy(); env['MYSQL_PWD']=config['db.password']
subprocess.run([mysql,'--host=127.0.0.1','--user='+config['db.user'],'--default-character-set=utf8mb4'],input=(root/'database/schema.sql').read_bytes(),env=env,check=True)
print('Base importada sin eliminar registros existentes.')
