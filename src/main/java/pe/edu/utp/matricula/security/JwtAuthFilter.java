package pe.edu.utp.matricula.security;
import jakarta.annotation.Priority;
import jakarta.ws.rs.Priorities;
import jakarta.ws.rs.container.*;
import jakarta.ws.rs.ext.Provider;
import pe.edu.utp.matricula.dto.ErrorResponse;
@Provider @PreMatching @Priority(Priorities.AUTHENTICATION)
public class JwtAuthFilter implements ContainerRequestFilter {
    public void filter(ContainerRequestContext ctx) {
        String path = ctx.getUriInfo().getPath();
        if (path.equals("auth/login") && ctx.getMethod().equals("POST")) return;
        String h = ctx.getHeaderString("Authorization");
        if (h == null || !h.matches("(?i)Bearer [A-Za-z0-9_\\-]+\\.[A-Za-z0-9_\\-]+\\.[A-Za-z0-9_\\-]+") || !JwtUtil.esTokenValido(h.substring(7)))
            ctx.abortWith(ErrorResponse.response(401,"Cabecera Bearer ausente o token inválido, alterado o expirado.",ctx.getUriInfo().getRequestUri().getPath()));
    }
}
