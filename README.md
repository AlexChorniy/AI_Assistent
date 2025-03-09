# AI Assistant for Thunderbird with LLaMA 2 (30B)
This project integrates an AI assistant into Thunderbird using LLaMA 2 (30B) as a backend model. The system is set up in a Dockerized environment to ensure portability and scalability.

# 📦 Prerequisites
Docker and Docker Compose installed on your machine
A Hugging Face account to obtain an access token for downloading models
# 🚀 Setup
1. Clone the repository
Clone this repository to your local machine:

git clone https://github.com/your-repo/ai-thunderbird.git
cd ai-thunderbird

2. Create a .env file
In the project root, create a .env file to store your Hugging Face token. This token will be used to authenticate and download the LLaMA model.

HF_TOKEN=your_huggingface_token_here
Get your Hugging Face token:

Go to Hugging Face Tokens
Click New Token and set it to Write permissions
Copy the generated token
Modify docker-compose.yml
Ensure that the .env file is referenced in the docker-compose.yml file. The docker-compose.yml is already configured to use the HF_TOKEN environment variable.

Example:

yaml
Copy
Edit
version: '3.8'
services:
  ai-thunderbird:
    build:
      context: .
      args:
        HF_TOKEN: ${HF_TOKEN}
    container_name: ai-thunderbird
    ports:
      - "5000:5000"
    restart: unless-stopped
    env_file:
      - .env
Build and Run the Docker Container

Build the Docker image and start the services:

bash
Copy
Edit
docker-compose --env-file .env build --no-cache
docker-compose up -d
The -d flag runs the container in detached mode.

⚙️ How It Works
LLaMA 2 Model Setup: The LLaMA model (30B) is downloaded from Hugging Face using the HF_TOKEN stored in the .env file.
Node.js App: The Node.js application runs in the container and integrates with Thunderbird. It uses LLaMA 2 for processing email data.
API Access: The AI assistant communicates through an API exposed on port 5000. You can customize this API to perform specific tasks like summarization, filtering, or answering email queries.
📂 Folder Structure
plaintext
Copy
Edit
ai-thunderbird/
├── Dockerfile               # Docker setup for Node.js and LLaMA 2
├── docker-compose.yml       # Docker Compose configuration
├── .env                     # Hugging Face token file
├── package.json             # Node.js dependencies
├── package-lock.json        # Lock file for npm
├── ai-thunderbird.js        # Main Node.js app
└── llama/
    └── llama.cpp            # LLaMA model and source code
🔧 Dockerfile Overview
The Dockerfile sets up the following:

Node.js Setup: The base image is node:18, which is used to install dependencies and run your Node.js app.
LLaMA Setup: It clones the llama.cpp repository, installs dependencies, and compiles the code using CMake.
Model Download: Downloads the LLaMA 2 model from Hugging Face using the curl command, authenticated with the HF_TOKEN.
⚡ Example Node.js Integration (ai-thunderbird.js)
javascript
Copy
Edit
const express = require('express');
const bodyParser = require('body-parser');
const fetch = require('node-fetch');

const app = express();
const port = 5000;

app.use(bodyParser.json());

// Example route to interact with the AI model
app.post('/ask', async (req, res) => {
  const { question } = req.body;

  try {
    // Call the LLaMA API (replace with your actual API endpoint if needed)
    const response = await fetch('http://localhost:5000/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: question }),
    });
    const data = await response.json();
    res.json(data);
  } catch (error) {
    res.status(500).send('Error querying the AI model');
  }
});

app.listen(port, () => {
  console.log(`AI Assistant listening at http://localhost:${port}`);
});
🔑 Environment Variables
HF_TOKEN: Your Hugging Face access token to authenticate model downloads.
Other environment variables: You can add more variables in .env as needed (e.g., for configuring AI behavior, the API key, etc.).
📊 API Endpoints
POST /ask: Send a question to the AI assistant.

Request body (JSON):

json
Copy
Edit
{
  "question": "How do I write a professional email?"
}
Example response:

json
Copy
Edit
{
  "answer": "To write a professional email, start with a formal greeting..."
}
⚠️ Troubleshooting
Model download fails (401 Unauthorized): Ensure that your Hugging Face token is correct and stored in .env.
Rebuild the Docker container with the --no-cache option.

bash
Copy
Edit
docker-compose --env-file .env build --no-cache
Docker container fails to start: Check the logs using docker-compose logs ai-thunderbird for detailed error messages.
Ensure all dependencies (like curl, git, cmake) are properly installed.

🔒 Security Considerations
Never expose your .env file publicly. It contains sensitive information like the Hugging Face token.
Use environment variables to store credentials securely, especially in production.
💡 Next Steps
Improve AI Email Features: Add more routes and features for email summarization, classification, etc.
Scale for Production: Optimize the Docker setup for production (e.g., multi-stage builds, caching strategies).
Thunderbird Integration: Integrate this setup directly with Thunderbird using the appropriate email APIs.
📚 Resources
Hugging Face Docs
LLaMA 2 GitHub
Node.js Express Documentation
