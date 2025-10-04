# 🚀 NASA Space Biology Knowledge Engine - FastAPI

A RESTful API for searching and querying NASA space biology research papers using RAG (Retrieval Augmented Generation).

## Features

-   ✅ **Vector Search**: Semantic search using ChromaDB and HuggingFace embeddings
-   ✅ **AI-Powered Answers**: LLM-generated responses with citations (Google Gemini)
-   ✅ **Persistent Storage**: Papers stored locally with ChromaDB
-   ✅ **SQLite Tracking**: Track paper loading status and progress
-   ✅ **Resume Capability**: Resume interrupted loading sessions
-   ✅ **Keyword Filtering**: Filter results by paper title keywords
-   ✅ **CSV Append**: Add new papers from multiple CSV files
-   ✅ **RESTful API**: Easy integration with any client
-   ✅ **Auto-docs**: Swagger UI and ReDoc available

## Installation

### 1. Create Virtual Environment (UV)

```fish
# Navigate to fastapi_app directory
cd /home/om_patil/Desktop/Codes/python/RAG/fastapi_app

# Create UV virtual environment
uv venv

# Activate (fish shell)
source .venv/bin/activate.fish
```

### 2. Install Dependencies

```fish
# Using UV pip
uv pip install -r requirements.txt

# Or regular pip
pip install -r requirements.txt
```

## Running the API

### Start the server:

```fish
# Development mode (auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:

-   **API**: http://localhost:8000
-   **Swagger UI**: http://localhost:8000/docs
-   **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 📊 Status & Info

#### `GET /` - Root endpoint

```bash
curl http://localhost:8000/
```

#### `GET /health` - Health check

```bash
curl http://localhost:8000/health
```

#### `GET /database-status` - Database status

```bash
curl http://localhost:8000/database-status
```

#### `GET /papers` - List all papers

```bash
curl http://localhost:8000/papers
```

#### `GET /models` - List available LLM models

```bash
curl http://localhost:8000/models
```

---

### 🔍 Search

#### `POST /search` - Search papers with optional AI answer

**Request:**

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does microgravity affect bone density?",
    "num_results": 10,
    "use_llm": true,
    "google_api_key": "YOUR_GOOGLE_API_KEY",
    "model_name": "gemini-2.5-flash",
    "search_method": "similarity",
    "use_keyword_filter": false
  }'
```

**Request with Keyword Filter:**

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "space mission bone loss",
    "num_results": 5,
    "use_llm": true,
    "google_api_key": "YOUR_API_KEY",
    "use_keyword_filter": true,
    "keyword_filter": "Bion, mission"
  }'
```

**Response:**

```json
{
    "answer": "According to research papers...",
    "source_documents": [
        {
            "page_content": "...",
            "metadata": {
                "title": "Mice in Bion-M 1 space mission...",
                "pmcid": "PMC7876543",
                "source": "https://..."
            }
        }
    ],
    "query": "...",
    "num_results": 5,
    "timestamp": "2025-10-03T..."
}
```

**Parameters:**

-   `query` (required): Search query or question
-   `num_results` (optional, default: 10): Number of results (1-50)
-   `use_llm` (optional, default: true): Generate AI answer
-   `google_api_key` (optional): Google API key for Gemini
-   `model_name` (optional, default: "gemini-2.5-flash"): LLM model
-   `search_method` (optional, default: "similarity"): similarity, mmr, or similarity_score
-   `use_keyword_filter` (optional, default: false): Enable keyword filtering
-   `keyword_filter` (optional): Comma-separated keywords

---

### 📥 Load Papers

#### `POST /load-papers` - Load papers from CSV

**Request:**

```bash
curl -X POST "http://localhost:8000/load-papers" \
  -H "Content-Type: application/json" \
  -d '{
    "num_papers": 10
  }'
