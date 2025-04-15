# AI LLaMA Server

This project sets up an AI-powered LLaMA server using Docker and Node.js. It pulls and runs a model from Hugging Face, integrating it with your application.

## Prerequisites

Ensure you have the following installed:
- Docker
- Docker Compose
- Node.js (if running locally)

## Setup Instructions

1. Clone the repository:
  git clone https://github.com/your-repo/ai-llama-server.git
  cd ai-llama-server
  

2. Create a `.env` file and add your Hugging Face token:
  echo "HF_TOKEN=your_huggingface_token" > .env
   

3. Build and start the Docker container:
   docker compose --env-file .env build --no-cache
   docker compose up -d


4. Chose required AI model
    https://huggingface.co/TheBloke/yayi2-30B-llama-GGUF
    change ling at lima-server/Dockerfile

5. Check Available Disk Space
    Run:
    df -h
    If your disk is full, you'll need to free up some space.

5. Clean Docker Cache & Unused Data
    Run:
    docker system prune -a --volumes
    This will remove all unused images, containers, and volumes.

6. Increase Docker Disk Space (If Using Docker Desktop)
    If you're on Docker Desktop, go to:

    Settings → Resources → Disk Image Size and increase the allocated space.
7. Remove Unused Docker Layers Manually
    Run:
    docker image prune -a
    docker volume prune
    docker container prune
8. Rebuild the Image
    After freeing up space, try building again:
    
    docker compose --env-file .env build --no-cache or  docker compose build --no-cache

    docker compose --env-file .env up -d

9. Start the containers
    docker compose up -d or docker compose up
10. Check logs if needed
    docker logs -f llama-server
    docker logs -f ai-server
11. After increasing the limit, use:
    docker logs -f --tail=500 llama-server // This will show the last 500 lines without truncation.

12. to pull AI model use next command line:
    curl -X POST http://localhost:11434/api/pull \
    -H "Content-Type: application/json" \
    -d '{"name": "llama3"}'

    to insure that model is pulled:
    curl http://localhost:11434/api/tags

    checking result request:  
    curl -X POST http://localhost:5050/generate \
    -H "Content-Type: application/json" \
    -d '{"prompt": "What is a black hole?"}'

## Accessing the Server

Once the server is running, access the API at:

http://localhost:4000


## Stopping the Server

To stop and remove the containers, run:

docker compose down


## Troubleshooting

- If you get a `401 Unauthorized` error when downloading the model, check your Hugging Face token.
- If the build fails, ensure you have enough system memory (LLaMA models are large!).
- Use `docker compose logs llama-server` to check logs for debugging.

## License
MIT License

