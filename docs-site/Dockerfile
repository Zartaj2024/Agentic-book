FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production

# Copy the rest of the application
COPY . .

# Build the site
RUN npm run build

# Serve the built site using a simple server
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Serve the built site
CMD ["serve", "-s", "build", "-l", "3000"]