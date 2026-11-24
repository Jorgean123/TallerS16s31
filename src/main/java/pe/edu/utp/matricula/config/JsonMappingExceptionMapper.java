package pe.edu.utp.matricula.config;
import jakarta.ws.rs.core.*;
import jakarta.ws.rs.ext.*;
import jakarta.annotation.Priority;
import com.fasterxml.jackson.databind.JsonMappingException;
import pe.edu.utp.matricula.dto.ErrorResponse;
@Provider @Priority(1)
public class JsonMappingExceptionMapper implements ExceptionMapper<JsonMappingException> {
    @Context UriInfo uri;
    public Response toResponse(JsonMappingException e) {
        return ErrorResponse.response(400,"JSON inválido: revise los tipos y campos permitidos.",uri.getRequestUri().getPath());
    }
}
