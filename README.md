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




https://github.com/user-attachments/assets/0ca23260-6d31-4563-8d34-60bcd4192e9a




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
