# Use the official Node.js image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json files
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the entire React project into the container
COPY . .

# Build the React application
RUN npm run build

# Install serve to serve the build directory
RUN npm install -g serve

# Set the environment variables
ENV NODE_ENV=production

# Start the application
CMD ["serve", "-s", "build"]
