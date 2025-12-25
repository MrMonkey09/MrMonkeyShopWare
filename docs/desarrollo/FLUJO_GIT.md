# 🔀 Flujo de Trabajo Git

Guía del flujo de trabajo con Git para el proyecto MrMonkeyShopWare.

---

## 📊 Estructura de Ramas

```
main ────●────────────●────────────●───> (releases estables)
         │            │            │
       v0.1.0      v0.2.0       v0.3.0
         │            │            │
dev  ────┴────────────┴────────────┴───> (desarrollo continuo)
```

| Rama | Propósito |
|------|-----------|
| `main` | Versiones estables y releases |
| `dev` | Desarrollo activo |
| `feature/*` | Nuevas funcionalidades (opcional) |
| `fix/*` | Corrección de bugs (opcional) |

---

## 🚀 Desarrollo Diario

### 1. Trabajar en dev

```bash
# Asegurarte de estar en dev
git checkout dev

# Hacer cambios...

# Commit con convención
git add .
git commit -m "feat: descripción corta"

# Push
git push origin dev
```

### 2. Convención de Commits

| Prefijo | Uso |
|---------|-----|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de bug |
| `docs:` | Documentación |
| `style:` | Formato (no afecta lógica) |
| `refactor:` | Refactorización |
| `test:` | Tests |
| `chore:` | Tareas de mantenimiento |

**Ejemplos**:
```bash
git commit -m "feat: añadir comando scan-usb"
git commit -m "fix: corregir detección de workspace"
git commit -m "docs: actualizar README"
```

---

## 🎉 Crear Release

### Opción A: Merge Normal

```bash
# Ir a main
git checkout main

# Traer cambios de dev
git merge dev

# Crear tag
git tag v0.2.0

# Push con tags
git push origin main --tags
```

### Opción B: Squash (Historial Limpio)

```bash
git checkout main
git merge --squash dev
git commit -m "🎉 v0.2.0 - Descripción de cambios"
git push origin main
```

### Opción C: Reset Completo (Como v0.1.0)

Si quieres un solo commit limpio:

```bash
git checkout --orphan release-temp
git add -A
git commit -m "🎉 v0.2.0 - Descripción completa"
git branch -D main
git branch -m main
git push origin main --force
```

---

## 📋 Ejemplo de Mensaje de Release

```
🎉 v0.2.0 - Nombre del Release

Nuevas funcionalidades:
- feat: nueva característica 1
- feat: nueva característica 2

Correcciones:
- fix: corrección importante

Documentación:
- docs: guías actualizadas
```

---

## ⚠️ Reglas Importantes

1. **Nunca hacer force push a main** (excepto releases limpias planificadas)
2. **Siempre trabajar en dev** para desarrollo
3. **Crear backup** antes de operaciones destructivas
4. **Testear en dev** antes de merge a main

---

## 🔧 Comandos Útiles

```bash
# Ver estado
git status

# Ver ramas
git branch -a

# Ver historial
git log --oneline -10

# Ver diferencias
git diff

# Deshacer último commit (mantiene cambios)
git reset --soft HEAD~1

# Crear rama feature
git checkout -b feature/mi-feature

# Eliminar rama
git branch -d nombre-rama
```

---

## 📚 Ver también

- [Guía de Contribución](./CONTRIBUIR.md)
- [Guía de Estilo](./GUIA_DE_ESTILO.md)
