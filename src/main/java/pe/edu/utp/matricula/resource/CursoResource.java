package pe.edu.utp.matricula.resource;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.*;
import java.util.Set;
import java.sql.SQLException;
import pe.edu.utp.matricula.dto.*;
import pe.edu.utp.matricula.service.CursoService;
@Path("/v1/cursos") @Produces(MediaType.APPLICATION_JSON)
public class CursoResource {
    private final CursoService service = new CursoService();
    @Context UriInfo uri;
    private Response bad(String msg) { return ErrorResponse.response(400,msg,uri.getRequestUri().getPath()); }
    @GET
    public Response listarCursos(@QueryParam("ciclo") String rawCiclo, @DefaultValue("id") @QueryParam("sort") String sort) throws SQLException {
        Integer ciclo = null;
        if (rawCiclo != null) {
            try { ciclo = Integer.valueOf(rawCiclo); } catch(NumberFormatException e) { return bad("El ciclo debe ser un entero entre 1 y 10."); }
            if (ciclo < 1 || ciclo > 10) return bad("El ciclo debe estar entre 1 y 10.");
        }
        boolean desc = sort.startsWith("-"); String campo = desc ? sort.substring(1) : sort;
        if (!Set.of("id","nombre","ciclo","vacantes").contains(campo)) return bad("Campo de ordenamiento no permitido.");
        return Response.ok(service.buscarYOrdenar(ciclo,campo,desc)).build();
    }
    @PATCH @Path("/{id}") @Consumes(MediaType.APPLICATION_JSON)
    public Response actualizarVacantes(@PathParam("id") String rawId, VacantesPatchDTO dto) throws SQLException {
        long id;
        try { id = Long.parseLong(rawId); if(id < 1) return bad("El ID debe ser un entero positivo."); }
        catch(NumberFormatException e) { return bad("El ID debe ser un entero positivo."); }
        if (dto == null || dto.vacantes == null || dto.vacantes < 0) return bad("El campo vacantes es obligatorio y debe ser un entero mayor o igual a cero.");
        var curso = service.actualizarVacantes(id,dto.vacantes);
        if (curso == null) return ErrorResponse.response(404,"No existe un curso con ID: " + id,uri.getRequestUri().getPath());
        return Response.ok(curso).build();
    }
}
