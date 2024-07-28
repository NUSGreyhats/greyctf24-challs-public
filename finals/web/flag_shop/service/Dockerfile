# Use the official Node.js image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code to the container
COPY . .

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies
RUN npm install


# Expose the port that the app will run on
EXPOSE 33335

# Start the app
CMD [ "npm", "start" ]
