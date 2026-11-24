package pe.edu.utp.matricula.resource;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Map;
import pe.edu.utp.matricula.config.Settings;
import pe.edu.utp.matricula.dto.*;
import pe.edu.utp.matricula.security.JwtUtil;
@Path("/auth/login") @Produces(MediaType.APPLICATION_JSON)
public class AuthResource {
    private boolean equals(String a, String b) { return a != null && MessageDigest.isEqual(a.getBytes(StandardCharsets.UTF_8),b.getBytes(StandardCharsets.UTF_8)); }
    @POST @Consumes(MediaType.APPLICATION_JSON)
    public Response login(LoginDTO dto, @Context UriInfo uri) {
        if (dto == null || !equals(dto.usuario,Settings.get("auth.user")) || !equals(dto.clave,Settings.get("auth.password")))
            return ErrorResponse.response(401,"Credenciales incorrectas.",uri.getRequestUri().getPath());
        return Response.ok(Map.of("access_token",JwtUtil.issue(dto.usuario),"token_type","Bearer","expires_in",1800)).build();
    }
}
