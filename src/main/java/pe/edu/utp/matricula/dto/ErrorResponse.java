package pe.edu.utp.matricula.dto;
import java.time.Instant;
import jakarta.ws.rs.core.Response;
public class ErrorResponse {
    public final String type = "about:blank";
    public final String timestamp = Instant.now().toString();
    public final int status;
    public final String title, detail, instance, error, message, path;
    public ErrorResponse(int status, String message, String path) {
        this.status = status;
        var standard = Response.Status.fromStatusCode(status);
        this.title = standard == null ? "Error" : standard.getReasonPhrase();
        this.error = title; this.detail = message; this.message = message;
        this.instance = path; this.path = path;
    }
    public static Response response(int status, String message, String path) {
        var r = Response.status(status).type("application/problem+json").entity(new ErrorResponse(status,message,path));
        if (status == 401) r.header("WWW-Authenticate", "Bearer realm=\"matricula\"");
        return r.build();
    }
}
