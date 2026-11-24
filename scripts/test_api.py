"""Pruebas HTTP reales. Ejecutar únicamente contra la base del laboratorio."""
import json, urllib.request, urllib.error, pathlib, base64, hmac, hashlib, time, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8089'
cfg = dict(line.strip().split('=',1) for line in (ROOT/'config/local.properties').read_text().splitlines() if '=' in line)
results=[]
def request(method,path,body=None,token=None,raw=None):
    headers={'Content-Type':'application/json'}
    if token is not None: headers['Authorization']='Bearer '+token
    data=raw.encode() if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req=urllib.request.Request(BASE+path,data=data,headers=headers,method=method)
    try: response=urllib.request.urlopen(req,timeout=15)
    except urllib.error.HTTPError as e: response=e
    content=response.read().decode()
    try: parsed=json.loads(content)
    except ValueError: parsed=content
    return response.status,parsed,dict(response.headers)
def case(name,method,path,expected,body=None,token=None,raw=None,check=lambda d:True):
    status,data,headers=request(method,path,body,token,raw)
    ok=status==expected and check(data)
    if expected>=400: ok=ok and headers.get('Content-Type','').startswith('application/problem+json') and isinstance(data,dict) and data.get('status')==expected
    item=dict(caso=name,method=method,url=BASE+path,authorization='Bearer <oculto>' if token else 'Ausente',body=raw if raw else body,esperado=expected,obtenido=status,cumple=ok,response=data)
    results.append(item); print(f'{name}: {status} '+('OK' if ok else 'FALLO'))
    return data
status,auth,_=request('POST','/api/auth/login',{'usuario':cfg['auth.user'],'clave':cfg['auth.password']})
assert status==200,auth
token=auth['access_token']
initial=request('GET','/api/v1/cursos',token=token)[1]
original=next(c['vacantes'] for c in initial if c['id']==1)
try:
    case('CP-01','GET','/api/v1/cursos',401)
    case('CP-02','GET','/api/v1/cursos?ciclo=6&sort=-vacantes',200,token=token,check=lambda d:len(d)>0 and all(c['ciclo']==6 for c in d) and [c['vacantes'] for c in d]==sorted([c['vacantes'] for c in d],reverse=True))
    case('CP-03','GET','/api/v1/cursos?sort=password',400,token=token)
    case('CP-04','PATCH','/api/v1/cursos/1',200,{'vacantes':20},token,check=lambda d:d['vacantes']==20)
    case('CP-05','PATCH','/api/v1/cursos/1',400,{'vacantes':-5},token)
    case('CP-06','PATCH','/api/v1/cursos/9999',404,{'vacantes':15},token)
    for i in range(4): case('Idempotencia-'+str(i+1),'PATCH','/api/v1/cursos/1',200,{'vacantes':20},token,check=lambda d:d['vacantes']==20)
    for value in ['0','11','abc','1.5','']:
        case('Ciclo-'+(value or 'vacio'),'GET','/api/v1/cursos?ciclo='+value,400,token=token)
    case('SQL-injection','GET','/api/v1/cursos?sort=id%3BDROP%20TABLE%20cursos',400,token=token)
    for label,payload in [('vacio',{}),('nulo',{'vacantes':None}),('decimal',{'vacantes':1.5}),('texto',{'vacantes':'20'}),('booleano',{'vacantes':True}),('desbordamiento',{'vacantes':2147483648}),('mass-assignment',{'vacantes':20,'nombre':'Hacked'})]:
        case('JSON-'+label,'PATCH','/api/v1/cursos/1',400,payload,token)
    case('JSON-malformado','PATCH','/api/v1/cursos/1',400,token=token,raw='{')
    case('JSON-null','PATCH','/api/v1/cursos/1',400,token=token,raw='null')
    case('Cero-valido','PATCH','/api/v1/cursos/1',200,{'vacantes':0},token,check=lambda d:d['vacantes']==0)
    case('JWT-alterado','GET','/api/v1/cursos',401,token=token[:len(token)//2]+'x'+token[len(token)//2+1:])
    case('JWT-malformado','GET','/api/v1/cursos',401,token='abc')
    def b64(v): return base64.urlsafe_b64encode(v).rstrip(b'=')
    header=b64(json.dumps({'alg':'HS256','typ':'JWT'}).encode())
    payload=b64(json.dumps({'sub':cfg['auth.user'],'iss':'utp-matricula','aud':['matricula-web'],'exp':int(time.time())-60}).encode())
    unsigned=header+b'.'+payload
    expired=(unsigned+b'.'+b64(hmac.new(base64.b64decode(cfg['jwt.secret']),unsigned,hashlib.sha256).digest())).decode()
    case('JWT-expirado','GET','/api/v1/cursos',401,token=expired)
    case('Bypass-login','GET','/api/v1/cursos/auth/login',401)
    case('Login-incorrecto','POST','/api/auth/login',401,{'usuario':'admin','clave':'incorrecta'})
finally:
    status,_,_=request('PATCH','/api/v1/cursos/1',{'vacantes':original},token)
    assert status==200,'No se restauraron las vacantes'
(ROOT/'evidencias').mkdir(exist_ok=True)
(ROOT/'evidencias/resultados.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{sum(r["cumple"] for r in results)}/{len(results)} casos aprobados. Vacantes originales restauradas.')
sys.exit(0 if all(r['cumple'] for r in results) else 1)
