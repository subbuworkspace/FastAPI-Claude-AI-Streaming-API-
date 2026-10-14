# FastAPI + Claude AI Streaming API 🚀

A beginner-friendly Python project demonstrating **FastAPI, REST APIs, Pydantic validation, CRUD operations, JSON data handling, and Claude AI streaming** using Server-Sent Events (SSE).

This project is designed to strengthen practical API development skills, understand how FastAPI works internally, and prepare for Python, backend development, and Generative AI interviews.

## 🎯 Project Objectives

- Understand FastAPI fundamentals and REST API development.
- Create endpoints using GET, POST, PUT, and DELETE.
- Validate request data using Pydantic.
- Read and update JSON-based records.
- Handle HTTP errors and status codes.
- Generate interactive API documentation using Swagger UI.
- Connect Claude AI using the Anthropic Python SDK.
- Stream LLM responses using Server-Sent Events.
- Manage API keys securely with environment variables.
- Practise API testing with Pytest.

## 🛠️ Technologies Used

- Python
- FastAPI
- Uvicorn
- Pydantic
- Anthropic Python SDK
- Python Dotenv
- JSON
- Pytest
- Git and GitHub

## 📁 Project Structure

```text
FastAPI-Claude-Streaming-Starter/
│
├── main.py                 # FastAPI application
├── patients.json           # Sample JSON records
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Ignore secrets and environments
├── tests/
│   └── test_main.py        # Automated API tests
├── LINKEDIN_POST.txt       # LinkedIn caption
└── README.md               # Project documentation
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/FastAPI-Claude-Streaming-Starter.git

cd FastAPI-Claude-Streaming-Starter
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv myenv
```

Activate it on Windows Git Bash:

```bash
source myenv/Scripts/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and configure your Anthropic API key:

```dotenv
ANTHROPIC_API_KEY=your_actual_api_key
ANTHROPIC_MODEL=claude-sonnet-4-20250514
```

Use a model ID available to your Anthropic account. Never upload your real `.env` file to GitHub.

### 5. Start the FastAPI server

```bash
python -m uvicorn main:app --reload
```

Open the following URLs:

- API root: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/patients` | Retrieve all sample records |
| GET | `/patients/{patient_id}` | Retrieve one record |
| POST | `/patients` | Create a record |
| PUT | `/patients/{patient_id}` | Update a record |
| DELETE | `/patients/{patient_id}` | Delete a record |
| POST | `/chatbot/stream` | Stream Claude AI responses |

## 🧪 Example API Request

### Create a record

Send a POST request to `/patients` using Swagger UI.

```json
{
  "id": 3,
  "name": "Taylor Example",
  "age": 29,
  "condition": "Sample condition C"
}
```

Expected status code: `201 Created`.

### Retrieve a record

```http
GET /patients/1
```

### Delete a record

```http
DELETE /patients/1
```

## 🤖 Claude AI Integration

The optional Claude endpoint accepts a prompt and streams the generated response.

Example request:

```json
{
  "message": "Explain FastAPI in simple terms.",
  "max_tokens": 200
}
```

Endpoint:

```http
POST /chatbot/stream
```

The implementation uses the Anthropic SDK to call Claude and FastAPI's `StreamingResponse` to send Server-Sent Events.

### How it works

```text
Client / Swagger UI
        |
        v
FastAPI Endpoint
        |
        v
Pydantic Validation
        |
        v
Anthropic Python SDK
        |
        v
Claude LLM
        |
        v
StreamingResponse
        |
        v
Text Chunks via SSE
```

**Note:** Claude API access requires a valid API key, an available model, and sufficient account access or credits. The CRUD endpoints work without Claude credentials.

## 🧠 Important FastAPI Concepts

### 1. FastAPI

A Python framework for building APIs with type hints, automatic validation integration, and generated OpenAPI documentation.

### 2. Uvicorn

An ASGI server that runs the FastAPI application.

```bash
python -m uvicorn main:app --reload
```

Here, `main` refers to `main.py`, while `app` refers to the FastAPI instance.

### 3. Pydantic

Used to validate and parse request data based on Python model declarations.

```python
from pydantic import BaseModel, Field

class Patient(BaseModel):
    id: int = Field(gt=0)
    name: str
    age: int = Field(ge=0, le=120)
    condition: str
```

### 4. HTTP Methods

- GET: Retrieve data.
- POST: Create data.
- PUT: Replace or update a resource.
- PATCH: Partially update a resource.
- DELETE: Remove a resource.

### 5. HTTP Status Codes

- `200`: Successful request.
- `201`: Resource created.
- `204`: Successful request with no response body.
- `400`: Bad request.
- `401`: Authentication required or invalid.
- `403`: Forbidden.
- `404`: Resource not found.
- `409`: Conflict.
- `422`: Request validation failed.
- `500`: Internal server error.

