// runtime/src/audio/audio_system.cpp
// Implementación base del sistema de audio
// Generado por MrMonkeyShopWare

#include "audio/audio_system.h"
#include <cstdio>
#include <unordered_map>

namespace xbox::audio {

// ═══════════════════════════════════════════════════════════════
// NULL AUDIO SYSTEM (Fallback/Testing)
// ═══════════════════════════════════════════════════════════════

class NullAudioSystem : public IAudioSystem {
public:
    bool Initialize(const AudioConfig& config) override {
        m_config = config;
        printf("[AUDIO] NullAudioSystem initialized (%u Hz, %u ch)\n",
               config.sampleRate, config.channels);
        return true;
    }
    
    void Shutdown() override {
        printf("[AUDIO] NullAudioSystem shutdown\n");
    }
    
    void Update() override {}
    
    SoundHandle LoadSound(const std::string& path) override {
        printf("[AUDIO] LoadSound: %s -> handle %llu\n", path.c_str(), m_nextHandle);
        return ++m_nextHandle;
    }
    
    SoundHandle LoadSoundFromMemory(const void*, size_t size, AudioFormat format) override {
        printf("[AUDIO] LoadSoundFromMemory: %zu bytes, format %d\n", size, (int)format);
        return ++m_nextHandle;
    }
    
    void UnloadSound(SoundHandle) override {}
    
    VoiceHandle Play(SoundHandle sound, bool loop) override {
        printf("[AUDIO] Play: sound %llu, loop=%d\n", sound, loop);
        return ++m_nextVoice;
    }
    
    void Stop(VoiceHandle) override {}
    void StopAll() override {}
    
    void SetVolume(VoiceHandle, float) override {}
    void SetPan(VoiceHandle, float) override {}
    void SetPitch(VoiceHandle, float) override {}
    
    bool IsPlaying(VoiceHandle) const override { return false; }
    
    void SetMasterVolume(float vol) override { m_masterVolume = vol; }
    float GetMasterVolume() const override { return m_masterVolume; }
    
    void SetListenerPosition(float, float, float) override {}
    void SetSourcePosition(VoiceHandle, float, float, float) override {}
    
    std::vector<int16_t> DecodeXMA(const void*, size_t size) override {
        // TODO: Implementar decodificador XMA real
        printf("[AUDIO] DecodeXMA: %zu bytes (stub - no audio)\n", size);
        return {};
    }
    
private:
    AudioConfig m_config;
    uint64_t m_nextHandle = 0;
    uint64_t m_nextVoice = 0;
    float m_masterVolume = 1.0f;
};

// ═══════════════════════════════════════════════════════════════
// FACTORY
// ═══════════════════════════════════════════════════════════════

std::unique_ptr<IAudioSystem> CreateAudioSystem() {
    // TODO: Crear sistema de audio real (XAudio2, OpenAL, etc.)
    return std::make_unique<NullAudioSystem>();
}

}  // namespace xbox::audio
