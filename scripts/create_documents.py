from pathlib import Path
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'entrega'; OUT.mkdir(exist_ok=True)
results=json.loads((ROOT/'evidencias/resultados.json').read_text(encoding='utf-8'))
assert all(r['cumple'] for r in results)
answers=[
'El estado final será de 20 vacantes aunque se repita la petición cuatro veces. El PATCH asigna el valor absoluto recibido y no resta vacantes. Por ello, f(f(x)) = f(x). La prueba repitió cuatro veces la misma actualización y obtuvo 20 en todas las respuestas. Esto no equivale a reservar una vacante por estudiante, operación que requeriría otra lógica de concurrencia.',
'Se devuelve 401 porque no existe una identidad autenticada válida. La respuesta incluye WWW-Authenticate: Bearer y un problema JSON. El 403 corresponde a una identidad válida sin permiso para la acción. El 500 representa un fallo interno del servidor, no la ausencia de credenciales.'
]
f=Document(ROOT/'Ficha_Trabajo_Lab_Semana16_Sesion31_API_Matricula_UTP.docx')
f.tables[1].cell(4,1).text='24 / 11 / 2026     |     Modalidad: [  ] Individual   [  ] Grupal'
for row,r in zip(f.tables[14].rows[1:],results[:6]): row.cells[4].text=f'{r["obtenido"]}\nCumple'
f.tables[15].cell(0,0).text='EVIDENCIAS DE EJECUCIÓN\nLos casos CP-01 a CP-06 se ejecutaron contra Apache HTTP Server, Tomcat y MySQL. Las solicitudes y respuestas están en Informe_Implementacion_UTP.docx y evidencias/resultados.json. Cliente utilizado: script HTTP automatizado. Capturas de Postman: pendientes; se adjunta una colección para reproducirlas.'
f.tables[15].cell(0,0).text='EVIDENCIAS DE EJECUCIÓN\nCasos CP-01 a CP-06: ver Informe_Implementacion_UTP.docx y evidencias/resultados.json. Son registros HTTP automatizados. Capturas de Postman pendientes; colección importable adjunta.'
for par in f.paragraphs:
    if 'Respuesta: ___' in par.text:
        text=par.text
        for answer in answers:
            start=text.find('Respuesta: ___')
            if start<0: break
            end=text.find('\n',start)
            if end<0: end=len(text)
            text=text[:start]+'Respuesta: '+answer+text[end:]
        par.text=text
f.save(OUT/'Ficha_Completada_UTP.docx')
d=Document(); sec=d.sections[0]
sec.page_width=Inches(8.5); sec.page_height=Inches(11)
sec.top_margin=sec.bottom_margin=Inches(.7); sec.left_margin=sec.right_margin=Inches(.8)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2']:
    st=d.styles[name]; st.font.name='Calibri'; st.font.color.rgb=RGBColor(0,0,0)
d.styles['Normal'].font.size=Pt(11); d.styles['Normal'].paragraph_format.space_after=Pt(7)
d.styles['Normal'].paragraph_format.line_spacing=1.08
d.styles['Title'].font.size=Pt(26); d.styles['Heading 1'].font.size=Pt(16); d.styles['Heading 2'].font.size=Pt(12)
for style in d.styles:
    for border in list(style.element.iter(qn('w:pBdr'))): border.getparent().remove(border)
def p(text): return d.add_paragraph(text)
def h(text): return d.add_heading(text,1)
def code(text):
    q=d.add_paragraph(); q.paragraph_format.space_after=Pt(9); q.paragraph_format.line_spacing=1
    r=q.add_run(text); r.font.name='Consolas'; r.font.size=Pt(9)
def table(headers,rows,widths):
    t=d.add_table(rows=1,cols=len(headers)); t.autofit=False
    for c,w in zip(t.columns,widths): c.width=Inches(w)
    for c,text in zip(t.rows[0].cells,headers): c.text=text
    for row in rows:
        for c,text in zip(t.add_row().cells,row): c.text=str(text)
    for i,row in enumerate(t.rows):
        for j,c in enumerate(row.cells):
            c.width=Inches(widths[j]); props=c._tc.get_or_add_tcPr(); borders=OxmlElement('w:tcBorders')
            for edge in ['top','left','bottom','right']:
                el=OxmlElement('w:'+edge); el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'4'); el.set(qn('w:color'),'D9D9D9'); borders.append(el)
            props.append(borders)
            shade=OxmlElement('w:shd'); shade.set(qn('w:fill'),'E8EDF3' if i==0 else ('F7F9FB' if i%2==0 else 'FFFFFF')); props.append(shade)
            margins=OxmlElement('w:tcMar')
            for side in ['top','left','bottom','right']:
                el=OxmlElement('w:'+side); el.set(qn('w:w'),'90'); el.set(qn('w:type'),'dxa'); margins.append(el)
            props.append(margins)
            for par in c.paragraphs:
                par.paragraph_format.space_after=Pt(2)
                for run in par.runs: run.font.size=Pt(10); run.bold=i==0
    return t
