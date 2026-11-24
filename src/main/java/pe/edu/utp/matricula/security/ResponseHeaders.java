package pe.edu.utp.matricula.security;
import jakarta.ws.rs.container.*;
import jakarta.ws.rs.ext.Provider;
@Provider
public class ResponseHeaders implements ContainerResponseFilter {
    public void filter(ContainerRequestContext req, ContainerResponseContext res) {
        res.getHeaders().putSingle("Cache-Control","no-store");
        res.getHeaders().putSingle("X-Content-Type-Options","nosniff");
    }
}
