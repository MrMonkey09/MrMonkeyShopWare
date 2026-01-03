// runtime/src/input/input_handler.cpp
// Implementación del sistema de input
// Generado por MrMonkeyShopWare

#include "input/input_handler.h"
#include <cstdio>
#include <cstring>

#ifdef _WIN32
#include <windows.h>
// XInput sería incluido aquí en implementación real
// #include <xinput.h>
#endif

namespace xbox::input {

// ═══════════════════════════════════════════════════════════════
// BASIC INPUT HANDLER (Keyboard/Mouse + Stub Gamepad)
// ═══════════════════════════════════════════════════════════════

class BasicInputHandler : public IInputHandler {
public:
    bool Initialize() override {
        printf("[INPUT] BasicInputHandler initialized\n");
        std::memset(&m_gamepads, 0, sizeof(m_gamepads));
        std::memset(&m_gamepadsPrev, 0, sizeof(m_gamepadsPrev));
        return true;
    }
    
    void Shutdown() override {
        printf("[INPUT] BasicInputHandler shutdown\n");
    }
    
    void Update() override {
        // Guardar estado anterior
        std::memcpy(&m_gamepadsPrev, &m_gamepads, sizeof(m_gamepads));
        m_keyboardPrev = m_keyboard;
        
        // Leer estado actual
        // En implementación real, aquí se usaría XInput/SDL
        
#ifdef _WIN32
        // Leer teclado desde GetAsyncKeyState
        for (int i = 0; i < 256; ++i) {
            m_keyboard.keys[i] = (GetAsyncKeyState(i) & 0x8000) != 0;
        }
        
        // Leer mouse
        POINT pt;
        if (GetCursorPos(&pt)) {
            m_mouse.deltaX = pt.x - m_mouse.x;
            m_mouse.deltaY = pt.y - m_mouse.y;
            m_mouse.x = pt.x;
            m_mouse.y = pt.y;
        }
        
        m_mouse.leftButton = (GetAsyncKeyState(VK_LBUTTON) & 0x8000) != 0;
        m_mouse.rightButton = (GetAsyncKeyState(VK_RBUTTON) & 0x8000) != 0;
        m_mouse.middleButton = (GetAsyncKeyState(VK_MBUTTON) & 0x8000) != 0;
#endif
        
        // Simular gamepad desde teclado (WASD + flechas)
        MapKeyboardToGamepad(0);
    }
    
    bool IsControllerConnected(uint32_t index) const override {
        // En implementación real, verificar con XInput
        return index == 0;  // Simular siempre player 1 conectado
    }
    
    GamepadState GetGamepadState(uint32_t index) const override {
        if (index < MAX_CONTROLLERS) return m_gamepads[index];
        return {};
    }
    
    GamepadState GetGamepadStatePrev(uint32_t index) const override {
        if (index < MAX_CONTROLLERS) return m_gamepadsPrev[index];
        return {};
    }
    
    void SetVibration(uint32_t index, const VibrationState&) override {
        // En implementación real, usar XInputSetState
        (void)index;
    }
    
    KeyboardState GetKeyboardState() const override { return m_keyboard; }
    KeyboardState GetKeyboardStatePrev() const override { return m_keyboardPrev; }
    MouseState GetMouseState() const override { return m_mouse; }
    
private:
    void MapKeyboardToGamepad(uint32_t index) {
        if (index >= MAX_CONTROLLERS) return;
        
        auto& gp = m_gamepads[index];
        gp.buttons = 0;
        
#ifdef _WIN32
        // Mapeo WASD -> Left Stick
        if (m_keyboard.IsKeyDown('W')) gp.leftThumbY = 32767;
        if (m_keyboard.IsKeyDown('S')) gp.leftThumbY = -32768;
        if (m_keyboard.IsKeyDown('A')) gp.leftThumbX = -32768;
        if (m_keyboard.IsKeyDown('D')) gp.leftThumbX = 32767;
        
        // Mapeo flechas -> Right Stick
        if (m_keyboard.IsKeyDown(VK_UP)) gp.rightThumbY = 32767;
        if (m_keyboard.IsKeyDown(VK_DOWN)) gp.rightThumbY = -32768;
        if (m_keyboard.IsKeyDown(VK_LEFT)) gp.rightThumbX = -32768;
        if (m_keyboard.IsKeyDown(VK_RIGHT)) gp.rightThumbX = 32767;
        
        // Botones
        if (m_keyboard.IsKeyDown(VK_SPACE)) gp.buttons |= static_cast<uint16_t>(Button::A);
        if (m_keyboard.IsKeyDown('E')) gp.buttons |= static_cast<uint16_t>(Button::B);
        if (m_keyboard.IsKeyDown('Q')) gp.buttons |= static_cast<uint16_t>(Button::X);
        if (m_keyboard.IsKeyDown('R')) gp.buttons |= static_cast<uint16_t>(Button::Y);
        if (m_keyboard.IsKeyDown(VK_RETURN)) gp.buttons |= static_cast<uint16_t>(Button::Start);
        if (m_keyboard.IsKeyDown(VK_ESCAPE)) gp.buttons |= static_cast<uint16_t>(Button::Back);
        if (m_keyboard.IsKeyDown(VK_LSHIFT)) gp.leftTrigger = 255;
        if (m_keyboard.IsKeyDown(VK_LCONTROL)) gp.rightTrigger = 255;
#endif
    }
    
    GamepadState m_gamepads[MAX_CONTROLLERS] = {};
    GamepadState m_gamepadsPrev[MAX_CONTROLLERS] = {};
    KeyboardState m_keyboard = {};
    KeyboardState m_keyboardPrev = {};
    MouseState m_mouse = {};
};

// ═══════════════════════════════════════════════════════════════
// FACTORY
// ═══════════════════════════════════════════════════════════════

std::unique_ptr<IInputHandler> CreateInputHandler() {
    return std::make_unique<BasicInputHandler>();
}

}  // namespace xbox::input
