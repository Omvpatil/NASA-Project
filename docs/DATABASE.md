# 📊 SQLite Database Management

## Overview

The FastAPI application now includes a **SQLite database** for tracking paper loading status. This allows you to:

-   ✅ Track which papers have been loaded
-   ✅ See loading progress and statistics
-   ✅ Append new CSV files without duplicates
-   ✅ Query paper status before scraping
-   ✅ Resume interrupted loading sessions

---

## Database Schema

### `papers` Table

| Column           | Type      | Description                                   |
| ---------------- | --------- | --------------------------------------------- |
| `id`             | INTEGER   | Primary key (auto-increment)                  |
| `title`          | TEXT      | Paper title from CSV                          |
| `link`           | TEXT      | Paper URL (unique)                            |
| `pmcid`          | TEXT      | PubMed Central ID (extracted from link)       |
| `isLoaded`       | BOOLEAN   | `TRUE` if paper has been scraped and loaded   |
| `isAbstracted`   | BOOLEAN   | `TRUE` if paper abstract has been extracted   |
| `loaded_at`      | TIMESTAMP | When the paper was loaded                     |
| `chunks_created` | INTEGER   | Number of text chunks created from this paper |
| `created_at`     | TIMESTAMP | When record was created                       |
| `updated_at`     | TIMESTAMP | Last update time                              |

**Indexes:**

-   `idx_link` - Fast lookup by link
-   `idx_isLoaded` - Fast filtering by loading status

---

## API Endpoints

### 1. Get Database Statistics

**GET** `/database/stats`

Get overall database statistics including loading progress.

**Response:**

```json
{
    "total_papers": 156,
    "loaded_papers": 45,
    "unloaded_papers": 111,
    "total_chunks": 234,
    "avg_chunks_per_paper": 5.2,
    "loading_progress": 28.85
}
```

**cURL:**

```bash
curl http://localhost:8000/database/stats
```

---

### 2. Get Loaded Papers

**GET** `/database/papers/loaded?limit=10`

Get papers that have been successfully loaded.

**Parameters:**

-   `limit` (optional): Maximum number of results

**Response:**

```json
{
    "count": 3,
    "papers": [
        {
            "id": 1,
            "title": "Microgravity induces pelvic bone loss through osteoclastic activity",
            "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/",
            "pmcid": "PMC8234567",
            "loaded_at": "2025-10-03T20:15:30.123456",
            "chunks_created": 5
        }
    ]
}
```

**cURL:**

```bash
curl "http://localhost:8000/database/papers/loaded?limit=10"
```

**Python:**

```python
import requests

response = requests.get("http://localhost:8000/database/papers/loaded", params={"limit": 10})
papers = response.json()["papers"]
print(f"Loaded {len(papers)} papers")
```

---

### 3. Get Unloaded Papers

**GET** `/database/papers/unloaded?limit=5`

Get papers that haven't been loaded yet (available for scraping).

**Parameters:**

-   `limit` (optional): Maximum number of results

**Response:**

```json
{
    "count": 5,
    "papers": [
        {
            "id": 46,
            "title": "Effects of spaceflight on muscle atrophy",
            "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9876543/",
            "pmcid": "PMC9876543",
            "created_at": "2025-10-03T19:00:00.000000"
        }
    ]
}
```

**cURL:**

```bash
curl "http://localhost:8000/database/papers/unloaded?limit=5"
```

---

### 4. Get All Papers

**GET** `/database/papers/all`

Get all papers with their loading status.

**Response:**

```json
{
    "count": 156,
    "papers": [
        {
            "id": 1,
            "title": "Microgravity induces pelvic bone loss...",
            "link": "https://...",
            "pmcid": "PMC8234567",
            "isLoaded": true,
            "loaded_at": "2025-10-03T20:15:30",
            "chunks_created": 5,
            "created_at": "2025-10-03T19:00:00"
        },
        {
            "id": 2,
            "title": "Effects of spaceflight...",
            "link": "https://...",
            "pmcid": "PMC9876543",
            "isLoaded": false,
            "loaded_at": null,
            "chunks_created": 0,
            "created_at": "2025-10-03T19:00:00"
        }
    ]
}
```

**cURL:**

