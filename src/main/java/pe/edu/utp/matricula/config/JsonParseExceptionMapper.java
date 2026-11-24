package pe.edu.utp.matricula.config;
import jakarta.ws.rs.core.*;
import jakarta.ws.rs.ext.*;
import jakarta.annotation.Priority;
import com.fasterxml.jackson.core.JsonParseException;
import pe.edu.utp.matricula.dto.ErrorResponse;
@Provider @Priority(1)
public class JsonParseExceptionMapper implements ExceptionMapper<JsonParseException> {
    @Context UriInfo uri;
    public Response toResponse(JsonParseException e) {
        return ErrorResponse.response(400,"El cuerpo no es un JSON válido.",uri.getRequestUri().getPath());
    }
}
