# Frontend Dockerfile (Next.js)
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package.json ./
COPY package-lock.json* ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Expose port (Railway will set PORT env var)
EXPOSE 3000

# Set production environment
ENV NODE_ENV=production
ENV PORT=3000

# Start the application on Railway's PORT
CMD ["sh", "-c", "next start -p ${PORT}"]