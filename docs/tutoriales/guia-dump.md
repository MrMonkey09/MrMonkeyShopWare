# 📀 Tutorial: Dump de Disco

Guía detallada para hacer dump de un disco Xbox 360.

---

## 📋 Requisitos

- Unidad óptica compatible ([lista](http://wiki.redump.org/index.php?title=Dumping_Guides))
- DiscImageCreator instalado
- Disco Xbox 360 original

---

## 🚀 Pasos

### 1. Verificar unidad

```bash
# Ver unidades disponibles
wmic logicaldisk get caption,description,volumename
```

Identifica la letra de tu unidad óptica (ej: `E:`)

### 2. Insertar disco

Espera a que Windows reconozca el disco.

### 3. Ejecutar dump

**CLI:**
```bash
python -m src.cli.dump E: --out ./mi_juego.iso
```

**GUI:**
1. Iniciar: `python -m src.gui.main`
2. Click en "Dump Disc"
3. Ingresar letra de unidad

### 4. Esperar

El proceso toma 15-30 minutos. Verás progreso en consola/GUI.

---

## 📂 Salida

Por defecto: `%TEMP%\x360dump\game.iso`

Con `--out`: La ruta que especificaste

---

## ⚠️ Problemas Comunes

### "No se encontró DiscImageCreator"
→ Configurar ruta en `config.py` o variable de entorno

### "Error en dump"
→ Limpiar disco, verificar unidad compatible

### Dump muy lento
→ Normal para algunos discos, puede tomar hasta 45 min

---

## 📚 Ver también

- [DiscImageCreator](../herramientas/disc-image-creator.md)
- [Requisitos](../requisitos.md)
