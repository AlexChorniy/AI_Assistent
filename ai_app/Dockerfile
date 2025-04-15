# Use a smaller base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Install CA certificates to fix SSL issues
RUN apk add --no-cache ca-certificates

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install --omit=dev

# Copy the rest of the application files
COPY . .

# Build the application
RUN npm run build

# Expose the required port
EXPOSE 4000

# Set environment variables (optional)
ENV NODE_ENV=production

# Start the application
CMD ["node", "build/server.js"]
