FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl git unzip wget software-properties-common \
    && apt-get clean

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python & app dependencies
COPY requirements.txt .
RUN apt-get install -y python3 python3-pip && pip3 install -r requirements.txt

COPY . /app
WORKDIR /app

# Start Ollama and FastAPI together
CMD ["bash", "-c", "ollama pull llama3 && ollama serve & uvicorn app:app --host 0.0.0.0 --port 5050"]