d.add_paragraph('API RESTful de matrícula UTP','Title')
p('Informe de implementación y validación')
p('Desarrollo Web Integrado · Semana 16 · Sesión 31\nDocente: Mtro. Ing. César A. Cárdenas Latorre\nFecha: 24 de noviembre de 2026\nEstudiante: ____________________    Código UTP: ______________')
h('Resultado de la práctica')
p('Se implementó una aplicación Java con JAX-RS para consultar cursos por ciclo, ordenar con campos autorizados y actualizar vacantes de forma idempotente. Apache HTTP Server publica la aplicación mediante un proxy hacia Apache Tomcat y los registros se guardan en MySQL. Las 31 pruebas HTTP automatizadas finalizaron correctamente, incluidos los seis casos de la guía.')
h('Arquitectura y ejecución')
table(['Componente','Implementación'],[('Interfaz','HTML, CSS y JavaScript; acceso, filtros y edición de vacantes.'),('Servidor HTTP','Apache HTTP Server en 127.0.0.1:8089.'),('Aplicación Java','Apache Tomcat 10.1; Jersey 3.1 y Jakarta REST. WAR para Java 17 o superior.'),('Persistencia','MySQL 8; base utp_matricula_s16; tabla cursos con restricciones e índices.'),('Autenticación','JWT HS256 con firma, emisor, audiencia y expiración de 30 minutos.')],[1.5,5.4])
p('Flujo: navegador → Apache HTTP Server → Apache Tomcat → recursos JAX-RS → JDBC → MySQL. Jersey aporta JAX-RS a Tomcat. Se eligió Jakarta EE, admitido por la guía, y se mantuvieron las rutas /api/v1/cursos.')
h('Acceso y archivos')
p('Dirección local: http://127.0.0.1:8089/\nLas credenciales y la clave JWT se encuentran en config/local.properties, excluido del paquete de entrega. El WAR está en target/matricula.war. El README explica instalación, acceso y pruebas.')
d.add_page_break(); h('Implementación de los tres retos')
d.add_heading('Consulta con filtrado y orden seguro',2)
p('CursoResource valida ciclo entre 1 y 10, incluidos valores no numéricos. sort admite id, nombre, ciclo y vacantes, con prefijo opcional de orden descendente. CursoService transforma la clave validada en una columna definida por el servidor y usa PreparedStatement para los valores. Los empates se ordenan por ID.')
d.add_heading('Actualización parcial idempotente',2)
p('VacantesPatchDTO contiene solo Integer vacantes. Se rechazan campos desconocidos, valores nulos, negativos, decimales, cadenas, booleanos y enteros fuera de rango. La transacción bloquea el curso con SELECT FOR UPDATE y ejecuta UPDATE cursos SET vacantes=? WHERE id=?. Si no existe devuelve 404; si el cuerpo es inválido devuelve 400; una actualización válida devuelve 200 con el curso actualizado.')
d.add_heading('Protección con Bearer JWT',2)
p('JwtAuthFilter actúa antes del enrutamiento. Únicamente POST /api/auth/login es público, con coincidencia exacta de ruta. Se verifican estructura, firma HS256, emisor, audiencia, sujeto y expiración. Un token ausente, alterado o vencido devuelve 401. La interfaz mantiene el token en memoria y lo descarta al cerrar sesión.')
d.add_heading('Errores estructurados',2)
p('Se usa application/problem+json con type, title, status, detail e instance. Como extensiones se conservan timestamp, error, message y path. Los errores de deserialización también siguen este contrato y no exponen trazas internas.')
h('Matriz de validación')
table(['Caso','Operación','Esperado','Obtenido'],[(r['caso'],r['method']+' '+r['url'].split('/api')[1].split('?')[0],r['esperado'],str(r['obtenido'])+' Cumple') for r in results[:6]],[.65,3.65,1,1.6])
p('Cliente: scripts/test_api.py. Las evidencias siguientes son registros HTTP reales, no capturas de Postman. La colección importable permite reproducir los casos y capturarlos en ese cliente.')
for index in range(0,6,2):
    d.add_page_break(); h('Evidencias de los casos '+str(index+1)+' y '+str(index+2))
    for r in results[index:index+2]:
        d.add_heading(r['caso']+'  '+str(r['obtenido'])+'  Cumple',2)
        code(r['method']+' '+r['url']+'\nAuthorization: '+r['authorization']+'\nContent-Type: application/json'+('\nBody: '+json.dumps(r['body'],ensure_ascii=False) if r['body'] is not None else ''))
        resp=r['response']
        if isinstance(resp,list):
            code('[\n'+',\n'.join('  {"id":'+str(x['id'])+', "codigo":'+json.dumps(x['codigo'])+',\n   "nombre":'+json.dumps(x['nombre'],ensure_ascii=False)+',\n   "ciclo":'+str(x['ciclo'])+', "vacantes":'+str(x['vacantes'])+'}' for x in resp)+'\n]')
        else: code(json.dumps(resp,ensure_ascii=False,indent=2))
        p({'CP-01':'La petición sin identidad válida fue interceptada.','CP-02':'Todos los cursos corresponden al ciclo 6 y están ordenados por vacantes descendentes.','CP-03':'password no pertenece a la lista blanca.','CP-04':'La respuesta confirma la asignación absoluta de 20 vacantes.','CP-05':'El valor negativo fue rechazado sin modificar el registro.','CP-06':'El curso con ID 9999 no existe.'}[r['caso']])
