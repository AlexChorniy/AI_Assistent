# Use official Node.js base image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your app's code
COPY . .

# Install system dependencies for LLaMA 2
RUN apt update && apt install -y build-essential cmake wget git curl

# Set up Hugging Face token from build arguments
ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}

# Download & build LLaMA.cpp
WORKDIR /app/llama
RUN git clone https://github.com/ggerganov/llama.cpp.git
WORKDIR /app/llama/llama.cpp
RUN mkdir build && cd build && cmake .. && cmake --build .

# Download LLaMA 2 (30B) model from Hugging Face
WORKDIR /app/llama
RUN curl -L -H "Authorization: Bearer ${HF_TOKEN}" \
     -o /app/llama/llama-2-30b.Q5_K_M.gguf \
     "https://huggingface.co/TheBloke/Llama-2-30B-GGUF/resolve/main/llama-2-30b.Q5_K_M.gguf"

# Expose the API port
EXPOSE 5000

# Start the Node.js application
CMD ["node", "ai-thunderbird.js"]
