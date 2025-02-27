# IT Visionary Chat Assistant

![It_Visionary_logo](https://github.com/user-attachments/assets/c3080ffe-00c3-4244-8486-cdfdf4bf6d6a)


An AI-powered IT consulting chatbot leveraging FastAPI backend and Streamlit frontend, containerized with Docker for seamless deployment.

## Features

- **AI-Powered Consultancy**: Gemini-based responses for IT infrastructure, cybersecurity, and cloud solutions
- **Session Management**: UUID-based conversation tracking with history preservation
- **Enterprise-Ready**: Containerized microservices architecture
- **Professional Interface**: Branded UI with custom header and message styling

## Prerequisites

- Docker 20.10+
- Docker Compose 2.20+
- Python 3.9+
- Google GenAI API Key

## Installation

```bash
git clone https://github.com/Moaz108/ITVisionary_Chatbot.git
```
## How to use it:





https://github.com/user-attachments/assets/2458c292-73c9-4ca9-b4bd-6d1a4bfd687d






## Configuration

Access:
- Backend Docs: http://localhost:8000/api/docs
- Frontend UI: http://localhost:8501

## Key Architectural Decisions

1- Microservices Design:
- Decoupled frontend/backend
-Independent scaling
-Separate dependency management

2- Network Isolation:
- Custom bridge network
- Service discovery via DNS names

3- Security:
- Environment-based secret management
- CORS middleware configuration
- Containerized execution sandbox

## Technical Challenges & Solutions

### 1. Container Networking
**Challenge**: Frontend service failed to connect to backend using localhost references in Docker environment  
**Solution**:  
- Implemented custom Docker bridge network (`app-network`)  
- Configured service discovery through DNS names (`backend`/`frontend`)  
- Modified connection URLs to use container names instead of localhost

### 2. CORS Configuration
**Challenge**: Browser blocked cross-origin requests between frontend and backend  
**Solution**:  
- Integrated FastAPI CORS middleware  
- Configured permissive policies for development environment:
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_methods=["*"],
      allow_headers=["*"]
  )
  ```
### 3. Asset Embedding
**Challenge**: Streamlit failed to load local images in containerized environment
**Solution**: - Created dedicated /images directory in Docker build process
              - Implemented Dockerfile COPY instruction

## API Endpoints

| Endpoint       | Method | Description                  | Request Body                              | Success Response                          |
|----------------|--------|------------------------------|-------------------------------------------|-------------------------------------------|
| `/api/start`   | POST   | Initialize new chat session  | None                                      | `{"session_id": string, "assistant_response": string}` |
| `/api/chat`    | POST   | Process user message         | `{"session_id": string, "message": string}` | `{"assistant_response": string, "session_id": string}` |

**Base URL**: `http://localhost:8000/api`
## Development:
you can check the Swagger UI , put this URL `http://localhost:8000/docs` in your browser , after the backed files running .


### 4.Docker setup
**Backend Configuration (`Dockerfile.backend`)**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY llm.py .
COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
- Base Image: Official Python 3.9 slim image
- Dependencies: Installs from requirements.txt
- Port Binding: Exposes API on 0.0.0.0:8000

**Frontend Configuration (`Dockerfile.frontend`)**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY llm.py .
COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
- Image Handling: Embeds logo directly in container
- Port Configuration: Exposes Streamlit on 0.0.0.0:8501
  
**Orchestration (`docker-compose.yml`)**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    networks:
      - app-network

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      - BACKEND_URL=http://backend:8000
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```
- Network Isolation: Dedicated bridge network for secure communication
- Service Discovery: Frontend accesses backend via DNS name `backend`
- Port Mapping:
  - Backend: 8000 → 8000
  - Frontend: 8501 → 8501


**Build & Run**
```bash
docker-compose up --build -d

# View logs
docker-compose logs -f
```
