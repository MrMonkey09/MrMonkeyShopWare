FROM ubuntu:22.04

# Instalar dependencias básicas
RUN apt-get update && apt-get install -y \
    git cmake ninja-build clang llvm build-essential \
    && rm -rf /var/lib/apt/lists/*

# Clonar el repo XenonRecompUnlimited
WORKDIR /opt
RUN git clone --recursive https://github.com/testdriveupgrade/XenonRecompUnlimited.git
WORKDIR /opt/XenonRecompUnlimited

# Parche rápido para el error de lzxDecompress duplicado
RUN sed -i 's/^static int lzxDecompress/int lzxDecompress/' /opt/XenonRecompUnlimited/XenonUtils/xex_patcher.cpp

# Compilar en Release
RUN mkdir build && cd build && \
    cmake .. -G Ninja -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_BUILD_TYPE=Release && \
    ninja

# Añadir binarios al PATH
ENV PATH="/opt/XenonRecompUnlimited/build/XenonAnalyse:/opt/XenonRecompUnlimited/build/XenonRecomp:$PATH"

# Carpeta de trabajo (montada desde el host)
WORKDIR /workspace
