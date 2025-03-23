# Use official Node.js base image
FROM --platform=linux/amd64 node:18

# Set environment variable for Hugging Face Token
ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}

# Set the working directory
WORKDIR /app

# Install required dependencies
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

# Clone and build LLaMA.cpp
WORKDIR /llama
RUN git clone https://github.com/ggerganov/llama.cpp.git
WORKDIR /llama/llama.cpp
RUN mkdir build && cd build && cmake .. && cmake --build .

# Download the Yayi2 30B LLaMA model from Hugging Face
WORKDIR /llama
RUN wget --header="Authorization: Bearer ${HF_TOKEN}" \
    "https://huggingface.co/TheBloke/yayi2-30B-llama-GGUF/resolve/main/yayi2-30b-llama.Q5_K_M.gguf" \
    -O /llama/yayi2-30b-llama.Q5_K_M.gguf

# Copy application source code
WORKDIR /app
COPY . .

# Expose API port
EXPOSE 5050

# Start the LLaMA Server (adjust if necessary)
CMD ["node", "server.js"]
