# Step 1: Build the React app using Vite
FROM node:22-alpine AS build

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all source code
COPY ./ ./

# Set NODE_OPTIONS before running the build
ENV NODE_OPTIONS=--max-old-space-size=4096

# Build the production version of the app
RUN npm run build -- --mode production

# Step 2: Serve the app using Nginx
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the build files from the build stage to Nginx's html directory
COPY --from=build /app/dist /usr/share/nginx/html

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
