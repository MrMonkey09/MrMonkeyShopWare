// runtime/include/audio/audio_system.h
// Sistema de Audio - Interfaz base
// Generado por MrMonkeyShopWare

#pragma once

#include <cstdint>
#include <string>
#include <memory>
#include <vector>
#include <functional>

namespace xbox::audio {

// ═══════════════════════════════════════════════════════════════
// ENUMS Y TIPOS
// ═══════════════════════════════════════════════════════════════

enum class AudioFormat {
    PCM16,      // PCM 16-bit
    PCM32F,     // PCM 32-bit float
    XMA2,       // Xbox Media Audio 2
    XWMA        // Xbox WMA
};

enum class SpeakerConfig {
    Stereo,     // 2.0
    Surround51, // 5.1
    Surround71  // 7.1
};

struct AudioConfig {
    uint32_t sampleRate = 48000;
    uint32_t channels = 2;
    SpeakerConfig speakers = SpeakerConfig::Stereo;
    uint32_t bufferSizeMs = 20;
};

// ═══════════════════════════════════════════════════════════════
// HANDLES
// ═══════════════════════════════════════════════════════════════

using SoundHandle = uint64_t;
using VoiceHandle = uint64_t;

constexpr SoundHandle INVALID_SOUND = 0;
constexpr VoiceHandle INVALID_VOICE = 0;

// ═══════════════════════════════════════════════════════════════
// INTERFAZ DE AUDIO
// ═══════════════════════════════════════════════════════════════

class IAudioSystem {
public:
    virtual ~IAudioSystem() = default;
    
    // Lifecycle
    virtual bool Initialize(const AudioConfig& config) = 0;
    virtual void Shutdown() = 0;
    virtual void Update() = 0;  // Llamar cada frame
    
    // Sound loading
    virtual SoundHandle LoadSound(const std::string& path) = 0;
    virtual SoundHandle LoadSoundFromMemory(
        const void* data, 
        size_t size, 
        AudioFormat format
    ) = 0;
    virtual void UnloadSound(SoundHandle handle) = 0;
    
    // Playback
    virtual VoiceHandle Play(SoundHandle sound, bool loop = false) = 0;
    virtual void Stop(VoiceHandle voice) = 0;
    virtual void StopAll() = 0;
    
    // Voice control
    virtual void SetVolume(VoiceHandle voice, float volume) = 0;  // 0.0 - 1.0
    virtual void SetPan(VoiceHandle voice, float pan) = 0;        // -1.0 (L) to 1.0 (R)
    virtual void SetPitch(VoiceHandle voice, float pitch) = 0;    // 0.5 - 2.0
    
    virtual bool IsPlaying(VoiceHandle voice) const = 0;
    
    // Master control
    virtual void SetMasterVolume(float volume) = 0;
    virtual float GetMasterVolume() const = 0;
    
    // 3D audio (optional)
    virtual void SetListenerPosition(float x, float y, float z) = 0;
    virtual void SetSourcePosition(VoiceHandle voice, float x, float y, float z) = 0;
    
    // XMA Decoding
    virtual std::vector<int16_t> DecodeXMA(const void* data, size_t size) = 0;
};

// ═══════════════════════════════════════════════════════════════
// FACTORY
// ═══════════════════════════════════════════════════════════════

/**
 * Crea el sistema de audio.
 */
std::unique_ptr<IAudioSystem> CreateAudioSystem();

}  // namespace xbox::audio
