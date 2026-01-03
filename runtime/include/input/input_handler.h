// runtime/include/input/input_handler.h
// Sistema de Input - Interfaz base
// Generado por MrMonkeyShopWare

#pragma once

#include <cstdint>
#include <string>
#include <functional>
#include <array>

namespace xbox::input {

// ═══════════════════════════════════════════════════════════════
// ENUMS - Compatible con Xbox 360 controller
// ═══════════════════════════════════════════════════════════════

enum class Button : uint16_t {
    DpadUp      = 0x0001,
    DpadDown    = 0x0002,
    DpadLeft    = 0x0004,
    DpadRight   = 0x0008,
    Start       = 0x0010,
    Back        = 0x0020,
    LeftThumb   = 0x0040,
    RightThumb  = 0x0080,
    LeftBumper  = 0x0100,
    RightBumper = 0x0200,
    A           = 0x1000,
    B           = 0x2000,
    X           = 0x4000,
    Y           = 0x8000,
};

// ═══════════════════════════════════════════════════════════════
// GAMEPAD STATE - Compatible con XINPUT_GAMEPAD
// ═══════════════════════════════════════════════════════════════

struct GamepadState {
    uint16_t buttons = 0;           // Bitmask de Button
    uint8_t leftTrigger = 0;        // 0-255
    uint8_t rightTrigger = 0;       // 0-255
    int16_t leftThumbX = 0;         // -32768 to 32767
    int16_t leftThumbY = 0;         // -32768 to 32767
    int16_t rightThumbX = 0;        // -32768 to 32767
    int16_t rightThumbY = 0;        // -32768 to 32767
    
    // Helpers
    bool IsPressed(Button btn) const {
        return (buttons & static_cast<uint16_t>(btn)) != 0;
    }
    
    float GetLeftTrigger() const { return leftTrigger / 255.0f; }
    float GetRightTrigger() const { return rightTrigger / 255.0f; }
    
    float GetLeftThumbX() const { return leftThumbX / 32767.0f; }
    float GetLeftThumbY() const { return leftThumbY / 32767.0f; }
    float GetRightThumbX() const { return rightThumbX / 32767.0f; }
    float GetRightThumbY() const { return rightThumbY / 32767.0f; }
};

// ═══════════════════════════════════════════════════════════════
// VIBRATION
// ═══════════════════════════════════════════════════════════════

struct VibrationState {
    uint16_t leftMotor = 0;   // 0-65535
    uint16_t rightMotor = 0;  // 0-65535
};

// ═══════════════════════════════════════════════════════════════
// KEYBOARD STATE (para PC)
// ═══════════════════════════════════════════════════════════════

struct KeyboardState {
    std::array<bool, 256> keys = {};
    
    bool IsKeyDown(uint8_t vkCode) const { return keys[vkCode]; }
};

// ═══════════════════════════════════════════════════════════════
// MOUSE STATE (para PC)
// ═══════════════════════════════════════════════════════════════

struct MouseState {
    int32_t x = 0;
    int32_t y = 0;
    int32_t deltaX = 0;
    int32_t deltaY = 0;
    int32_t scrollDelta = 0;
    bool leftButton = false;
    bool rightButton = false;
    bool middleButton = false;
};

// ═══════════════════════════════════════════════════════════════
// INPUT SYSTEM
// ═══════════════════════════════════════════════════════════════

constexpr uint32_t MAX_CONTROLLERS = 4;

class IInputHandler {
public:
    virtual ~IInputHandler() = default;
    
    // Lifecycle
    virtual bool Initialize() = 0;
    virtual void Shutdown() = 0;
    virtual void Update() = 0;  // Llamar cada frame
    
    // Gamepad
    virtual bool IsControllerConnected(uint32_t index) const = 0;
    virtual GamepadState GetGamepadState(uint32_t index) const = 0;
    virtual GamepadState GetGamepadStatePrev(uint32_t index) const = 0;
    
    // Vibration
    virtual void SetVibration(uint32_t index, const VibrationState& state) = 0;
    
    // Keyboard (PC)
    virtual KeyboardState GetKeyboardState() const = 0;
    virtual KeyboardState GetKeyboardStatePrev() const = 0;
    
    // Mouse (PC)
    virtual MouseState GetMouseState() const = 0;
    
    // Helpers
    bool WasButtonPressed(uint32_t index, Button btn) const {
        return GetGamepadState(index).IsPressed(btn) && 
               !GetGamepadStatePrev(index).IsPressed(btn);
    }
    
    bool WasButtonReleased(uint32_t index, Button btn) const {
        return !GetGamepadState(index).IsPressed(btn) && 
               GetGamepadStatePrev(index).IsPressed(btn);
    }
};

// ═══════════════════════════════════════════════════════════════
// FACTORY
// ═══════════════════════════════════════════════════════════════

/**
 * Crea el sistema de input.
 * Usa XInput en Windows, SDL/evdev en Linux.
 */
std::unique_ptr<IInputHandler> CreateInputHandler();

}  // namespace xbox::input
