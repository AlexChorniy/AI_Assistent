FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY . .

# Upgrade pip and install core dependencies
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --upgrade transformers\
 && pip install --no-cache-dir fastapi uvicorn python-dotenv transformers accelerate torch pillow \
 && pip install --no-cache-dir "huggingface_hub[hf_xet]"

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 5050

# Command to run FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5050"]
