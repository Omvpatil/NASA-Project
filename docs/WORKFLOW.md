# 🔄 Complete Workflow with SQLite Database

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Application                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐   │
│  │   CSV File   │ ───→ │   SQLite DB  │ ←──→ │  FastAPI API │   │
│  │  (GitHub)    │      │  (tracking)  │      │  (endpoints) │   │
│  └──────────────┘      └──────────────┘      └──────────────┘   │
│                               │                      │          │
│                               ↓                      ↓          │
│                        ┌──────────────┐      ┌──────────────┐   │
│                        │ Load Papers  │ ───→ │  ChromaDB    │   │
│                        │  (scraping)  │      │  (vectors)   │   │
│                        └──────────────┘      └──────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Data Flow:
1. CSV → SQLite (title, link, isLoaded=false)
2. Get unloaded papers from SQLite
3. Scrape paper content from web
4. Create embeddings and store in ChromaDB
5. Mark as loaded in SQLite (isLoaded=true, chunks_created)
```

---

## Complete Workflow Steps

### Step 1: Start the API

```bash
cd /home/om_patil/Desktop/Codes/python/RAG/fastapi_app
./start.fish
```

**What happens:**

-   ✅ API starts on port 8000
-   ✅ SQLite database initialized at `./papers.db`
-   ✅ Embeddings model loaded
-   ✅ Existing ChromaDB loaded (if exists)

---

### Step 2: Load Papers (Automatic CSV Import)

```bash
curl -X POST "http://localhost:8000/load-papers" \
  -H "Content-Type: application/json" \
  -d '{"num_papers": 10}'
```

**What happens:**

1. ✅ CSV file downloaded from GitHub
2. ✅ All papers imported to SQLite (title, link)
3. ✅ First 10 unloaded papers retrieved
4. ✅ Papers scraped from PMC website
5. ✅ Text chunked and embedded
6. ✅ Stored in ChromaDB
7. ✅ Marked as loaded in SQLite

---

### Step 3: Check Database Statistics

```bash
curl http://localhost:8000/database/stats
```

---

### Step 4: Search and Query

```bash
# Search in SQLite database
curl "http://localhost:8000/database/papers/search?query=bone&loaded_only=true"

# Semantic vector search with AI
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does microgravity affect bone density?",
    "num_results": 5,
    "use_llm": true,
    "google_api_key": "YOUR_API_KEY"
  }'
```

---

### Step 5: Append New CSV

```bash
curl -X POST "http://localhost:8000/database/append-csv" \
  -H "Content-Type: application/json" \
  -d '{
    "csv_url": "https://example.com/additional_papers.csv"
  }'
```

---

## See DATABASE.md for complete documentation
