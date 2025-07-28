# MJ LangGraph Project Report API

A FastAPI-based API for generating various project reports.

## Features

- Generate summary, financial, performance, and detailed reports
- Support for JSON and CSV output formats
- Health check endpoint
- Project management functionality

## Docker Setup

### Prerequisites

- Docker
- Docker Compose

### Quick Start

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access the API:**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Root Endpoint: http://localhost:8000/

### Development

For development with hot reload, you can uncomment the volume mount in `docker-compose.yml`:

```yaml
volumes:
  - .:/app  # Uncomment this line
```

### Production

For production deployment, consider:

1. Using the commented nginx service in `docker-compose.yml`
2. Setting up proper environment variables
3. Using a production WSGI server like gunicorn

### Docker Commands

```bash
# Build the image
docker build -t mj-langgraph .

# Run the container
docker run -p 8000:8000 mj-langgraph

# Run with docker-compose
docker-compose up

# Run in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f app
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /projects` - List all projects
- `GET /projects/{project_id}` - Get specific project
- `POST /reports/generate` - Generate a report
- `GET /reports/download` - Download a report
- `GET /reports/types` - Get available report types

## Environment Variables

- `PYTHONPATH` - Python path (set to `/app` in container)
- `PYTHONUNBUFFERED` - Disable Python output buffering

## Health Checks

The application includes health checks that verify the API is responding correctly. The health check endpoint is available at `/health`. 