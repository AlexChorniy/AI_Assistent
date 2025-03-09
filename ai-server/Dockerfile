# Use official Node.js base image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of your app's code
COPY . .

# Expose the API port
EXPOSE 5000

# Start the Node.js application
CMD ["node", "ai-thunderbird.js"]
