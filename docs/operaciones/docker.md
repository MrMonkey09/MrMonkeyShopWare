# 🐳 Docker

Guía para usar Docker con MrMonkeyShopWare.

---

## 📋 Propósito

Docker se usa principalmente para compilar **XenonRecomp** en Linux, ya que facilita el proceso de build.

---

## 🚀 Inicio Rápido

```bash
cd docker
docker-compose up -d
docker exec -it xenonrecomp bash
```

---

## 📁 Archivos

| Archivo | Descripción |
|---------|-------------|
| `docker/Dockerfile` | Imagen con XenonRecomp compilado |
| `docker/docker-compose.yml` | Configuración del servicio |

---

## 🔧 Dockerfile

```dockerfile
FROM ubuntu:22.04

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    git cmake ninja-build clang llvm build-essential

# Clonar y compilar XenonRecomp
WORKDIR /opt
RUN git clone --recursive https://github.com/testdriveupgrade/XenonRecompUnlimited.git
WORKDIR /opt/XenonRecompUnlimited

# Parche para error de compilación
RUN sed -i 's/^static int lzxDecompress/int lzxDecompress/' \
    /opt/XenonRecompUnlimited/XenonUtils/xex_patcher.cpp

# Compilar
RUN mkdir build && cd build && \
    cmake .. -G Ninja \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_BUILD_TYPE=Release && \
    ninja

# Binarios en PATH
ENV PATH="/opt/XenonRecompUnlimited/build/XenonAnalyse:..."

WORKDIR /workspace
```

---

## 📂 Volúmenes

El `docker-compose.yml` monta:

```yaml
volumes:
  - ./workspace:/workspace
```

Coloca tus archivos XEX en `workspace/` para procesarlos dentro del contenedor.

---

## 💻 Uso

### Analizar XEX

```bash
docker exec -it xenonrecomp XenonAnalyse /workspace/default.xex /workspace/analysis.toml
```

### Recompilar

```bash
docker exec -it xenonrecomp XenonRecomp /workspace/project.toml /workspace/ppc_context.h
```

---

## 🔄 Rebuild

```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## 📚 Ver también

- [DESPLIEGUE.md](./DESPLIEGUE.md)
- [XenonRecomp](./herramientas/xenon-recomp.md)
