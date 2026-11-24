package pe.edu.utp.matricula.security;
import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import javax.crypto.SecretKey;
import java.util.*;
import java.time.Instant;
import pe.edu.utp.matricula.config.Settings;
public final class JwtUtil {
    private static final SecretKey KEY = Keys.hmacShaKeyFor(Base64.getDecoder().decode(Settings.get("jwt.secret")));
    public static String issue(String user) {
        Instant now = Instant.now();
        return Jwts.builder().subject(user).issuer("utp-matricula").audience().add("matricula-web").and()
            .issuedAt(Date.from(now)).expiration(Date.from(now.plusSeconds(1800))).signWith(KEY,Jwts.SIG.HS256).compact();
    }
    public static boolean esTokenValido(String token) {
        try {
            if (token.length() > 4096 || token.split("\\.",-1).length != 3) return false;
            var jwt = Jwts.parser().verifyWith(KEY).requireIssuer("utp-matricula").requireAudience("matricula-web").build().parseSignedClaims(token);
            return "HS256".equals(jwt.getHeader().getAlgorithm()) && jwt.getPayload().getExpiration() != null
                && Settings.get("auth.user").equals(jwt.getPayload().getSubject());
        } catch (JwtException | IllegalArgumentException e) { return false; }
    }
    private JwtUtil() {}
}
