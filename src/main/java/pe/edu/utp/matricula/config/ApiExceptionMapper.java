package pe.edu.utp.matricula.config;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import jakarta.ws.rs.ext.*;
import com.fasterxml.jackson.core.JsonProcessingException;
import pe.edu.utp.matricula.dto.ErrorResponse;
@Provider
public class ApiExceptionMapper implements ExceptionMapper<Exception> {
    @Context UriInfo uri;
    public Response toResponse(Exception ex) {
        int status = ex instanceof WebApplicationException w ? w.getResponse().getStatus() : 500;
        Throwable cause = ex;
        while (cause != null) {
            if (cause instanceof JsonProcessingException) { status = 400; break; }
            cause = cause.getCause();
        }
        String message = switch(status) {
            case 400 -> "Solicitud inválida. Revise parámetros y cuerpo JSON.";
            case 404 -> "Recurso no encontrado.";
            case 405 -> "Método HTTP no permitido.";
            case 415 -> "Utilice Content-Type: application/json.";
            default -> "No se pudo procesar la solicitud.";
        };
        return ErrorResponse.response(status, message, uri.getRequestUri().getPath());
    }
}