```bash
curl http://localhost:8000/database/papers/all
```

---

### 5. Search Papers in Database

**GET** `/database/papers/search?query=bone&loaded_only=false`

Search papers by title in the tracking database.

**Parameters:**

-   `query` (required): Search text
-   `loaded_only` (optional): Only return loaded papers

**Response:**

```json
{
    "query": "bone",
    "count": 12,
    "papers": [
        {
            "id": 1,
            "title": "Microgravity induces pelvic bone loss...",
            "link": "https://...",
            "pmcid": "PMC8234567",
            "isLoaded": true,
            "loaded_at": "2025-10-03T20:15:30",
            "chunks_created": 5
        }
    ]
}
```

**cURL:**

```bash
curl "http://localhost:8000/database/papers/search?query=bone&loaded_only=false"
```

**Python:**

```python
response = requests.get(
    "http://localhost:8000/database/papers/search",
    params={"query": "bone", "loaded_only": True}
)
results = response.json()
print(f"Found {results['count']} papers about bone")
```

---

### 6. Append CSV to Database

**POST** `/database/append-csv`

Add papers from a new CSV file to the database (duplicates are automatically ignored).

**Request:**

```json
{
    "csv_url": "https://example.com/new_papers.csv"
}
```

**Response:**

```json
{
    "status": "success",
    "message": "CSV appended successfully",
    "stats": {
        "total": 50,
        "added": 35,
        "duplicates": 15,
        "errors": 0
    }
}
```

**cURL:**

```bash
curl -X POST "http://localhost:8000/database/append-csv" \
  -H "Content-Type: application/json" \
  -d '{
    "csv_url": "https://raw.githubusercontent.com/user/repo/main/new_papers.csv"
  }'
```

**Python:**

```python
response = requests.post(
    "http://localhost:8000/database/append-csv",
    json={"csv_url": "https://example.com/new_papers.csv"}
)
print(response.json())
```

---

### 7. Get Non-Abstracted Papers

**GET** `/database/papers/non-abstracted?limit=5`

Get papers that haven't had their abstracts extracted yet.

**Parameters:**

-   `limit` (optional): Maximum number of results

**Response:**

```json
{
    "count": 5,
    "papers": [
        {
            "id": 50,
            "title": "Radiation effects on cellular function",
            "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9999999/",
            "pmcid": "PMC9999999",
            "created_at": "2025-10-03T19:00:00.000000"
        }
    ]
}
```

**cURL:**

```bash
curl "http://localhost:8000/database/papers/non-abstracted?limit=5"
```

**Use case:** Get papers for abstract extraction workflow

---

## Workflow Examples

### 1. Initial Setup

```bash
# 1. Start the API
./start.fish

# 2. CSV is automatically loaded into SQLite on first /load-papers call
curl -X POST "http://localhost:8000/load-papers" \
  -H "Content-Type: application/json" \
  -d '{"num_papers": 10}'

# 3. Check statistics
curl http://localhost:8000/database/stats
```

---

### 2. Resume Interrupted Loading

```bash
# 1. Check how many papers are unloaded
curl http://localhost:8000/database/stats

# 2. Get list of unloaded papers
curl "http://localhost:8000/database/papers/unloaded?limit=5"

# 3. Load next batch
curl -X POST "http://localhost:8000/load-papers" \
  -H "Content-Type: application/json" \
  -d '{"num_papers": 10}'
```

---

### 3. Append New Papers from CSV

```bash
# 1. Upload new CSV file to GitHub or server
# 2. Append to database
curl -X POST "http://localhost:8000/database/append-csv" \
  -H "Content-Type: application/json" \
  -d '{
    "csv_url": "https://example.com/additional_papers.csv"
  }'

# 3. Load new papers
curl -X POST "http://localhost:8000/load-papers" \
  -H "Content-Type: application/json" \
  -d '{"num_papers": 20}'
```

---

### 4. Track Loading Progress

