package pe.edu.utp.matricula.config;
import jakarta.ws.rs.core.*;
import jakarta.ws.rs.ext.*;
import com.fasterxml.jackson.core.JsonProcessingException;
import pe.edu.utp.matricula.dto.ErrorResponse;
@Provider
public class JsonExceptionMapper implements ExceptionMapper<JsonProcessingException> {
    @Context UriInfo uri;
    public Response toResponse(JsonProcessingException e) {
        return ErrorResponse.response(400,"JSON inválido: use únicamente los campos y tipos permitidos.",uri.getRequestUri().getPath());
    }
}
