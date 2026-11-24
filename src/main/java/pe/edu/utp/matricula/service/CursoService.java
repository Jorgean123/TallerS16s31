package pe.edu.utp.matricula.service;
import java.sql.*;
import java.util.*;
import pe.edu.utp.matricula.config.Settings;
import pe.edu.utp.matricula.model.Curso;
public class CursoService {
    private static final Map<String,String> COLUMNS = Map.of("id","id","nombre","nombre","ciclo","ciclo","vacantes","vacantes");
    private Connection connection() throws SQLException {
        return DriverManager.getConnection(Settings.get("db.url"),Settings.get("db.user"),Settings.get("db.password"));
    }
    private Curso read(ResultSet r) throws SQLException {
        return new Curso(r.getLong("id"),r.getString("codigo"),r.getString("nombre"),r.getInt("ciclo"),r.getInt("vacantes"));
    }
    public List<Curso> buscarYOrdenar(Integer ciclo, String campo, boolean desc) throws SQLException {
        String column = COLUMNS.get(campo);
        if (column == null) throw new IllegalArgumentException("Orden no permitido");
        String sql = "SELECT id,codigo,nombre,ciclo,vacantes FROM cursos" + (ciclo == null ? "" : " WHERE ciclo = ?")
            + " ORDER BY " + column + (desc ? " DESC" : " ASC") + (campo.equals("id") ? "" : ", id ASC");
        try (var c = connection(); var s = c.prepareStatement(sql)) {
            if (ciclo != null) s.setInt(1,ciclo);
            try(var r = s.executeQuery()) { List<Curso> list = new ArrayList<>(); while(r.next()) list.add(read(r)); return list; }
        }
    }
    public Curso actualizarVacantes(long id, int vacantes) throws SQLException {
        try(var c = connection()) {
            c.setAutoCommit(false);
            try {
                Curso result;
                try(var q = c.prepareStatement("SELECT id,codigo,nombre,ciclo,vacantes FROM cursos WHERE id=? FOR UPDATE")) {
                    q.setLong(1,id);
                    try(var r = q.executeQuery()) {
                        if (!r.next()) { c.rollback(); return null; }
                        Curso old = read(r);
                        result = new Curso(old.id(),old.codigo(),old.nombre(),old.ciclo(),vacantes);
                    }
                }
                try(var s = c.prepareStatement("UPDATE cursos SET vacantes=? WHERE id=?")) {
                    s.setInt(1,vacantes); s.setLong(2,id); s.executeUpdate();
                }
                c.commit(); return result;
            } catch(SQLException e) { c.rollback(); throw e; }
        }
    }
}
