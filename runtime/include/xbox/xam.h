// runtime/include/xbox/xam.h
// Xbox Abstraction Layer (XAM) - Stubs base
// Generado por MrMonkeyShopWare

#pragma once

#include "xboxkrnl.h"

namespace xbox::xam {

// ═══════════════════════════════════════════════════════════════
// CONTENT
// ═══════════════════════════════════════════════════════════════

/**
 * Crea un handle de contenido.
 */
DWORD XamContentCreate(
    DWORD dwUserIndex,
    LPCSTR pszRootName,
    PVOID pContentData,
    DWORD dwContentFlags,
    HANDLE* phContent
);

/**
 * Cierra un handle de contenido.
 */
DWORD XamContentClose(HANDLE hContent);

// ═══════════════════════════════════════════════════════════════
// USER INTERFACE
// ═══════════════════════════════════════════════════════════════

/**
 * Muestra un message box.
 * @return ID del botón presionado
 */
DWORD XamShowMessageBox(
    DWORD dwUserIndex,
    LPCSTR szTitle,
    LPCSTR szText,
    DWORD cButtons,
    LPCSTR* pszButtons,
    DWORD dwFocusButton,
    DWORD dwFlags
);

/**
 * Muestra teclado virtual.
 */
DWORD XamShowKeyboard(
    DWORD dwUserIndex,
    DWORD dwFlags,
    LPCSTR szDefaultText,
    LPCSTR szTitle,
    LPCSTR szDescription,
    LPVOID pszResultText,
    DWORD cchResultText
);

// ═══════════════════════════════════════════════════════════════
// USER PROFILE
// ═══════════════════════════════════════════════════════════════

/**
 * Obtiene información del usuario.
 */
DWORD XamUserGetSigninState(DWORD dwUserIndex);

/**
 * Obtiene el gamertag del usuario.
 */
DWORD XamUserGetGamertag(
    DWORD dwUserIndex,
    LPVOID pszGamertag,
    DWORD cchGamertag
);

// ═══════════════════════════════════════════════════════════════
// NETWORKING (Stubs - mayoría no implementados)
// ═══════════════════════════════════════════════════════════════

/**
 * Inicializa networking.
 */
DWORD XNetStartup();

/**
 * Finaliza networking.
 */
DWORD XNetCleanup();

// ═══════════════════════════════════════════════════════════════
// RUNTIME
// ═══════════════════════════════════════════════════════════════

/**
 * Inicializa XAM.
 */
bool Initialize();

/**
 * Finaliza XAM.
 */
void Shutdown();

}  // namespace xbox::xam