```python
import requests
import time

BASE_URL = "http://localhost:8000"

def track_loading_progress():
    """Monitor loading progress"""
    while True:
        # Get stats
        stats = requests.get(f"{BASE_URL}/database/stats").json()

        print(f"\n📊 Loading Progress: {stats['loading_progress']}%")
        print(f"   Loaded: {stats['loaded_papers']}/{stats['total_papers']}")
        print(f"   Chunks: {stats['total_chunks']}")
        print(f"   Avg chunks/paper: {stats['avg_chunks_per_paper']}")

        if stats['loading_progress'] >= 100:
            print("✅ All papers loaded!")
            break

        # Load next batch
        print("\n🔄 Loading next 10 papers...")
        result = requests.post(
            f"{BASE_URL}/load-papers",
            json={"num_papers": 10}
        ).json()

        print(f"   Loaded: {result['papers_loaded']} papers")
        print(f"   Created: {result['chunks_created']} chunks")

        time.sleep(2)  # Brief pause

# Run
track_loading_progress()
```

---

### 5. Search Before Loading

```python
import requests

BASE_URL = "http://localhost:8000"

def check_paper_status(search_term: str):
    """Check if papers about a topic are loaded"""

    # Search in database
    response = requests.get(
        f"{BASE_URL}/database/papers/search",
        params={"query": search_term}
    )

    results = response.json()
    loaded = [p for p in results["papers"] if p["isLoaded"]]
    unloaded = [p for p in results["papers"] if not p["isLoaded"]]

    print(f"📚 Papers about '{search_term}':")
    print(f"   ✅ Loaded: {len(loaded)}")
    print(f"   ⏳ Not loaded: {len(unloaded)}")

    if unloaded:
        print(f"\n   Next papers to load:")
        for p in unloaded[:3]:
            print(f"   - {p['title'][:60]}...")

# Check status
check_paper_status("bone loss")
check_paper_status("radiation")
```

---

## Database Files

-   **SQLite Database**: `./papers.db` (in `fastapi_app/` directory)
-   **Vector Store**: `./chroma_db/` (ChromaDB)

Both are created automatically on first use.

---

## Database Manager Python Class

### Direct Usage

```python
from database_manager import PaperDatabaseManager

# Initialize
db = PaperDatabaseManager("./papers.db")

# Load CSV
stats = db.load_csv("https://example.com/papers.csv")
print(f"Added {stats['added']} papers")

# Get unloaded papers
papers = db.get_unloaded_papers(limit=10)
for paper in papers:
    print(f"- {paper['title']}")

# Mark as loaded
db.mark_as_loaded(paper['link'], chunks_created=5)

# Mark as abstracted (for abstract extraction workflow)
db.mark_as_abstracted(paper['link'])

# Get non-abstracted papers
non_abstracted = db.get_nonAbstracted_papers(limit=10)
for paper in non_abstracted:
    print(f"- {paper['title']}")

# Get statistics
stats = db.get_stats()
print(f"Progress: {stats['loading_progress']}%")

# Close connection
db.close()
```

---

## Benefits

### 1. **Resume Capability**

-   API restart doesn't lose track of loaded papers
-   Can stop and resume loading at any time
-   Progress persists across sessions

### 2. **Duplicate Prevention**

-   Same CSV can be loaded multiple times safely
-   Unique constraint on `link` prevents duplicates
-   `append-csv` ignores existing papers

### 3. **Progress Tracking**

-   Real-time statistics on loading progress
-   Know exactly which papers are loaded
-   Track chunks per paper for optimization

### 4. **Query Before Load**

-   Search database to see what's available
-   Check if specific papers are loaded
-   Prioritize loading based on needs

### 5. **Multi-CSV Support**

-   Append multiple CSV files
-   Merge different paper sources
-   Build comprehensive database incrementally

### 6. **Abstract Extraction Tracking**

-   Track which papers have abstracts extracted
-   Separate workflow for abstract-only processing
-   Useful for lightweight indexing before full loading

---

## Two-Stage Loading Workflow

The database supports a **two-stage loading approach**:

### Stage 1: Abstract Extraction (Lightweight)

```python
# Get papers without abstracts
non_abstracted = db.get_nonAbstracted_papers(limit=20)

# Extract and store abstracts (faster, less data)
for paper in non_abstracted:
    abstract = scrape_article_abstract(paper['link'])
    # Store abstract in separate vector store
    db.mark_as_abstracted(paper['link'])
```

### Stage 2: Full Paper Loading (Complete)

