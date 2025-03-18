# Use Node.js 18 as the base image
FROM node:18

# Set working directory
WORKDIR /app

# Install CA certificates to fix SSL issues
RUN apt-get update && apt-get install -y ca-certificates

# Install dependencies
COPY package*.json package-lock*.json ./
RUN npm install

# Copy the entire project
COPY . .

# Expose the required port (adjust based on your app's needs)
EXPOSE 4000

# Set environment variables (optional)
ENV NODE_ENV=production

# Start the application
CMD ["node", "index.js"]
