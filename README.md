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
- `POST /reports/generate-template` - Generate AI-powered template report
- `GET /reports/languages` - Get supported languages for templates

## Environment Variables

- `PYTHONPATH` - Python path (set to `/app` in container)
- `PYTHONUNBUFFERED` - Disable Python output buffering
- `GEMINI_API_KEY` - Google Gemini API key for AI-powered report generation
- `GOOGLE_APPLICATION_CREDENTIALS` - Path to Google Cloud service account credentials (optional)
- `OLLAMA_HOST` - Ollama host (default: host.docker.internal for Docker)
- `OLLAMA_PORT` - Ollama port (default: 11434)

## AI Setup

This application supports multiple AI providers for enhanced report generation:

### Option 1: Google Generative AI (Gemini) - Recommended

1. **Get a Gemini API Key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Set the environment variable: `export GEMINI_API_KEY=your_api_key_here`

2. **For Docker:**
   ```bash
   # Set the API key when running docker-compose
   GEMINI_API_KEY=your_api_key_here docker-compose up
   
   # Or create a .env file with your API key
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   docker-compose up
   ```

3. **For Local Development:**
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   python app.py
   ```

### Option 2: Ollama (Local AI)

If you don't have a Gemini API key, the application will automatically fallback to Ollama:

1. **Install Ollama:**
   ```bash
   # macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Or download from https://ollama.ai/download
   ```

2. **Start Ollama and pull a model:**
   ```bash
   ollama serve
   ollama pull llama3.2
   ```

3. **Run the application:**
   ```bash
   # Docker will automatically connect to Ollama
   docker-compose up
   
   # Or run locally
   python app.py
   ```

### AI Provider Priority

The application will use AI providers in this order:
1. Google Generative AI (if API key is provided)
2. Ollama (if available and Gemini is not)
3. Fallback mode (no AI features)

## Template-Based Report Generation

The application supports AI-powered report generation using customizable templates in multiple languages:

### Supported Languages
- **English (en)** - Default language with business plan templates
- **Kannada (kn)** - ಕನ್ನಡ language support with localized templates

### Template Structure
Each language has its own template directory:
- `templates_en/` - English templates
- `templates_kn/` - Kannada templates

Each directory contains:
- `system_prompt.jinja` - AI system instructions
- `user_prompt.jinja` - Report structure and formatting
- `user_form.jinja` - Data input template

### Using Template Reports

**API Endpoint:**
```bash
POST /reports/generate-template
```

**Request Body:**
```json
{
  "project_data": {
    "field1": "Project Name",
    "field2": "Project Type",
    "field3": "Location",
    "field4": "Duration",
    "field5": "Promoter Name",
    "field6": "Experience",
    "field7": "Background",
    "field8": "Market Size",
    "field9": "Production Cost",
    "field10": "Selling Price",
    "field11": "Profit Percentage",
    "field12": "Project Objective",
    "field13": "Unique Selling Proposition",
    "field14": "Key Challenges",
    "field15": "Key Opportunities",
    "format": "business_plan",
    "language": "en"
  },
  "language": "en"
}
```

**Response:**
```json
{
  "report_id": "template_report_20241201_143022_en",
  "generated_at": "2024-12-01T14:30:22",
  "language": "en",
  "report": "Generated AI report content...",
  "status": "success"
}
```

### Testing Templates

Run the test script to verify template functionality:
```bash
uv run python test_templates.py
```

## Health Checks

The application includes health checks that verify the API is responding correctly. The health check endpoint is available at `/health`. 