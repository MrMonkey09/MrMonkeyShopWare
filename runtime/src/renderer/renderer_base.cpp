// runtime/src/renderer/renderer_base.cpp
// Implementación base del renderer y factory
// Generado por MrMonkeyShopWare

#include "renderer/renderer.h"
#include <cstdio>

namespace xbox::renderer {

// ═══════════════════════════════════════════════════════════════
// NULL RENDERER (Fallback/Testing)
// ═══════════════════════════════════════════════════════════════

class NullRenderer : public IRenderer {
public:
    bool Initialize(const RendererConfig& config) override {
        m_config = config;
        printf("[RENDERER] NullRenderer initialized\n");
        return true;
    }
    
    void Shutdown() override {
        printf("[RENDERER] NullRenderer shutdown\n");
    }
    
    void BeginFrame() override {}
    void EndFrame() override {}
    void Present() override {}
    
    TextureHandle CreateTexture(uint32_t, uint32_t, TextureFormat, const void*) override {
        return ++m_nextHandle;
    }
    
    void DestroyTexture(TextureHandle) override {}
    
    BufferHandle CreateBuffer(size_t, bool) override {
        return ++m_nextHandle;
    }
    
    void DestroyBuffer(BufferHandle) override {}
    void UpdateBuffer(BufferHandle, const void*, size_t) override {}
    
    ShaderHandle LoadShader(const std::string&, ShaderType) override {
        return ++m_nextHandle;
    }
    
    ShaderHandle CompileShader(const std::string&, ShaderType, const std::string&) override {
        return ++m_nextHandle;
    }
    
    void DestroyShader(ShaderHandle) override {}
    
    void SetViewport(float, float, float, float) override {}
    void SetScissor(int32_t, int32_t, uint32_t, uint32_t) override {}
    
    void BindTexture(uint32_t, TextureHandle) override {}
    void BindConstantBuffer(uint32_t, BufferHandle) override {}
    
    void Draw(uint32_t, uint32_t) override {}
    void DrawIndexed(uint32_t, uint32_t) override {}
    
    Backend GetBackend() const override { return Backend::None; }
    std::string GetDeviceName() const override { return "Null Renderer"; }
    Resolution GetResolution() const override { return m_config.resolution; }
    
    void OnResize(uint32_t w, uint32_t h) override {
        m_config.resolution.width = w;
        m_config.resolution.height = h;
    }
    
private:
    RendererConfig m_config;
    uint64_t m_nextHandle = 0;
};

// ═══════════════════════════════════════════════════════════════
// FACTORY IMPLEMENTATION
// ═══════════════════════════════════════════════════════════════

std::unique_ptr<IRenderer> CreateRenderer(Backend backend) {
    switch (backend) {
        case Backend::DirectX12:
            // TODO: return std::make_unique<DX12Renderer>();
            printf("[RENDERER] DX12 not yet implemented, using Null\n");
            return std::make_unique<NullRenderer>();
            
        case Backend::Vulkan:
            // TODO: return std::make_unique<VulkanRenderer>();
            printf("[RENDERER] Vulkan not yet implemented, using Null\n");
            return std::make_unique<NullRenderer>();
            
        case Backend::None:
        default:
            return std::make_unique<NullRenderer>();
    }
}

Backend DetectBestBackend() {
#ifdef _WIN32
    // En Windows, preferir DX12
    return Backend::DirectX12;
#else
    // En Linux/Mac, preferir Vulkan
    return Backend::Vulkan;
#endif
}

std::vector<Backend> GetAvailableBackends() {
    std::vector<Backend> backends;
    backends.push_back(Backend::None);  // Siempre disponible
    
#ifdef RUNTIME_DX12
    backends.push_back(Backend::DirectX12);
#endif

#ifdef RUNTIME_VULKAN
    backends.push_back(Backend::Vulkan);
#endif
    
    return backends;
}

}  // namespace xbox::renderer
