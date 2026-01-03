// runtime/include/renderer/renderer.h
// Abstracción de Renderer - Interfaz base
// Generado por MrMonkeyShopWare

#pragma once

#include <cstdint>
#include <string>
#include <vector>
#include <memory>
#include <functional>

namespace xbox::renderer {

// ═══════════════════════════════════════════════════════════════
// ENUMS Y TIPOS
// ═══════════════════════════════════════════════════════════════

enum class Backend {
    None,
    DirectX12,
    Vulkan
};

enum class ShaderType {
    Vertex,
    Pixel,
    Compute,
    Geometry
};

enum class TextureFormat {
    RGBA8,
    BGRA8,
    R8,
    R16F,
    R32F,
    RGBA16F,
    RGBA32F,
    BC1,    // DXT1
    BC3,    // DXT5
    BC7
};

struct Resolution {
    uint32_t width = 1280;
    uint32_t height = 720;
    bool fullscreen = false;
    bool vsync = true;
};

struct RendererConfig {
    Backend backend = Backend::DirectX12;
    Resolution resolution;
    uint32_t maxFramesInFlight = 2;
    bool debugMode = false;
    std::string shaderCachePath = "./shader_cache/";
};

// ═══════════════════════════════════════════════════════════════
// HANDLES
// ═══════════════════════════════════════════════════════════════

using TextureHandle = uint64_t;
using BufferHandle = uint64_t;
using ShaderHandle = uint64_t;
using PipelineHandle = uint64_t;

constexpr TextureHandle INVALID_TEXTURE = 0;
constexpr BufferHandle INVALID_BUFFER = 0;
constexpr ShaderHandle INVALID_SHADER = 0;
constexpr PipelineHandle INVALID_PIPELINE = 0;

// ═══════════════════════════════════════════════════════════════
// INTERFAZ BASE DEL RENDERER
// ═══════════════════════════════════════════════════════════════

class IRenderer {
public:
    virtual ~IRenderer() = default;
    
    // Lifecycle
    virtual bool Initialize(const RendererConfig& config) = 0;
    virtual void Shutdown() = 0;
    
    // Frame
    virtual void BeginFrame() = 0;
    virtual void EndFrame() = 0;
    virtual void Present() = 0;
    
    // Resources
    virtual TextureHandle CreateTexture(
        uint32_t width, uint32_t height,
        TextureFormat format,
        const void* data = nullptr
    ) = 0;
    
    virtual void DestroyTexture(TextureHandle handle) = 0;
    
    virtual BufferHandle CreateBuffer(
        size_t size,
        bool isConstant = false
    ) = 0;
    
    virtual void DestroyBuffer(BufferHandle handle) = 0;
    virtual void UpdateBuffer(BufferHandle handle, const void* data, size_t size) = 0;
    
    // Shaders
    virtual ShaderHandle LoadShader(
        const std::string& path,
        ShaderType type
    ) = 0;
    
    virtual ShaderHandle CompileShader(
        const std::string& source,
        ShaderType type,
        const std::string& entryPoint = "main"
    ) = 0;
    
    virtual void DestroyShader(ShaderHandle handle) = 0;
    
    // Drawing
    virtual void SetViewport(float x, float y, float width, float height) = 0;
    virtual void SetScissor(int32_t x, int32_t y, uint32_t width, uint32_t height) = 0;
    
    virtual void BindTexture(uint32_t slot, TextureHandle texture) = 0;
    virtual void BindConstantBuffer(uint32_t slot, BufferHandle buffer) = 0;
    
    virtual void Draw(uint32_t vertexCount, uint32_t startVertex = 0) = 0;
    virtual void DrawIndexed(uint32_t indexCount, uint32_t startIndex = 0) = 0;
    
    // Info
    virtual Backend GetBackend() const = 0;
    virtual std::string GetDeviceName() const = 0;
    virtual Resolution GetResolution() const = 0;
    
    // Resize
    virtual void OnResize(uint32_t width, uint32_t height) = 0;
};

// ═══════════════════════════════════════════════════════════════
// FACTORY
// ═══════════════════════════════════════════════════════════════

/**
 * Crea un renderer del backend especificado.
 * @param backend Backend a usar (DX12, Vulkan)
 * @return Puntero único al renderer
 */
std::unique_ptr<IRenderer> CreateRenderer(Backend backend);

/**
 * Detecta el mejor backend disponible en el sistema.
 */
Backend DetectBestBackend();

/**
 * Obtiene backends disponibles.
 */
std::vector<Backend> GetAvailableBackends();

}  // namespace xbox::renderer
