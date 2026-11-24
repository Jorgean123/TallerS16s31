# Sistema de matrícula UTP

Java 17+, Jakarta REST/Jersey, Apache Tomcat 10.1, Apache HTTP Server y MySQL 8.

## Acceso

Abrir **http://127.0.0.1:8089/**. Usuario de demostración: **admin**. Consultar la contraseña de aplicación en `auth.password` del archivo privado `config/local.properties`. Es independiente de las credenciales de MySQL. La sesión JWT dura 30 minutos.

Apache HTTP Server escucha en 8089 y redirige a Tomcat en 8088. Ambos usan configuración dedicada en `.runtime`, sin modificar los servicios existentes.

## Instalar y ejecutar

1. Instalar JDK 17+, Maven 3.9, MySQL 8, Apache Tomcat 10.1 y Apache HTTP Server (XAMPP es válido).
2. Ejecutar `database/schema.sql` desde MySQL Workbench. Crea la base `utp_matricula_s16` y ocho cursos sin borrar registros existentes.
3. Copiar `config/local.properties.example` a `config/local.properties`. Completar credenciales y una clave JWT Base64 de al menos 32 bytes aleatorios. En esta máquina ya está configurado. No compartir este archivo: está excluido del ZIP y del WAR.
4. Ejecutar desde PowerShell:

```powershell
.\scripts\build.ps1
.\scripts\start.ps1 -TomcatHome 'C:\apache-tomcat-10.1.59'
.\scripts\start-apache.ps1 -ApacheHome 'C:\xampp\apache'
```

Maven usa el JDK del PATH y los certificados de Windows. Los scripts no detienen servicios ajenos si los puertos están ocupados. Para detener este proyecto:

```powershell
.\scripts\stop.ps1
& 'C:\xampp\apache\bin\httpd.exe' -k shutdown -f "$PWD\.runtime\apache\httpd.conf"
```

Para recompilar: detener ambos servidores, ejecutar build y arrancar otra vez. Logs: `.runtime/tomcat/logs` y `.runtime/apache/error.log`.

## API

| Método | Ruta | Función |
|---|---|---|
| POST | `/api/auth/login` | JSON con usuario y clave; devuelve access_token |
| GET | `/api/v1/cursos?ciclo=6&sort=-vacantes` | Consulta autenticada |
| PATCH | `/api/v1/cursos/1` | JSON `{"vacantes":20}`; asignación absoluta |

Enviar `Authorization: Bearer <access_token>`. Orden permitido: id, nombre, ciclo, vacantes; prefijo `-` para descendente. Ciclo válido: 1 a 10. PATCH solo acepta vacantes como entero no negativo. Los errores usan `application/problem+json` con RFC 7807 y extensiones de la guía.

## Pruebas y entrega

Ejecutar `python scripts/test_api.py` con Python 3. Solo usa biblioteca estándar. Realiza 31 pruebas HTTP y restaura las vacantes iniciales de ID 1 al terminar. Utilizar exclusivamente contra la base de laboratorio sin usuarios concurrentes. Resultados: `evidencias/resultados.json`.

Importar `postman/Matricula_UTP.postman_collection.json`. Completar la variable privada `clave` y ejecutar primero **00 Login**, cuyo script guarda el token. Ejecutar CP-01 a CP-06. CP-04 fija 20 vacantes; restaurar luego el valor previo mediante PATCH. Ocultar el token al tomar capturas.

En `entrega/` están la ficha completada y el informe. Nombre, código y modalidad del estudiante quedan pendientes. Las evidencias son registros HTTP automatizados; las capturas de Postman están pendientes. La revisión interactiva del navegador estuvo bloqueada por el entorno de automatización.

Fuentes Java: `src/main/java/pe/edu/utp/matricula`; interfaz: `src/main/webapp`; WAR: `target/matricula.war`. El WAR puede desplegarse como ROOT.war para mantener las rutas sin prefijo. La configuración privada se indica con `MATRICULA_CONFIG`.

El laboratorio utiliza root en MySQL según lo solicitado y una cuenta administradora local. Un despliegue público requiere HTTPS, privilegios mínimos, cuentas con contraseñas derivadas mediante hash y limitación de intentos. El PATCH administra un total disponible; no implementa una reserva individual.