```

**Response:**

```json
{
    "status": "success",
    "papers_loaded": 10,
    "chunks_created": 50,
    "message": "Successfully loaded 10 papers and created 50 chunks"
}
```

**Note:** This process takes time (1-2 minutes per paper). For production, consider running this in the background.

---

### 🔄 Reset

#### `POST /reset-database` - Reset database

```bash
curl -X POST "http://localhost:8000/reset-database"
```

---

## Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Check health
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# 2. Search without LLM
response = requests.post(
    f"{BASE_URL}/search",
    json={
        "query": "How does microgravity affect bones?",
        "num_results": 5,
        "use_llm": False
    }
)
results = response.json()
print(f"Found {results['num_results']} papers")

# 3. Search with LLM
response = requests.post(
    f"{BASE_URL}/search",
    json={
        "query": "What are the effects of radiation on astronauts?",
        "num_results": 5,
        "use_llm": True,
        "google_api_key": "YOUR_API_KEY",
        "model_name": "gemini-2.5-flash"
    }
)
results = response.json()
print(f"AI Answer: {results['answer']}")

# 4. Load papers (if database empty)
response = requests.post(
    f"{BASE_URL}/load-papers",
    json={"num_papers": 10}
)
print(response.json())
```

---

## JavaScript/TypeScript Client Example

```typescript
// Using fetch API
const searchPapers = async () => {
    const response = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            query: "How does microgravity affect bone density?",
            num_results: 10,
            use_llm: true,
            google_api_key: "YOUR_API_KEY",
            model_name: "gemini-2.5-flash",
        }),
    });

    const data = await response.json();
    console.log("Answer:", data.answer);
    console.log("Sources:", data.source_documents);
};

searchPapers();
```

---

## Environment Variables

Create a `.env` file (optional):

```env
GOOGLE_API_KEY=your_google_api_key_here
PERSIST_DIRECTORY=./chroma_db
COLLECTION_NAME=space_biology_papers
```

Update code to use:

```python
from dotenv import load_dotenv
load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
```

---

## Directory Structure

```
fastapi_app/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .env                # Environment variables (create this)
└── chroma_db/          # Vector database (auto-created)
    └── ...
```

---

## Testing with curl

### 1. Basic Search (No LLM)

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "bone loss", "num_results": 3, "use_llm": false}'
```

### 2. Search with AI Answer

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What causes bone loss in space?",
    "use_llm": true,
    "google_api_key": "YOUR_KEY"
  }'
```

### 3. Load Papers

```bash
curl -X POST "http://localhost:8000/load-papers" \
  -H "Content-Type: application/json" \
  -d '{"num_papers": 5}'
```

---

## API Response Codes

| Code | Meaning                            |
| ---- | ---------------------------------- |
| 200  | Success                            |
| 404  | Database not loaded / Not found    |
| 422  | Validation error (invalid request) |
| 500  | Internal server error              |

---

## Comparison: Streamlit vs FastAPI

| Feature         | Streamlit App           | FastAPI App                  |
| --------------- | ----------------------- | ---------------------------- |
| **UI**          | Web interface           | REST API                     |
| **Use Case**    | Interactive exploration | Integration/Automation       |
| **Client**      | Browser                 | Any (Python, JS, curl, etc.) |
| **Deployment**  | Single app              | Microservice                 |
| **State**       | Session-based           | Stateless (DB persists)      |
| **Scalability** | Limited                 | High (multi-worker)          |

---

## Production Deployment

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t nasa-rag-api .
docker run -p 8000:8000 nasa-rag-api
```

### Using systemd (Linux)

Create `/etc/systemd/system/nasa-rag.service`:

```ini
[Unit]
Description=NASA RAG API
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/fastapi_app
ExecStart=/path/to/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:

```bash
sudo systemctl start nasa-rag
sudo systemctl enable nasa-rag
```

---

## Troubleshooting

### Database not loading

-   Check if `chroma_db/` directory exists
-   Run `/load-papers` endpoint to create database
-   Check file permissions

### Slow searches

-   Reduce `num_results`
-   Use `similarity` instead of `mmr`
-   Disable LLM with `use_llm: false`

### API key errors

-   Get free API key: https://aistudio.google.com/apikey
-   Pass in request body: `"google_api_key": "YOUR_KEY"`

---
