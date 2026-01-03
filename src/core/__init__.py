# Core - Lógica principal de MrMonkeyShopWare
from .config import *
from .dumper import dump_disc
from .extractor import extract_iso, list_xex_files
from .analyser import analyse_xex
from .cleaner_xex import clean_xex
from .toml_generator import generate_project_toml, validate_project_toml
from .pipeline import full_pipeline, find_main_xex, PipelineResult
from .database import GameDatabase, Game, GameStatus
from .shader_recomp import run_recompilation, RecompResult, validate_recomp_output, check_xenon_recomp_available
from .game_profiles import GameProfile, ProfileManager
from .logger import get_logger, setup_logging, add_gui_handler, GUILogHandler

# Módulos de recompilación
from .xenos_shader_recomp import (
    convert_shader, convert_shader_archive, find_shader_files,
    batch_convert_shaders, check_xenos_recomp_available, ShaderRecompResult
)
from .xenon_toml_generator import (
    XenonRecompConfig, generate_xenon_toml, generate_default_config,
    update_toml_with_r14_addresses
)
from .build_automation import (
    BuildResult, check_clang_available, check_cmake_available,
    generate_cmakelists, build_with_cmake, build_with_clang_direct,
    get_build_requirements
)

# Scaffolding y Reference Extractor
from .scaffolding import (
    ProjectConfig, ScaffoldResult, create_project_scaffold,
    update_project_scaffold, validate_project_structure
)
from .reference_extractor import (
    FunctionStub, ExtractionResult, extract_from_repository,
    compare_game_requirements, generate_stubs_header, generate_stubs_implementation,
    extract_function_list_from_xenia
)