d.add_page_break(); h('Metacognición y comprobaciones adicionales')
d.add_heading('Reintentos de la actualización',2); p(answers[0])
d.add_heading('Diferencia entre los códigos de error',2); p(answers[1])
h('Pruebas adicionales')
table(['Grupo','Validación'],[('Idempotencia','Cuatro PATCH sucesivos con 20 devuelven siempre 20.'),('Parámetros','Ciclos 0, 11, abc, 1.5 y vacío son rechazados. Una inyección en sort devuelve 400.'),('JSON','Se rechazan campos ausentes, nulos, JSON malformado, tipos incorrectos, desbordamiento y campos adicionales. Cero es válido.'),('JWT y acceso','Se rechazan tokens alterados, malformados y expirados; una ruta que contiene auth/login no elude el filtro; el login incorrecto devuelve 401.')],[1.5,5.4])
p('Resultado: 31 de 31 casos aprobados. El script restaura las vacantes iniciales al finalizar. Las respuestas completas se conservan en evidencias/resultados.json. Maven generó el WAR sin errores.')
h('Alcance y reproducción')
p('Es un laboratorio local con una cuenta administradora. La conexión HTTP se limita a esta máquina. Una publicación institucional requeriría HTTPS, gestión de usuarios con contraseñas derivadas mediante hash, limitación de intentos y credenciales MySQL de privilegios mínimos. El PATCH asigna disponibilidad; no realiza reservas individuales.')
p('Para reproducir: importar database/schema.sql, completar config/local.properties, ejecutar scripts/build.ps1, scripts/start.ps1 y scripts/start-apache.ps1, abrir la dirección local y ejecutar scripts/test_api.py. El README detalla los comandos y el procedimiento de Postman.')
d.save(OUT/'Informe_Implementacion_UTP.docx')
items=[{'name':'00 Login','request':{'method':'POST','header':[{'key':'Content-Type','value':'application/json'}],'body':{'mode':'raw','raw':'{"usuario":"{{usuario}}","clave":"{{clave}}"}'},'url':'{{baseUrl}}/api/auth/login'},'event':[{'listen':'test','script':{'type':'text/javascript','exec':['pm.test("Login 200", () => pm.response.to.have.status(200));','if (pm.response.code === 200) pm.collectionVariables.set("token", pm.response.json().access_token);']}}]}]
for r in results[:6]:
    headers=[{'key':'Content-Type','value':'application/json'}]
    if r['caso']!='CP-01': headers.append({'key':'Authorization','value':'Bearer {{token}}'})
    req={'method':r['method'],'header':headers,'url':'{{baseUrl}}/api'+r['url'].split('/api',1)[1]}
    if r['body'] is not None: req['body']={'mode':'raw','raw':json.dumps(r['body'])}
    tests=[f'pm.test("HTTP {r["esperado"]}", () => pm.response.to.have.status({r["esperado"]}));']
    if r['caso']=='CP-02': tests+=['pm.test("Filtro y orden", () => { const a=pm.response.json(); pm.expect(a.every(c=>c.ciclo===6)).to.be.true; pm.expect(a.every((c,i)=>i===0 || a[i-1].vacantes>=c.vacantes)).to.be.true; });']
    if r['caso']=='CP-04': tests+=['pm.test("Vacantes 20", () => pm.expect(pm.response.json().vacantes).to.eql(20));']
    items.append({'name':r['caso'],'request':req,'event':[{'listen':'test','script':{'type':'text/javascript','exec':tests}}]})
collection={'info':{'name':'Matrícula UTP Semana 16','schema':'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'},'variable':[{'key':'baseUrl','value':'http://127.0.0.1:8089'},{'key':'usuario','value':'admin'},{'key':'clave','value':''},{'key':'token','value':''}],'item':items}
(ROOT/'postman').mkdir(exist_ok=True)
(ROOT/'postman/Matricula_UTP.postman_collection.json').write_text(json.dumps(collection,ensure_ascii=False,indent=2),encoding='utf-8')
print('Documentos y colección Postman generados.')
