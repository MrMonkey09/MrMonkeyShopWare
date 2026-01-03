// runtime/src/xboxkrnl/memory.cpp
// Implementación de stubs de memoria
// Generado por MrMonkeyShopWare

#include "xbox/xboxkrnl.h"
#include <cstdlib>
#include <cstdio>
#include <unordered_map>
#include <mutex>

namespace xbox::kernel {

// Memory tracking
static std::unordered_map<void*, size_t> g_allocations;
static std::mutex g_memMutex;
static size_t g_totalAllocated = 0;

PVOID XMemAlloc(size_t size, DWORD flags) {
    void* ptr = std::malloc(size);
    
    if (ptr) {
        std::lock_guard<std::mutex> lock(g_memMutex);
        g_allocations[ptr] = size;
        g_totalAllocated += size;
        
        // Debug: descomentar para tracking
        // printf("[XBOXKRNL] XMemAlloc: %zu bytes at %p (total: %zu)\n", 
        //        size, ptr, g_totalAllocated);
    }
    
    return ptr;
}

void XMemFree(PVOID ptr) {
    if (!ptr) return;
    
    {
        std::lock_guard<std::mutex> lock(g_memMutex);
        auto it = g_allocations.find(ptr);
        if (it != g_allocations.end()) {
            g_totalAllocated -= it->second;
            g_allocations.erase(it);
        }
    }
    
    std::free(ptr);
}

BOOL XVirtualProtect(
    PVOID lpAddress,
    size_t dwSize,
    DWORD flNewProtect,
    DWORD* lpflOldProtect
) {
    // TODO: Implementar con VirtualProtect en Windows
    // Por ahora, stub que siempre tiene éxito
    if (lpflOldProtect) {
        *lpflOldProtect = 0;
    }
    return TRUE;
}

// Utilidad: obtener memoria total asignada
size_t GetTotalAllocatedMemory() {
    std::lock_guard<std::mutex> lock(g_memMutex);
    return g_totalAllocated;
}

}  // namespace xbox::kernel
