package pe.edu.utp.matricula.config;

import java.nio.file.*;
import java.util.Properties;

public final class Settings {
    private static final Properties VALUES = load();
    private static Properties load() {
        Properties p = new Properties();
        String file = System.getProperty("matricula.config", System.getenv("MATRICULA_CONFIG"));
        if (file == null) throw new IllegalStateException("Configure MATRICULA_CONFIG.");
        try (var in = Files.newInputStream(Path.of(file))) { p.load(in); return p; }
        catch (Exception e) { throw new IllegalStateException("No se pudo leer la configuración privada."); }
    }
    public static String get(String key) {
        String value = VALUES.getProperty(key);
        if (value == null || value.isBlank()) throw new IllegalStateException("Falta configuración: " + key);
        return value;
    }
    private Settings() {}
}