```python
# Get unloaded papers
unloaded = db.get_unloaded_papers(limit=10)

# Scrape full content and create embeddings
for paper in unloaded:
    full_text = scrape_article_text(paper['link'])
    # Create chunks and embeddings
    db.mark_as_loaded(paper['link'], chunks_created=5)
```

**Benefits:**

-   ✅ Quick initial indexing with abstracts
-   ✅ Full loading on-demand for relevant papers
-   ✅ Reduced bandwidth and storage initially
-   ✅ Faster initial search capability

---

## Database Management Commands

### View Database

```bash
# Install SQLite CLI (if needed)
sudo apt-get install sqlite3

# Open database
sqlite3 papers.db

# View papers
SELECT * FROM papers LIMIT 10;

# Count loaded papers
SELECT COUNT(*) FROM papers WHERE isLoaded = 1;

# Count abstracted papers
SELECT COUNT(*) FROM papers WHERE isAbstracted = 1;

# See loading statistics
SELECT
    COUNT(*) as total,
    SUM(CASE WHEN isLoaded = 1 THEN 1 ELSE 0 END) as loaded,
    SUM(CASE WHEN isAbstracted = 1 THEN 1 ELSE 0 END) as abstracted,
    SUM(chunks_created) as total_chunks
FROM papers;

# Exit
.quit
```

### Backup Database

```bash
# Backup SQLite database
cp papers.db papers_backup_$(date +%Y%m%d).db

# Backup ChromaDB
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz chroma_db/
```

### Reset Everything

```bash
# Via API
curl -X POST http://localhost:8000/reset-database

# Or manually delete files
rm papers.db
rm -rf chroma_db/
```

---

## CSV File Requirements

Your CSV file must have these columns:

-   **Title** (required): Paper title
-   **Link** (required): Paper URL

Optional columns are ignored.

**Example CSV:**

```csv
Title,Link
"Microgravity induces bone loss","https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/"
"Effects of spaceflight on muscle","https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9876543/"
```

---

## Troubleshooting

### Database Not Found

```bash
# Check if file exists
ls -la papers.db

# If missing, will be created automatically on startup
./start.fish
```

### Papers Not Marked as Loaded

Check logs when calling `/load-papers`:

```
✅ Scraped successfully
📊 Marked as loaded: Paper title... (5 chunks)
```

If not seeing this, check database manager initialization.

### Duplicate Papers

The database prevents duplicates automatically:

-   Unique constraint on `link` column
-   `INSERT OR IGNORE` used for safety
-   Duplicate count returned in stats

---

## Integration Example

### Complete Workflow with Database

```python
import requests
import time

BASE_URL = "http://localhost:8000"

def complete_workflow():
    # 1. Append new CSV
    print("📥 Appending CSV...")
    response = requests.post(
        f"{BASE_URL}/database/append-csv",
        json={"csv_url": "https://example.com/papers.csv"}
    )
    stats = response.json()["stats"]
    print(f"   Added: {stats['added']}, Duplicates: {stats['duplicates']}")

    # 2. Check database stats
    print("\n📊 Database Stats:")
    stats = requests.get(f"{BASE_URL}/database/stats").json()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    # 3. Load papers
    print("\n🔄 Loading papers...")
    response = requests.post(
        f"{BASE_URL}/load-papers",
        json={"num_papers": 10}
    )
    result = response.json()
    print(f"   Loaded: {result['papers_loaded']} papers")

    # 4. Search loaded papers
    print("\n🔍 Searching loaded papers...")
    response = requests.get(
        f"{BASE_URL}/database/papers/search",
        params={"query": "bone", "loaded_only": True}
    )
    results = response.json()
    print(f"   Found {results['count']} papers about bone")

    # 5. Query vector database
    print("\n🤖 Querying with AI...")
    response = requests.post(
        f"{BASE_URL}/search",
        json={
            "query": "How does microgravity affect bones?",
            "num_results": 5,
            "use_llm": True,
            "google_api_key": "YOUR_API_KEY"
        }
    )
    answer = response.json()["answer"]
    print(f"   Answer: {answer[:200]}...")

# Run complete workflow
complete_workflow()
```

---

**The SQLite database provides persistent tracking of paper loading status, enabling resumable loading sessions and preventing duplicate work!** 🚀
