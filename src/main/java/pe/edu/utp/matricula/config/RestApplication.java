package pe.edu.utp.matricula.config;
import jakarta.ws.rs.ApplicationPath;
import org.glassfish.jersey.server.ResourceConfig;
import org.glassfish.jersey.jackson.JacksonFeature;
@ApplicationPath("/api")
public class RestApplication extends ResourceConfig {
    public RestApplication() { packages("pe.edu.utp.matricula"); register(JacksonFeature.class); }
}
