# ❓ Preguntas Frecuentes (FAQ)

## 📦 Instalación

### ¿Qué versión de Python necesito?
Python 3.11 o superior. Puedes verificar con `python --version`.

### ¿Funciona en Linux o Mac?
Parcialmente. El dump de discos requiere Windows, pero la extracción y análisis pueden funcionar en Linux con Wine o usando Docker.

### ¿Por qué necesito pywin32?
Se usa para detectar unidades ópticas en Windows mediante la API de Win32.

---

## 📀 Dump de Discos

### ¿Qué unidades ópticas son compatibles?
Consulta la [lista de redump.org](http://wiki.redump.org/index.php?title=Dumping_Guides). Las más recomendadas son LG GGC-H20L y Asus BW-16D1HT.

### ¿Por qué el dump falla?
Posibles causas:
- Disco rayado o sucio
- Unidad no compatible
- DiscImageCreator no configurado correctamente

### ¿Cuánto tiempo tarda un dump?
Generalmente 15-30 minutos dependiendo del estado del disco y la velocidad de la unidad.

---

## 📂 Extracción

### ¿Qué formato tienen los ISOs de Xbox 360?
Formato XISO (Xbox ISO). No son ISOs estándar y requieren `extract-xiso` para extraerlos.

### ¿Dónde se guardan los archivos extraídos?
Por defecto, en una carpeta con el mismo nombre que el ISO, junto a él.

---

## 🔍 Análisis

### ¿Qué es un archivo XEX?
Xbox Executable - El formato de ejecutable de Xbox 360. Contiene código PowerPC compilado.

### ¿Por qué necesito limpiar el XEX?
Los XEX vienen encriptados y comprimidos. xextool los desencripta y descomprime para que XenonAnalyse pueda analizarlos.

### ¿Qué contiene el analysis.toml?
Información sobre funciones, switch tables y metadatos necesarios para la recompilación.

---

## ⚙️ Configuración

### ¿Cómo cambio las rutas de las herramientas?
Tres opciones:
1. Editar `src/core/config.py`
2. Usar variables de entorno
3. Colocar herramientas en `C:\tools\`

### ¿Puedo usar rutas con espacios?
Sí, el código maneja rutas con espacios correctamente.

---

## ⚖️ Legal

### ¿Es legal usar este proyecto?
Sí, para uso personal con discos originales que poseas. No distribuyas ISOs ni builds recompilados.

### ¿Puedo compartir los juegos recompilados?
No. Los juegos recompilados siguen teniendo copyright. Solo para uso personal.

---

## 🐛 Problemas Comunes

### "No se encontró DiscImageCreator"
Descarga DiscImageCreator de redump.org y configura la ruta correctamente.

### "XenonAnalyse falló"
Asegúrate de que el XEX esté limpio (desencriptado y descomprimido).

### "Error al extraer ISO"
Verifica que el ISO no esté corrupto y que extract-xiso esté correctamente instalado.

---

## 💬 ¿Más preguntas?

- Abre un [Issue en GitHub](https://github.com/MrMonkey/MrMonkeyShopWare/issues)
- Únete a las [Discusiones](https://github.com/MrMonkey/MrMonkeyShopWare/discussions)
