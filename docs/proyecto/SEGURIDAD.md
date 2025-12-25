# 🔒 Seguridad

Políticas de seguridad del proyecto.

---

## 📢 Reportar Vulnerabilidades

Si descubres una vulnerabilidad de seguridad, **NO** abras un issue público.

### Proceso

1. Envía email a [seguridad@ejemplo.com]
2. Incluye:
   - Descripción del problema
   - Pasos para reproducir
   - Impacto potencial
3. Espera respuesta en 48 horas

---

## 🔐 Alcance

### En alcance

- Código del repositorio
- Dependencias directas
- Configuración por defecto

### Fuera de alcance

- Herramientas externas (DiscImageCreator, etc.)
- Infraestructura de terceros

---

## 🛡️ Prácticas de Seguridad

### Código

- No ejecutar comandos arbitrarios
- Sanitizar todas las rutas de archivo
- No exponer credenciales en logs

### Dependencias

- Mantener dependencias actualizadas
- Revisar `pip audit` regularmente
- Usar `requirements.txt` con versiones fijas

---

## 📋 Versiones Soportadas

| Versión | Soporte |
|---------|---------|
| 0.1.x   | ✅ Actual |
| < 0.1   | ❌ No soportado |

---

## 📚 Ver también

- [CODIGO_DE_CONDUCTA.md](./CODIGO_DE_CONDUCTA.md)
