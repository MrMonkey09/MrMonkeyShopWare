# Tutorial: Tu Primer Proyecto de Recompilación

Este tutorial te guía paso a paso para crear tu primer proyecto de recompilación usando MrMonkeyShopWare.

## Prerrequisitos

- [ ] MrMonkeyShopWare instalado
- [ ] Herramientas configuradas ([ver guía](../herramientas/configuracion-recompilacion.md))
- [ ] ISO de un juego Xbox 360 (legalmente obtenido)

---

## Paso 1: Crear Proyecto

1. Abre MrMonkeyShopWare
2. Click en **"Nuevo Proyecto"**
3. Selecciona tu archivo ISO
4. Elige una carpeta de destino

MrMonkeyShopWare automáticamente:
- Extrae el ISO
- Localiza el XEX principal
- Muestra información del juego

---

## Paso 2: Análisis Automático

1. Con el proyecto abierto, click **"Analizar"**
2. Espera a que complete:
   - ✅ Desencriptar XEX
   - ✅ Ejecutar XenonAnalyse
   - ✅ Generar jump tables

**Resultado:** Archivo `analysis.toml` con datos detectados.

---

## Paso 3: Configurar TOML

### Opción A: Usar Template

1. Click **"Generar Config"**
2. Revisa el archivo generado
3. **Las direcciones r14 estarán comentadas**

### Opción B: Configuración Manual

Si conoces las direcciones (de IDA/Ghidra):

```toml
# Descomentar y ajustar:
restgprlr_14_address = 0x831B0B40
savegprlr_14_address = 0x831B0AF0
```

> **💡 Tip:** El fork [XenonRecompUnlim](https://github.com/testdriveupgrade/XenonRecompUnlim) 
> puede detectar automáticamente algunas direcciones r14.

---

## Paso 4: Recompilar

1. Click **"Recompilar"**
2. Observa el progreso en el log
3. Verifica resultados:

```
✅ Archivos C++ generados: 127
   - ppc_recomp.00.cpp
   - ppc_recomp.01.cpp
   - ...
```

---

## Paso 5: Convertir Shaders

1. Click **"Convertir Shaders"**
2. Selecciona `shader.ar` (si existe)
3. Espera conversión a HLSL

---

## Paso 6: ¿Y ahora qué?

### Lo que tienes:
- ✅ Código C++ del juego
- ✅ Shaders en HLSL

### Lo que falta (trabajo de desarrollo):
- ❌ Runtime layer (xboxkrnl, XAM)
- ❌ Renderer (DX12/Vulkan)
- ❌ Sistema de audio
- ❌ Input handling

### Siguiente paso:

1. **Estudiar** [Unleashed Recompiled](https://github.com/hedge-dev/UnleashedRecomp) como referencia
2. **Unirse** a comunidades de recompilación
3. **Contribuir** al desarrollo del runtime

---

## Ejemplo Completo (CLI)

```python
from core import (
    extract_iso, find_main_xex, analyse_xex,
    XenonRecompConfig, generate_xenon_toml,
    run_recompilation, find_shader_files, batch_convert_shaders
)

# 1. Extraer
extracted = extract_iso("MiJuego.iso", "output/")
xex = find_main_xex(extracted)

# 2. Analizar
analysis = analyse_xex(xex, "output/analysis/")
print(f"Juego: {analysis.xex_info.display_name}")

# 3. Configurar
config = XenonRecompConfig(
    xex_path=xex,
    switch_table_path=analysis.toml_file
)
generate_xenon_toml(config, "output/config.toml")

# 4. Recompilar
result = run_recompilation("output/config.toml")
print(f"Generados: {len(result.cpp_files)} archivos C++")

# 5. Shaders
shaders = find_shader_files(extracted)
batch_convert_shaders(shaders, "output/hlsl/")
```

---

## Problemas Comunes

### "XenonRecomp no encontrado"

→ Verifica la ruta en Ajustes → Herramientas

### "Unrecognized instruction: xxx"

→ El juego usa instrucciones no implementadas. Consulta el [README de XenonRecomp](https://github.com/hedge-dev/XenonRecomp).

### "El TOML no es válido"

→ Revisa sintaxis TOML. Las direcciones deben ser hexadecimales: `0x831B0B40`

---

## ¿Necesitas ayuda?

- 📖 [Guía completa de recompilación](recompilacion-xbox360.md)
- 💬 [Discusiones de XenonRecomp](https://github.com/hedge-dev/XenonRecomp/discussions)
- 🎮 Discord de la comunidad
