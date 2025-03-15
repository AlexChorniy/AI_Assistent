# Use official Node.js base image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (if available) first
COPY package.json package-lock.json ./

# Ensure package.json exists, if not, create it inside the container
RUN test -f package.json || npm init -y

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Expose the API port
EXPOSE 5000

# Start the Node.js application
CMD ["node", "ai-thunderbird.js"]
