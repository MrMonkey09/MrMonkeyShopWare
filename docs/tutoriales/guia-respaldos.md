# 📂 Guía: Métodos de Respaldo Xbox 360

Esta guía explica los diferentes métodos de respaldo de juegos Xbox 360 y cómo usarlos con MrMonkeyShopWare.

---

## 📊 Comparativa de Métodos

| Método | Origen | Formato | Soportado | Mejor para |
|--------|--------|---------|-----------|------------|
| **Disco físico** | Unidad óptica | DVD-DL | ✅ Dump | Juegos originales |
| **ISO** | Archivo | .iso | ✅ Pipeline | Respaldos descargados |
| **Carpetas USB** | Copia directa | Archivos | ✅ Analizar XEX | Respaldos de consola |
| **Disco virtual** | Imagen montada | Virtual | ❌ No soportado | - |
| **GOD/LIVE** | Xbox 360 | Contenedor | ⚠️ Parcial | Juegos digitales |

---

## 🔍 Explicación Detallada de Cada Método

### 📀 1. Disco Físico Original

**¿Qué es?**
El disco DVD-DL original del juego en la unidad óptica de tu PC.

**Características técnicas:**
- Formato: DVD-DL (Dual Layer, 8.5 GB)
- Protección: Sectores especiales XGD2/XGD3
- Requiere: Unidad óptica compatible con lectura raw

**Flujo en MrMonkeyShopWare:**
```
Disco físico → 📀 Dump Disc → ISO → Extracción → Análisis
```

**Ventajas:**
- ✅ Preserva toda la información del disco
- ✅ Genera ISO completa

**Limitaciones:**
- ❌ Necesitas unidad óptica compatible
- ❌ No todas las unidades pueden leer sectores raw
- ❌ Proceso lento (~30 min)

---

### 💿 2. Archivo ISO

**¿Qué es?**
Imagen completa del disco en un solo archivo .iso.

**Características técnicas:**
- Formato: ISO 9660 / Xbox 360 XDVDFS
- Tamaño: ~6-8 GB típicamente
- Contiene: Sistema de archivos completo del juego

**Flujo en MrMonkeyShopWare:**
```
archivo.iso → 🚀 Pipeline → Extracción → Análisis → BD
```

**Ventajas:**
- ✅ **Método más fácil** - solo arrastra el archivo
- ✅ No requiere hardware especial
- ✅ Pipeline completo automático

**Limitaciones:**
- ❌ ISOs grandes ocupan espacio

> [!TIP]
> **Este es el método recomendado** si ya tienes respaldos.

---

### 💾 3. Carpetas en USB (Copia directa)

**¿Qué es?**
Los archivos del juego copiados directamente a un USB o disco duro, sin comprimir.

**Origen típico:**
- Copiado desde Xbox 360 con homebrew (Aurora, FreeStyle)
- Extraído de una ISO previamente

**Estructura típica:**
```
USB:/
└── Games/
    └── Mi Juego [12345678]/
        ├── default.xex      ← Ejecutable principal
        ├── default.xexp     ← Datos de ejecución
        ├── game.exe
        └── Content/
            ├── data/
            └── ...
```

**Flujo en MrMonkeyShopWare:**
```
default.xex → 🔬 Analizar XEX → Análisis → BD
```

**Ventajas:**
- ✅ Acceso directo al XEX
- ✅ No necesita extracción
- ✅ Puedes analizar juegos individuales

**Limitaciones:**
- ❌ Puede faltar metadata del disco
- ❌ Debes encontrar el XEX manualmente

---

### 🖥️ 4. Disco Virtual (NO SOPORTADO)

**¿Qué es?**
Una ISO montada como unidad virtual usando software como:
- Daemon Tools
- Virtual CloneDrive
- Montador nativo de Windows 10/11

**¿Por qué no funciona?**

```
┌─────────────────────────────────────────────────────────┐
│  Disco Virtual vs Disco Físico                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Disco Físico:                                          │
│  [Sectores Raw] → [Driver] → [DiscImageCreator] ✅     │
│                                                         │
│  Disco Virtual:                                         │
│  [Archivo ISO] → [Emulación] → [Sistema de Archivos]   │
│                           ↓                             │
│                  DiscImageCreator ❌                    │
│                  (no ve sectores raw)                   │
└─────────────────────────────────────────────────────────┘
```

**DiscImageCreator** necesita acceso a los **sectores raw** del disco. Los discos virtuales solo emulan el sistema de archivos, no el hardware.

**Solución:**
```
❌ Montar ISO → Intentar dump
✅ Usar el archivo .iso directamente → Pipeline
```

