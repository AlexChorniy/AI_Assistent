# Use official Node.js base image
FROM --platform=linux/amd64 node:18

# Set environment variable for Hugging Face Token
ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}

# Set the working directory for your app
WORKDIR /app

# Install required dependencies (wget, curl, git, cmake, build-essential)
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    cmake \
    build-essential \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js dependencies
COPY package*.json ./
RUN npm install

# Clone LLaMA.cpp and build it
WORKDIR /llama
RUN git clone https://github.com/ggerganov/llama.cpp.git
WORKDIR /llama/llama.cpp
RUN mkdir build && cd build && \
    cmake .. -DGGML_OPTIMIZE=OFF -DGGML_USE_FP16=OFF -DGGML_USE_SVE=OFF && \
    cmake --build . 

# Download the Yayi2 30B Llama model from Hugging Face
WORKDIR /llama
RUN wget --header="Authorization: Bearer ${HF_TOKEN}" \
    "https://huggingface.co/TheBloke/yayi2-30B-llama-GGUF/resolve/main/yayi2-30b-llama.Q5_K_M.gguf" \
    -O /llama/yayi2-30b-llama.Q5_K_M.gguf

# Copy the application source code
WORKDIR /app
COPY . .

# Expose API port
EXPOSE 8000

# Start the Node.js application
CMD ["node", "ai-thunderbird.js"]
