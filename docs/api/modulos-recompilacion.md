# Referencia API: Módulos de Recompilación

Documentación de referencia para los módulos de recompilación Xbox 360 en MrMonkeyShopWare.

---

## xenos_shader_recomp

Módulo para conversión de shaders Xbox 360 a HLSL.

### Funciones

#### `check_xenos_recomp_available() -> bool`
Verifica si XenosRecomp está disponible.

#### `convert_shader(input_shader, output_hlsl, log=None, timeout=60) -> ShaderRecompResult`
Convierte un shader binario a HLSL.

**Parámetros:**
- `input_shader` (str): Ruta al shader binario
- `output_hlsl` (str): Ruta de salida HLSL
- `log` (Callable): Función de logging
- `timeout` (int): Timeout en segundos

**Retorna:** `ShaderRecompResult`

#### `batch_convert_shaders(shader_files, output_dir, log=None) -> Tuple[int, int, List[str]]`
Convierte múltiples shaders.

**Retorna:** `(éxitos, fallos, archivos_generados)`

#### `find_shader_files(game_dir) -> List[str]`
Busca archivos de shader en un directorio.

### Clases

#### `ShaderRecompResult`
```python
@dataclass
class ShaderRecompResult:
    success: bool
    hlsl_files: List[str]
    error: Optional[str]
    return_code: int
    stdout: str
    stderr: str
```

---

## xenon_toml_generator

Generador de archivos TOML para XenonRecomp.

### Funciones

#### `generate_xenon_toml(config, output_path, log=None) -> str`
Genera TOML en formato XenonRecomp.

**Parámetros:**
- `config` (XenonRecompConfig): Configuración
- `output_path` (str): Ruta de salida
- `log` (Callable): Función de logging

**Retorna:** Ruta al archivo generado

#### `generate_default_config(xex_path, output_dir, analysis_toml=None, patch_path=None, log=None) -> str`
Genera configuración con valores por defecto.

#### `update_toml_with_r14_addresses(toml_path, r14_addresses, log=None) -> bool`
Actualiza TOML con direcciones r14.

### Clases

#### `XenonRecompConfig`
```python
@dataclass
class XenonRecompConfig:
    # Rutas
    xex_path: str
    output_dir: str = "ppc"
    switch_table_path: Optional[str] = None
    patch_file_path: Optional[str] = None
    
    # Direcciones r14
    restgprlr_14: Optional[int] = None
    savegprlr_14: Optional[int] = None
    restfpr_14: Optional[int] = None
    savefpr_14: Optional[int] = None
    restvmx_14: Optional[int] = None
    savevmx_14: Optional[int] = None
    restvmx_64: Optional[int] = None
    savevmx_64: Optional[int] = None
    
    # setjmp/longjmp
    setjmp_address: Optional[int] = None
    longjmp_address: Optional[int] = None
    
    # Optimizaciones
    skip_lr: bool = False
    skip_msr: bool = False
    ctr_as_local: bool = False
    xer_as_local: bool = False
    reserved_as_local: bool = False
    cr_as_local: bool = False
    non_argument_as_local: bool = False
    non_volatile_as_local: bool = False
    
    # Avanzado
    functions: List[Dict[str, int]]
    invalid_instructions: List[Dict[str, int]]
    midasm_hooks: List[Dict[str, Any]]
```

---

## build_automation

Automatización de compilación con CMake y Clang.

### Funciones

#### `check_clang_available() -> Tuple[bool, Optional[str]]`
Verifica si Clang está disponible.

**Retorna:** `(disponible, versión)`

#### `check_cmake_available() -> Tuple[bool, Optional[str]]`
Verifica si CMake está disponible.

#### `generate_cmakelists(project_name, ppc_dir, output_path, additional_sources=None, log=None) -> str`
Genera CMakeLists.txt para el proyecto.

#### `build_with_cmake(project_dir, build_type="Release", generator=None, log=None, timeout=600) -> BuildResult`
Compila el proyecto con CMake.

#### `build_with_clang_direct(cpp_files, output_exe, include_dirs=None, log=None, timeout=600) -> BuildResult`
Compila directamente con Clang sin CMake.

#### `get_build_requirements() -> dict`
Obtiene estado de herramientas de build.

**Retorna:**
```python
{
    "clang": {"available": bool, "version": str},
    "cmake": {"available": bool, "version": str},
    "ready": bool
}
```

### Clases

#### `BuildResult`
```python
@dataclass
class BuildResult:
    success: bool
    executable_path: Optional[str]
    error: Optional[str]
    return_code: int
    stdout: str
    stderr: str
```

---

## Ejemplo de Uso Completo

```python
from core import (
    # Análisis
    analyse_xex, find_main_xex,
    
    # TOML
    XenonRecompConfig, generate_xenon_toml,
    
    # Recompilación
    run_recompilation,
    
    # Shaders
    find_shader_files, batch_convert_shaders,
    
    # Build
    generate_cmakelists, build_with_cmake,
    get_build_requirements
)

def recompile_game(xex_path: str, output_dir: str):
    """Pipeline completo de recompilación."""
    
    # 1. Verificar herramientas
    reqs = get_build_requirements()
    if not reqs["ready"]:
        raise RuntimeError("Clang no disponible")
    
    # 2. Analizar XEX
    analysis = analyse_xex(xex_path, f"{output_dir}/analysis")
    
    # 3. Generar configuración
    config = XenonRecompConfig(
        xex_path=xex_path,
        switch_table_path=analysis.toml_file
    )
    toml_path = generate_xenon_toml(config, f"{output_dir}/config.toml")
    
    # 4. Recompilar
    result = run_recompilation(toml_path)
    if not result.success:
        raise RuntimeError(result.error)
    
    # 5. Generar CMake
    generate_cmakelists("MiJuego", f"{output_dir}/ppc", f"{output_dir}/CMakeLists.txt")
    
    # 6. Compilar
    build_result = build_with_cmake(output_dir)
    
    return build_result.executable_path
```