---

### 📦 5. Formato GOD/LIVE (Parcial)

**¿Qué es?**
Contenedores de juegos descargados de Xbox Live o convertidos con herramientas.

**Características:**
- GOD: Games On Demand (juegos digitales)
- LIVE: Contenido descargable

**Soporte actual:**
- ⚠️ **Parcial** - debes extraer el contenido primero
- Usa herramientas como `god2iso` o `wxPirs`

**Flujo:**
```
archivo.god → [Herramienta externa] → ISO o carpetas → MrMonkeyShopWare
```

---

## 📈 ¿Cuál Método Usar?

```
                    ¿Tienes el disco original?
                              │
              ┌───────────────┼───────────────┐
              ▼               │               ▼
             Sí               │              No
              │               │               │
              ▼               │               ▼
    ¿Tienes unidad óptica     │    ¿Tienes archivo ISO?
     compatible?              │               │
         │                    │      ┌────────┼────────┐
    ┌────┴────┐               │      ▼        │        ▼
    ▼         ▼               │     Sí        │       No
   Sí        No               │      │        │        │
    │         │               │      ▼        │        ▼
    ▼         ▼               │   Pipeline    │  ¿Carpetas/USB?
📀 Dump   Busca ISO           │      ✅       │        │
            online            │               │   ┌────┴────┐
                              │               │   ▼         ▼
                              │               │  Sí        No
                              │               │   │         │
                              │               │   ▼         ▼
                              │               │ Analizar   Buscar
                              │               │  XEX ✅   respaldo
                              │               │
                              └───────────────┘
```

---

## 📊 Resumen Rápido

| Tienes | Usa esta vista | Acción |
|--------|----------------|--------|
| ISO como archivo | 🚀 Pipeline | Arrastra el .iso |
| Carpetas en USB | 🔬 Analizar XEX | Busca `default.xex` |
| Disco físico | � Dump Disc | Ingresa letra de unidad |
| ISO montada | ❌ | Desmonta y usa el archivo |

**Es el caso más fácil.**

1. Abre **MrMonkeyShopWare**
2. Ve a **🚀 Pipeline**
3. Arrastra tu archivo `.iso` a la zona de drop
4. El pipeline automáticamente:
   - Extrae el contenido
   - Encuentra el XEX principal
   - Analiza y extrae metadata
   - Genera project.toml
   - Guarda en historial

![Arrastrar ISO](./screenshots/drag_iso.png)

---

## 💾 Si tienes carpetas en USB

Cuando copiaste el juego desde la Xbox 360 a un USB, tienes las carpetas del juego directamente.

1. Conecta el USB
2. Abre **MrMonkeyShopWare**
3. Ve a **🔬 Analizar XEX**
4. Haz clic en la zona de drop
5. Navega a tu USB → carpeta del juego
6. Selecciona `default.xex` (el ejecutable principal)

### Estructura típica de un juego copiado:

```
USB:/
└── JUEGO/
    ├── default.xex     ← Selecciona este
    ├── default.xexp
    └── Content/
        └── ...
```

> [!TIP]
> Si no encuentras `default.xex`, busca cualquier archivo `.xex` en la carpeta.

---

## ❌ ISO en Disco Virtual (No Soportado)

**DiscImageCreator no funciona con discos virtuales** (como Daemon Tools o el montador de Windows).

### ¿Por qué?
DiscImageCreator necesita acceso "raw" al hardware de la unidad óptica para leer los sectores especiales de Xbox 360. Los discos virtuales emulan solo la capa de sistema de archivos, no el hardware.

### Solución:
**No montes la ISO**, usa el archivo directamente:

1. Desmonta el disco virtual
2. Usa el archivo `.iso` original
3. Arrástralo al **🚀 Pipeline**

---

## 🔧 Flujos Alternativos

```
┌─────────────────────────────────────────────────────────────┐
│                    ¿Qué tienes?                             │
└─────────────────────────────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
    Archivo ISO      Carpetas/USB      Disco físico
         │                 │                 │
         ▼                 ▼                 ▼
   🚀 Pipeline      🔬 Analizar XEX    📀 Dump Disc
         │                 │                 │
         └────────┬────────┘                 │
                  ▼                          ▼
           Análisis + BD ◄───────────────────┘
                  │
                  ▼
          📚 Historial
```

---

## 📚 Ver también

- [Pipeline Completo](./pipeline-completo.md)
- [Guía de Análisis](./guia-analisis.md)
- [Guía de Dump](./guia-dump.md)
