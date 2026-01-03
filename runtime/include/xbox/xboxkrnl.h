// runtime/include/xbox/xboxkrnl.h
// Xbox 360 Kernel Stubs - Base compartida
// Generado por MrMonkeyShopWare

#pragma once

#include <cstdint>
#include <functional>

// Tipos básicos Xbox 360
typedef uint32_t DWORD;
typedef int32_t LONG;
typedef uint32_t ULONG;
typedef void* HANDLE;
typedef void* PVOID;
typedef void* LPVOID;
typedef const char* LPCSTR;
typedef uint16_t WORD;
typedef uint8_t BYTE;
typedef int BOOL;
typedef uint64_t ULONGLONG;

#define TRUE 1
#define FALSE 0
#define INVALID_HANDLE_VALUE ((HANDLE)(intptr_t)-1)

namespace xbox::kernel {

// ═══════════════════════════════════════════════════════════════
// THREADING
// ═══════════════════════════════════════════════════════════════

typedef DWORD (*LPTHREAD_START_ROUTINE)(LPVOID lpParameter);

/**
 * Crea un nuevo thread.
 * @param lpStartAddress Función de inicio
 * @param lpParameter Parámetro para la función
 * @param dwCreationFlags Flags de creación
 * @param lpThreadId ID del thread creado (output)
 * @return Handle al thread o INVALID_HANDLE_VALUE
 */
HANDLE XCreateThread(
    LPTHREAD_START_ROUTINE lpStartAddress,
    LPVOID lpParameter,
    DWORD dwCreationFlags,
    DWORD* lpThreadId
);

/**
 * Espera a que un objeto se señalice.
 */
DWORD XWaitForSingleObject(HANDLE hHandle, DWORD dwMilliseconds);

/**
 * Termina el thread actual.
 */
void XExitThread(DWORD dwExitCode);

// ═══════════════════════════════════════════════════════════════
// MEMORY
// ═══════════════════════════════════════════════════════════════

/**
 * Reserva memoria.
 */
PVOID XMemAlloc(size_t size, DWORD flags);

/**
 * Libera memoria.
 */
void XMemFree(PVOID ptr);

/**
 * Cambia protección de memoria.
 */
BOOL XVirtualProtect(
    PVOID lpAddress,
    size_t dwSize,
    DWORD flNewProtect,
    DWORD* lpflOldProtect
);

// ═══════════════════════════════════════════════════════════════
// SYNC
// ═══════════════════════════════════════════════════════════════

/**
 * Crea un evento.
 */
HANDLE XCreateEvent(
    BOOL bManualReset,
    BOOL bInitialState,
    LPCSTR lpName
);

/**
 * Señaliza un evento.
 */
BOOL XSetEvent(HANDLE hEvent);

/**
 * Resetea un evento.
 */
BOOL XResetEvent(HANDLE hEvent);

/**
 * Crea una sección crítica.
 */
void XInitializeCriticalSection(PVOID lpCriticalSection);

/**
 * Entra a sección crítica.
 */
void XEnterCriticalSection(PVOID lpCriticalSection);

/**
 * Sale de sección crítica.
 */
void XLeaveCriticalSection(PVOID lpCriticalSection);

// ═══════════════════════════════════════════════════════════════
// FILE I/O
// ═══════════════════════════════════════════════════════════════

/**
 * Abre un archivo.
 */
HANDLE XCreateFile(
    LPCSTR lpFileName,
    DWORD dwDesiredAccess,
    DWORD dwShareMode,
    DWORD dwCreationDisposition
);

/**
 * Lee de un archivo.
 */
BOOL XReadFile(
    HANDLE hFile,
    LPVOID lpBuffer,
    DWORD nNumberOfBytesToRead,
    DWORD* lpNumberOfBytesRead
);

/**
 * Cierra un handle.
 */
BOOL XCloseHandle(HANDLE hObject);

// ═══════════════════════════════════════════════════════════════
// CRYPTO (Stubs básicos)
// ═══════════════════════════════════════════════════════════════

/**
 * SHA hash.
 */
DWORD XeCryptSha(
    const BYTE* pbInput1, DWORD cbInput1,
    const BYTE* pbInput2, DWORD cbInput2,
    const BYTE* pbInput3, DWORD cbInput3,
    BYTE* pbDigest, DWORD cbDigest
);

// ═══════════════════════════════════════════════════════════════
// RUNTIME INITIALIZATION
// ═══════════════════════════════════════════════════════════════

/**
 * Inicializa el runtime de Xbox.
 * Debe llamarse antes de cualquier función del kernel.
 */
bool Initialize();

/**
 * Finaliza el runtime.
 */
void Shutdown();

}  // namespace xbox::kernel
