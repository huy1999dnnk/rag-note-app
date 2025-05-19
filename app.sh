#!/bin/bash

# Define file paths for the relocated Docker Compose files
BACKEND_COMPOSE="./backend/docker-compose.yml"
BACKEND_OVERRIDE="./backend/docker-compose.override.yml"
BACKEND_DEV_COMPOSE="./backend/docker-compose.dev.yml"
FRONTEND_COMPOSE="./frontend/docker-compose.yml"
FRONTEND_OVERRIDE="./frontend/docker-compose.override.yml"

# Display help information
function show_help {
  echo "Task Management App Control Script"
  echo "Usage: $0 {command} [options]"
  echo ""
  echo "Commands:"
  echo "  deploy         Start both frontend and backend in Docker (production mode)"
  echo "  down           Stop all containers"
  echo "  backend        Start only backend services (for local frontend dev)"
  echo "  logs [service] View logs from a specific service (or all if omitted)"
  echo "  build          Rebuild all Docker images"
  echo "  dev            Run backend in Docker and start frontend dev server locally"
  echo "  frontend       Start only frontend container"
  echo ""
  echo "Options:"
  echo "  -d, --detach   Run containers in the background"
}

case "$1" in
  deploy)
    echo "Ensuring Docker network exists..."
    docker network create --driver bridge task-management-network || true

    echo "Stopping any existing containers..."
    docker-compose -f $BACKEND_COMPOSE -f $BACKEND_OVERRIDE -f $FRONTEND_COMPOSE -f $FRONTEND_OVERRIDE down

    echo "Starting backend services first..."
    docker-compose -f $BACKEND_COMPOSE -f $BACKEND_OVERRIDE up -d

    echo "Waiting for backend to initialize (5 seconds)..."
    sleep 5

    echo "Starting frontend services..."
    docker-compose -f $FRONTEND_COMPOSE -f $FRONTEND_OVERRIDE up ${@:2}
    ;;
  down)
    echo "Stopping all containers..."
    docker-compose -f $BACKEND_COMPOSE -f $BACKEND_OVERRIDE -f $FRONTEND_COMPOSE -f $FRONTEND_OVERRIDE down ${@:2}
    ;;
  backend)
    echo "Starting only backend services..."
    docker-compose -f $BACKEND_COMPOSE up ${@:2}
    ;;
  frontend)
    echo "Starting only frontend services..."
    docker-compose -f $FRONTEND_COMPOSE up ${@:2}
    ;;
  logs)
    if [ -z "$2" ]; then
      docker-compose -f $BACKEND_COMPOSE -f $BACKEND_OVERRIDE -f $FRONTEND_COMPOSE -f $FRONTEND_OVERRIDE logs -f
    else
      docker-compose -f $BACKEND_COMPOSE -f $BACKEND_OVERRIDE -f $FRONTEND_COMPOSE -f $FRONTEND_OVERRIDE logs -f "$2"
    fi
    ;;
  build)
    echo "Build is disabled on EC2. Use GitHub Actions to build and push images."
    ;;
  dev)
    echo "Starting backend services in Docker with hot reloading enabled..."
    docker-compose -f $BACKEND_COMPOSE -f $BACKEND_DEV_COMPOSE up -d
    
    echo "Starting frontend development server locally with development env..."
    cd frontend && npm run dev -- --mode development
    ;;
  dev-down)
    echo "Stopping development containers..."
    docker-compose -f $BACKEND_COMPOSE -f $BACKEND_DEV_COMPOSE down
    ;;
  *)
    show_help
    ;;
esac