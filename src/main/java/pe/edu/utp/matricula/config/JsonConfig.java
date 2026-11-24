package pe.edu.utp.matricula.config;
import com.fasterxml.jackson.databind.*;
import jakarta.ws.rs.ext.*;
@Provider
public class JsonConfig implements ContextResolver<ObjectMapper> {
    private final ObjectMapper mapper = new ObjectMapper()
        .enable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
        .disable(DeserializationFeature.ACCEPT_FLOAT_AS_INT)
        .disable(MapperFeature.ALLOW_COERCION_OF_SCALARS);
    public ObjectMapper getContext(Class<?> type) { return mapper; }
}