### 6. Environment Variables

Store API keys and configuration outside the source code. Use `python-dotenv` to load local `.env` settings and `.gitignore` to keep secrets out of version control.

### 7. StreamingResponse

Sends data progressively rather than waiting for the complete response. In this project, it supports Claude text streaming through SSE.

### 8. Async Programming

FastAPI supports both `def` and `async def` endpoints. Use asynchronous I/O when working with async-compatible libraries, and avoid blocking operations inside asynchronous handlers.

## 🎤 FastAPI Interview Questions

**Q1. What is FastAPI?**

FastAPI is a modern Python framework for building APIs, featuring type-driven validation and automatic API documentation.

**Q2. What is the difference between FastAPI and Flask?**

FastAPI provides integrated request validation and OpenAPI documentation. Flask is a lightweight framework offering a flexible, minimal core.

**Q3. What is ASGI?**

ASGI stands for Asynchronous Server Gateway Interface. It defines how asynchronous Python web applications communicate with servers.

**Q4. Why do we use Uvicorn?**

Uvicorn runs ASGI applications such as FastAPI and handles incoming HTTP requests.

**Q5. What is Pydantic?**

Pydantic validates and parses structured data using Python type annotations and model definitions.

**Q6. What is dependency injection?**

It allows reusable dependencies, such as database sessions and authentication logic, to be provided to endpoints using FastAPI's `Depends`.

**Q7. What is the difference between path and query parameters?**

A path parameter identifies a resource, such as `/patients/10`. A query parameter filters or modifies a request, such as `/patients?limit=10`.

**Q8. What is the difference between PUT and PATCH?**

PUT typically replaces a resource, while PATCH applies a partial update.

**Q9. How does FastAPI generate Swagger documentation?**

FastAPI generates an OpenAPI schema from routes, type hints, and Pydantic models. Swagger UI uses this schema to provide interactive documentation.

**Q10. How do you handle exceptions?**

Raise `HTTPException` with an appropriate status code and detail message, and use exception handlers for consistent error responses.

**Q11. What is middleware?**

Middleware executes around request and response processing, supporting features such as CORS, timing, and request logging.

**Q12. How do you test FastAPI applications?**

Use Pytest with FastAPI's `TestClient` to send requests and verify response codes and payloads.

**Q13. What is CORS?**

Cross-Origin Resource Sharing is a browser mechanism that controls which origins can access an API from frontend code.

**Q14. What is the difference between authentication and authorization?**

Authentication verifies identity; authorization determines permissions.

**Q15. What is SSE?**

Server-Sent Events is a mechanism for sending a stream of events from a server to a client over HTTP.

**Q16. Why might Uvicorn report `Attribute "app" not found`?**

The module or variable name may be incorrect, the Python file may be empty, or it may not contain `app = FastAPI()`.

**Q17. Why use `.env`?**

It separates configuration and secrets from application source code. The real `.env` should not be committed to Git.

**Q18. What is CRUD?**

CRUD means Create, Read, Update, and Delete—the fundamental operations used to manage resources.

**Q19. How would you improve this project for production?**

Add database persistence, authentication, authorization, rate limiting, structured logging, monitoring, secure secret management, and comprehensive tests.

**Q20. How can you deploy FastAPI?**

Package the application with its dependencies, configure a production ASGI server, provide environment variables securely, and deploy behind HTTPS with monitoring and suitable resource limits.

## 🧪 Run Automated Tests

Execute:

```bash
python -m pytest -q
```

The tests cover basic endpoints, patient retrieval, missing records, and input validation.

## 🔒 Security and Limitations

- Use only synthetic records in this demonstration.
- Do not expose real patient information through public endpoints.
- Never commit API keys or `.env` files.
- Add authentication and authorization before exposing sensitive data.
- JSON-file storage is intended for learning; use a database for production.
- Configure rate limits and request-size restrictions for LLM endpoints.
- Handle provider errors and logging carefully without leaking secrets.

## 🚀 Future Enhancements

- Integrate PostgreSQL or another production database.
- Add JWT-based authentication and role-based access.
- Implement pagination, filtering, and sorting.
- Build a chat frontend for streaming Claude responses.
- Add Docker and GitHub Actions.
- Deploy to a cloud platform.
- Add monitoring, structured logs, and more integration tests.

## 📚 Official References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Anthropic Python SDK](https://platform.claude.com/docs/en/api/sdks/python)
- [Claude Streaming Documentation](https://platform.claude.com/docs/en/build-with-claude/streaming)

## 👨‍💻 Author

**Subrata Mondal**

Data Analytics | Python | Machine Learning | Generative AI

*Keep Learning. Keep Building. 🚀*
