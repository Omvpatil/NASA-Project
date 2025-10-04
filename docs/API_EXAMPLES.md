# 📡 Complete API Request/Response Examples

This document contains detailed examples for all API endpoints with complete request/response payloads.

## Endpoint Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/health` | Health check status |
| GET | `/database-status` | Vector database status |
| GET | `/papers` | List all papers in vector store |
| GET | `/models` | List available LLM models |
| POST | `/database/load-csv` | Load CSV into SQLite database |
| GET | `/database/stats` | SQLite database statistics |
| GET | `/database/papers/loaded` | Get loaded papers from database |
| GET | `/database/papers/unloaded` | Get unloaded papers from database |
| GET | `/database/papers/all` | Get all papers from database |
| GET | `/database/papers/search` | Search papers in database by title |
| POST | `/database/append-csv` | Append new CSV to database |
| POST | `/load-papers` | Scrape and load papers with embeddings |
| POST | `/search` | Search papers (with optional LLM) |
| POST | `/search/on-demand` | On-demand search with image extraction |
| POST | `/reset-database` | Reset all databases |

---

## 1. GET `/` - Root/Welcome Endpoint

### Request

```bash
curl http://localhost:8000/
```

### Response

```json
{
    "message": "NASA Space Biology Knowledge Engine API",
    "version": "1.0.0",
    "endpoints": {
        "health": "/health",
        "search": "/search (POST)",
        "load_papers": "/load-papers (POST)",
        "database_status": "/database-status",
        "papers_list": "/papers",
        "reset_database": "/reset-database (POST)"
    }
}
```

---

## 2. GET `/health` - Health Check

### Request

```bash
curl http://localhost:8000/health
```

### Response

```json
{
    "status": "healthy",
    "database_loaded": true,
    "timestamp": "2025-10-05T19:45:30.123456"
}
```

---

## 3. GET `/database-status` - Database Status

### Request

```bash
curl http://localhost:8000/database-status
```

### Response

```json
{
    "status": "loaded",
    "collection_name": "space_biology_papers",
    "persist_directory": "./chroma_db",
    "total_chunks": 823,
    "total_papers": 156
}
```

---

## 4. GET `/papers` - List All Papers

### Request

```bash
curl http://localhost:8000/papers
```

### Response

```json
{
    "total_papers": 10,
    "papers": [
        {
            "title": "Microgravity induces pelvic bone loss through osteoclastic activity",
            "pmcid": "PMC8234567",
            "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/"
        },
        {
            "title": "Mice in Bion-M 1 space mission: proteomic analysis of liver",
            "pmcid": "PMC7654321",
            "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7654321/"
        },
        {
            "title": "Effects of spaceflight on the circadian rhythm",
            "pmcid": "PMC9876543",
            "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9876543/"
        }
    ]
}
```

---

## 5. GET `/models` - List Available LLM Models

### Request

```bash
curl http://localhost:8000/models
```

### Response

```json
{
    "models": [
        {
            "name": "gemini-2.5-flash",
            "description": "Latest Gemini 2.5 (Fast, Experimental)"
        },
        {
            "name": "gemini-2.5-pro",
            "description": "Gemini 2.5 Pro (Balanced)"
        },
        {
            "name": "gemini-1.5-pro",
            "description": "Gemini 1.5 Pro (Most Capable)"
        },
        {
            "name": "gemini-1.0-pro",
            "description": "Gemini 1.0 Pro (Legacy)"
        }
    ]
}
```

---

## 6. POST `/search` - Search Papers

### Example 1: Basic Search (No LLM)

#### Request

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "bone loss in microgravity",
    "num_results": 5,
    "use_llm": false
  }'
```

#### Response

```json
{
    "answer": null,
    "source_documents": [
        {
            "page_content": "Microgravity induces pelvic bone loss through osteoclastic activity. Studies show that prolonged exposure to microgravity leads to significant bone mineral density reduction, primarily affecting weight-bearing bones such as the pelvis and femur. The process involves increased osteoclast activity and decreased osteoblast function...",
            "metadata": {
                "title": "Microgravity induces pelvic bone loss through osteoclastic activity",
                "pmcid": "PMC8234567",
                "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/"
            }
        },
        {
            "page_content": "Analysis of bone remodeling in astronauts revealed that microgravity conditions cause a 1-2% monthly bone loss in weight-bearing regions. This accelerated bone loss is comparable to osteoporosis in elderly individuals...",
            "metadata": {
                "title": "Bone remodeling during spaceflight: mechanisms and countermeasures",
                "pmcid": "PMC9123456",
                "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9123456/"
            }
        },
        {
            "page_content": "The Bion-M 1 mission provided valuable insights into skeletal changes in microgravity. Mice exposed to 30 days of spaceflight showed significant trabecular bone loss and altered bone architecture...",
            "metadata": {
                "title": "Mice in Bion-M 1 space mission: skeletal analysis",
                "pmcid": "PMC7654321",
                "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7654321/"
            }
        },
        {
            "page_content": "Countermeasures for bone loss include resistance exercise protocols and bisphosphonate medication. Studies indicate that high-intensity resistance training can partially mitigate microgravity-induced bone loss...",
            "metadata": {
                "title": "Exercise countermeasures for spaceflight-induced bone loss",
                "pmcid": "PMC8765432",
                "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8765432/"
            }
        },
        {
            "page_content": "Calcium metabolism is significantly altered in microgravity environments. Increased urinary calcium excretion combined with reduced calcium absorption contributes to the overall bone loss phenotype...",
            "metadata": {
                "title": "Calcium homeostasis during spaceflight",
                "pmcid": "PMC9234567",
                "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9234567/"
            }
        }
    ],
    "query": "bone loss in microgravity",
    "num_results": 5,
    "timestamp": "2025-10-03T19:50:15.234567"
}
```

---

### Example 2: Search with LLM Answer

#### Request

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does microgravity affect bone density in astronauts?",
    "num_results": 8,
    "use_llm": true,
    "google_api_key": "AIzaSy...",
    "model_name": "gemini-2.5-flash",
    "search_method": "similarity"
  }'
```

#### Response

```json
{
    "answer": "According to the research papers, microgravity has significant negative effects on bone density in astronauts:\n\n**Key Findings:**\n\n1. **Bone Loss Rate**: Astronauts experience approximately 1-2% bone loss per month in weight-bearing bones during spaceflight, which is comparable to the annual bone loss rate in elderly individuals with osteoporosis.\n\n2. **Affected Areas**: The most affected regions include:\n   - Pelvic bones\n   - Femur (thigh bone)\n   - Lumbar spine\n   - Heel bones\n\n3. **Mechanisms**: The bone loss occurs through:\n   - Increased osteoclastic activity (bone breakdown)\n   - Decreased osteoblastic function (bone formation)\n   - Altered calcium metabolism\n   - Increased urinary calcium excretion\n\n4. **Countermeasures**: Research suggests several mitigation strategies:\n   - High-intensity resistance exercise (2+ hours daily)\n   - Bisphosphonate medications\n   - Optimized nutrition with adequate calcium and vitamin D\n   - Vibration therapy\n\n5. **Long-term Implications**: The Bion-M 1 mission data shows that even after 30 days in space, significant trabecular bone loss and altered bone architecture can occur, raising concerns for long-duration missions to Mars.\n\n**Sources:**\n- \"Microgravity induces pelvic bone loss through osteoclastic activity\" (PMC8234567)\n- \"Bone remodeling during spaceflight: mechanisms and countermeasures\" (PMC9123456)\n- \"Mice in Bion-M 1 space mission: skeletal analysis\" (PMC7654321)\n- \"Exercise countermeasures for spaceflight-induced bone loss\" (PMC8765432)",
    "source_documents": [
        {
            "page_content": "Microgravity induces pelvic bone loss through osteoclastic activity...",
            "metadata": {
                "title": "Microgravity induces pelvic bone loss through osteoclastic activity",
                "pmcid": "PMC8234567",
                "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/"
            }
        }
        // ... (7 more documents)
    ],
    "query": "How does microgravity affect bone density in astronauts?",
    "num_results": 8,
    "timestamp": "2025-10-03T19:52:30.456789"
}
```

---

### Example 3: Search with Keyword Filter

#### Request

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "space mission results",
    "num_results": 10,
    "use_llm": true,
    "google_api_key": "AIzaSy...",
    "model_name": "gemini-2.5-flash",
    "search_method": "similarity",
    "use_keyword_filter": true,
    "keyword_filter": "Bion, ISS, mission"
  }'
```

#### Response

```json
{
    "answer": "The Bion-M 1 and ISS missions have provided crucial insights into space biology:\n\n**Bion-M 1 Mission Findings:**\n- 30-day spaceflight caused significant physiological changes in mice\n- Liver proteomic analysis revealed altered metabolic pathways\n- Skeletal analysis showed trabecular bone loss\n- Muscle atrophy was observed in hindlimb muscles\n\n**ISS Research Results:**\n- Long-duration studies on protein crystallization\n- Plant growth experiments in microgravity\n- Circadian rhythm disruption in astronauts\n- Immune system changes during extended stays\n\n**Sources:**\n- \"Mice in Bion-M 1 space mission: proteomic analysis of liver\" (PMC7654321)\n- \"ISS research on circadian rhythm regulation\" (PMC8123456)",
    "source_documents": [
        {
            "page_content": "Mice in Bion-M 1 space mission: proteomic analysis of liver...",
            "metadata": {
                "title": "Mice in Bion-M 1 space mission: proteomic analysis of liver",
                "pmcid": "PMC7654321",
                "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7654321/"
            }
        },
        {
            "page_content": "ISS research on circadian rhythm regulation...",
            "metadata": {
                "title": "ISS research on circadian rhythm regulation",
                "pmcid": "PMC8123456",
                "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8123456/"
            }
        }
        // Only papers with "Bion", "ISS", or "mission" in title
    ],
    "query": "space mission results",
    "num_results": 2,
    "timestamp": "2025-10-03T19:55:00.789012"
}
```

---

### Example 4: Search with MMR (Maximum Marginal Relevance)

#### Request

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "radiation effects on astronauts",
    "num_results": 5,
    "use_llm": false,
    "search_method": "mmr"
  }'
```

#### Response

```json
{
    "answer": null,
    "source_documents": [
        {
            "page_content": "Cosmic radiation exposure during spaceflight poses significant health risks...",
            "metadata": {
                "title": "Radiation protection strategies for deep space missions",
                "pmcid": "PMC9345678",
                "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9345678/"
            }
        },
        {
            "page_content": "DNA damage from galactic cosmic rays can lead to increased cancer risk...",
            "metadata": {
                "title": "Molecular mechanisms of radiation-induced damage",
                "pmcid": "PMC8456789",
                "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8456789/"
            }
        },
        {
            "page_content": "Circadian rhythm disruption is another concern for astronauts...",
            "metadata": {
                "title": "Sleep and circadian rhythm in space",
                "pmcid": "PMC7567890",
                "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7567890/"
            }
        }
        // MMR provides diverse results
    ],
    "query": "radiation effects on astronauts",
    "num_results": 5,
    "timestamp": "2025-10-03T19:57:00.123456"
}
```

---

## 7. POST `/database/load-csv` - Load CSV to SQLite Database

### Description
Loads the CSV file from GitHub into the SQLite database without scraping papers. This is the first step before loading full papers.

### Request

```bash
curl -X POST "http://localhost:8000/database/load-csv" \
  -H "Content-Type: application/json"
```

### Response

```json
{
    "status": "success",
    "message": "CSV loaded into database",
    "stats": {
        "total_papers": 607,
        "new_papers_added": 607,
        "duplicate_papers_skipped": 0,
        "papers_already_loaded": 0,
        "papers_unloaded": 607
    }
}
```

---

## 8. POST `/load-papers` - Load Papers from CSV

### Description
Scrapes full papers and creates embeddings. Must run `/database/load-csv` first.

### Example 1: Load 10 Papers

#### Request

```bash
curl -X POST "http://localhost:8000/load-papers" \
  -H "Content-Type: application/json" \
  -d '{
    "num_papers": 10
  }'
```

#### Response (Success)

```json
{
    "status": "success",
    "papers_loaded": 10,
    "chunks_created": 47,
    "message": "Successfully loaded 10 papers and created 47 chunks"
}
```

#### Response (Error - No Papers in Database)

```json
{
    "status": "success",
    "papers_loaded": 0,
    "chunks_created": 0,
    "message": "All papers already loaded or no papers available. Load CSV first using /database/load-csv"
}
```

---

### Example 2: Load All Available Papers

#### Request

```bash
curl -X POST "http://localhost:8000/load-papers" \
  -H "Content-Type: application/json" \
  -d '{
    "num_papers": 607
  }'
```

#### Response

```json
{
    "status": "success",
    "papers_loaded": 156,
    "chunks_created": 823,
    "message": "Successfully loaded 156 papers and created 823 chunks"
}
```

---

## 9. POST `/reset-database` - Reset Database

### Description
Resets both the vector database and SQLite tracking database.

### Request

```bash
curl -X POST "http://localhost:8000/reset-database" \
  -H "Content-Type: application/json"
```

### Response

```json
{
    "status": "success",
    "message": "Both databases reset successfully. Use /load-papers to create new databases."
}
```

---

## 10. GET `/database/stats` - Get Database Statistics

### Request

```bash
curl http://localhost:8000/database/stats
```

### Response

```json
{
    "total_papers": 607,
    "loaded_papers": 156,
    "unloaded_papers": 451,
    "total_chunks_created": 823,
    "database_path": "./papers.db"
}
```

---

## 11. GET `/database/papers/loaded` - Get Loaded Papers

### Request

```bash
curl "http://localhost:8000/database/papers/loaded?limit=5"
```

### Response

```json
{
    "count": 5,
    "papers": [
        {
            "id": 1,
            "title": "Microgravity induces pelvic bone loss through osteoclastic activity",
            "pmcid": "PMC8234567",
            "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/",
            "isLoaded": true,
            "loadedAt": "2025-10-05T10:30:00",
            "chunksCreated": 5
        },
        {
            "id": 2,
            "title": "Mice in Bion-M 1 space mission: proteomic analysis of liver",
            "pmcid": "PMC7654321",
            "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7654321/",
            "isLoaded": true,
            "loadedAt": "2025-10-05T10:31:00",
            "chunksCreated": 4
        }
    ]
}
```

---

## 12. GET `/database/papers/unloaded` - Get Unloaded Papers

### Request

```bash
curl "http://localhost:8000/database/papers/unloaded?limit=3"
```

### Response

```json
{
    "count": 3,
    "papers": [
        {
            "id": 157,
            "title": "Effects of spaceflight on cardiovascular system",
            "pmcid": "PMC9999999",
            "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9999999/",
            "isLoaded": false,
            "loadedAt": null,
            "chunksCreated": 0
        }
    ]
}
```

---

## 13. GET `/database/papers/all` - Get All Papers

### Request

```bash
curl http://localhost:8000/database/papers/all
```

### Response

```json
{
    "count": 607,
    "papers": [
        {
            "id": 1,
            "title": "Microgravity induces pelvic bone loss through osteoclastic activity",
            "pmcid": "PMC8234567",
            "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/",
            "isLoaded": true,
            "loadedAt": "2025-10-05T10:30:00",
            "chunksCreated": 5
        }
        // ... 606 more papers
    ]
}
```

---

## 14. GET `/database/papers/search` - Search Papers in Database

### Request

```bash
curl "http://localhost:8000/database/papers/search?query=bone%20loss&loaded_only=true"
```

### Response

```json
{
    "query": "bone loss",
    "count": 3,
    "papers": [
        {
            "id": 1,
            "title": "Microgravity induces pelvic bone loss through osteoclastic activity",
            "pmcid": "PMC8234567",
            "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/",
            "isLoaded": true,
            "loadedAt": "2025-10-05T10:30:00",
            "chunksCreated": 5
        },
        {
            "id": 45,
            "title": "Bone remodeling during spaceflight: mechanisms and countermeasures",
            "pmcid": "PMC9123456",
            "link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9123456/",
            "isLoaded": true,
            "loadedAt": "2025-10-05T10:35:00",
            "chunksCreated": 6
        }
    ]
}
```

---

## 15. POST `/database/append-csv` - Append CSV to Database

### Description
Append papers from a new CSV file to the existing database.

### Request

```bash
curl -X POST "http://localhost:8000/database/append-csv" \
  -H "Content-Type: application/json" \
  -d '{
    "csv_url": "https://example.com/new_papers.csv"
  }'
```

### Response

```json
{
    "status": "success",
    "message": "CSV appended successfully",
    "stats": {
        "total_papers": 650,
        "new_papers_added": 43,
        "duplicate_papers_skipped": 0,
        "papers_already_loaded": 156,
        "papers_unloaded": 494
    }
}
```

---

## 16. POST `/search/on-demand` - On-Demand Search with Image Extraction

### Description

Advanced search that:

1. Searches abstract database first
2. Identifies relevant papers
3. Scrapes full content + images on-demand
4. Returns answer with image URLs

### Request

```bash
curl -X POST "http://localhost:8000/search/on-demand" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does microgravity affect bone density?",
    "num_results": 5,
    "use_llm": true,
    "google_api_key": "YOUR_API_KEY",
    "model_name": "gemini-2.5-flash"
  }'
```

### Response

```json
{
    "answer": "According to research papers, microgravity significantly affects bone density...\n\n**Key Findings with Visual Evidence:**\n- Figure 1 (PMC8234567) shows trabecular bone loss\n- Figure 2 (PMC9123456) demonstrates osteoclast activity\n\n**Sources:**\n- \"Microgravity induces pelvic bone loss\" (PMC8234567)\n- \"Bone remodeling during spaceflight\" (PMC9123456)",
    "source_documents": [
        {
            "page_content": "Microgravity induces pelvic bone loss...",
            "metadata": {
                "title": "Microgravity induces pelvic bone loss through osteoclastic activity",
                "pmcid": "PMC8234567",
                "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/",
                "image_urls": [
                    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/bin/figure1.jpg",
                    "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/bin/figure2.jpg"
                ]
            }
        }
    ],
    "images_found": [
        {
            "pmcid": "PMC8234567",
            "title": "Microgravity induces pelvic bone loss...",
            "images": [
                "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/bin/figure1.jpg",
                "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/bin/figure2.jpg"
            ]
        }
    ],
    "papers_newly_scraped": 2,
    "papers_already_loaded": 3,
    "query": "How does microgravity affect bone density?",
    "timestamp": "2025-10-05T10:30:00.123456"
}
```

### Python Example

```python
import requests

response = requests.post(
    "http://localhost:8000/search/on-demand",
    json={
        "query": "bone loss mechanisms in space",
        "num_results": 5,
        "use_llm": True,
        "google_api_key": "YOUR_API_KEY"
    }
)

result = response.json()
print(f"Answer: {result['answer']}\n")
print(f"Newly scraped: {result['papers_newly_scraped']} papers")
print(f"Already loaded: {result['papers_already_loaded']} papers")

# Display images
for img_data in result['images_found']:
    print(f"\n{img_data['title']}:")
    for img_url in img_data['images']:
        print(f"  - {img_url}")
```

---

## Error Responses

### 404 - Database Not Loaded

```json
{
    "detail": "Vector database not loaded. Please load papers first using /load-papers endpoint."
}
````

### 422 - Validation Error (Invalid Request)

```json
{
    "detail": [
        {
            "type": "int_parsing",
            "loc": ["body", "num_results"],
            "msg": "Input should be a valid integer, unable to parse string as an integer",
            "input": "invalid"
        }
    ]
}
```

### 500 - Internal Server Error

```json
{
    "detail": "An error occurred while processing your request: Connection timeout"
}
```

---

## Python Client Examples

### Complete Client Class

```python
import requests
from typing import Optional, List, Dict, Any
import json

class NASARAGClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()

    def database_status(self) -> Dict[str, Any]:
        """Get database status"""
        response = requests.get(f"{self.base_url}/database-status")
        return response.json()

    def list_papers(self) -> Dict[str, Any]:
        """List all loaded papers"""
        response = requests.get(f"{self.base_url}/papers")
        return response.json()

    def list_models(self) -> Dict[str, Any]:
        """List available LLM models"""
        response = requests.get(f"{self.base_url}/models")
        return response.json()

    def load_csv_to_database(self) -> Dict[str, Any]:
        """Load CSV into SQLite database"""
        response = requests.post(f"{self.base_url}/database/load-csv")
        return response.json()

    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        response = requests.get(f"{self.base_url}/database/stats")
        return response.json()

    def get_loaded_papers(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get loaded papers from database"""
        params = {"limit": limit} if limit else {}
        response = requests.get(f"{self.base_url}/database/papers/loaded", params=params)
        return response.json()

    def get_unloaded_papers(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """Get unloaded papers from database"""
        params = {"limit": limit} if limit else {}
        response = requests.get(f"{self.base_url}/database/papers/unloaded", params=params)
        return response.json()

    def get_all_papers_from_db(self) -> Dict[str, Any]:
        """Get all papers from database"""
        response = requests.get(f"{self.base_url}/database/papers/all")
        return response.json()

    def search_papers_in_db(self, query: str, loaded_only: bool = False) -> Dict[str, Any]:
        """Search papers in database by title"""
        params = {"query": query, "loaded_only": loaded_only}
        response = requests.get(f"{self.base_url}/database/papers/search", params=params)
        return response.json()

    def append_csv(self, csv_url: str) -> Dict[str, Any]:
        """Append papers from new CSV to database"""
        payload = {"csv_url": csv_url}
        response = requests.post(f"{self.base_url}/database/append-csv", json=payload)
        return response.json()

    def search(
        self,
        query: str,
        num_results: int = 10,
        use_llm: bool = True,
        google_api_key: Optional[str] = None,
        model_name: str = "gemini-2.5-flash",
        search_method: str = "similarity",
        use_keyword_filter: bool = False,
        keyword_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """Search papers"""
        payload = {
            "query": query,
            "num_results": num_results,
            "use_llm": use_llm,
            "google_api_key": google_api_key,
            "model_name": model_name,
            "search_method": search_method,
            "use_keyword_filter": use_keyword_filter,
            "keyword_filter": keyword_filter
        }
        response = requests.post(f"{self.base_url}/search", json=payload)
        return response.json()

    def on_demand_search(
        self,
        query: str,
        num_results: int = 5,
        use_llm: bool = True,
        google_api_key: Optional[str] = None,
        model_name: str = "gemini-2.5-flash"
    ) -> Dict[str, Any]:
        """On-demand search with image extraction"""
        payload = {
            "query": query,
            "num_results": num_results,
            "use_llm": use_llm,
            "google_api_key": google_api_key,
            "model_name": model_name
        }
        response = requests.post(f"{self.base_url}/search/on-demand", json=payload)
        return response.json()

    def load_papers(self, num_papers: int = 10) -> Dict[str, Any]:
        """Load papers from CSV"""
        payload = {"num_papers": num_papers}
        response = requests.post(f"{self.base_url}/load-papers", json=payload)
        return response.json()

    def reset_database(self) -> Dict[str, Any]:
        """Reset database"""
        response = requests.post(f"{self.base_url}/reset-database")
        return response.json()


# Usage examples
if __name__ == "__main__":
    client = NASARAGClient()

    # 1. Check health
    print("Health:", client.health_check())

    # 2. Load CSV to database
    print("\nLoading CSV to database...")
    csv_result = client.load_csv_to_database()
    print(f"Stats: {csv_result['stats']}")

    # 3. Check database stats
    stats = client.get_database_stats()
    print(f"\nDatabase stats: {stats}")

    # 4. Load papers (if needed)
    if stats.get("unloaded_papers", 0) > 0:
        print("\nLoading papers...")
        result = client.load_papers(num_papers=10)
        print(f"Loaded {result['papers_loaded']} papers")

    # 5. Get loaded papers
    loaded = client.get_loaded_papers(limit=5)
    print(f"\nLoaded papers: {loaded['count']}")

    # 6. Search in database
    db_search = client.search_papers_in_db("bone", loaded_only=True)
    print(f"\nDatabase search results: {db_search['count']} papers")

    # 7. Search without LLM
    results = client.search(
        query="bone loss in space",
        num_results=5,
        use_llm=False
    )
    print(f"\nFound {results['num_results']} papers")

    # 8. Search with LLM
    results = client.search(
        query="How does microgravity affect bones?",
        num_results=5,
        use_llm=True,
        google_api_key="YOUR_API_KEY"
    )
    print(f"\nAI Answer: {results['answer']}")

    # 9. On-demand search with images
    on_demand_results = client.on_demand_search(
        query="bone density mechanisms in space",
        num_results=3,
        use_llm=True,
        google_api_key="YOUR_API_KEY"
    )
    print(f"\nOn-demand search:")
    print(f"  Papers newly scraped: {on_demand_results['papers_newly_scraped']}")
    print(f"  Papers already loaded: {on_demand_results['papers_already_loaded']}")
    print(f"  Images found: {len(on_demand_results['images_found'])}")

    # 10. Search with keyword filter
    results = client.search(
        query="space mission findings",
        num_results=10,
        use_llm=True,
        google_api_key="YOUR_API_KEY",
        use_keyword_filter=True,
        keyword_filter="Bion, ISS"
    )
    print(f"\nFiltered results: {results['num_results']} papers")
```

---

## JavaScript/TypeScript Examples

### Async/Await Client

```javascript
class NASARAGClient {
    constructor(baseURL = "http://localhost:8000") {
        this.baseURL = baseURL;
    }

    async healthCheck() {
        const response = await fetch(`${this.baseURL}/health`);
        return await response.json();
    }

    async databaseStatus() {
        const response = await fetch(`${this.baseURL}/database-status`);
        return await response.json();
    }

    async loadCSVToDatabase() {
        const response = await fetch(`${this.baseURL}/database/load-csv`, {
            method: "POST",
        });
        return await response.json();
    }

    async getDatabaseStats() {
        const response = await fetch(`${this.baseURL}/database/stats`);
        return await response.json();
    }

    async getLoadedPapers(limit = null) {
        const url = limit 
            ? `${this.baseURL}/database/papers/loaded?limit=${limit}`
            : `${this.baseURL}/database/papers/loaded`;
        const response = await fetch(url);
        return await response.json();
    }

    async getUnloadedPapers(limit = null) {
        const url = limit 
            ? `${this.baseURL}/database/papers/unloaded?limit=${limit}`
            : `${this.baseURL}/database/papers/unloaded`;
        const response = await fetch(url);
        return await response.json();
    }

    async searchPapersInDB(query, loadedOnly = false) {
        const url = `${this.baseURL}/database/papers/search?query=${encodeURIComponent(query)}&loaded_only=${loadedOnly}`;
        const response = await fetch(url);
        return await response.json();
    }

    async appendCSV(csvUrl) {
        const response = await fetch(`${this.baseURL}/database/append-csv`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ csv_url: csvUrl }),
        });
        return await response.json();
    }

    async search({
        query,
        numResults = 10,
        useLLM = true,
        googleApiKey = null,
        modelName = "gemini-2.5-flash",
        searchMethod = "similarity",
        useKeywordFilter = false,
        keywordFilter = null,
    }) {
        const response = await fetch(`${this.baseURL}/search`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                query,
                num_results: numResults,
                use_llm: useLLM,
                google_api_key: googleApiKey,
                model_name: modelName,
                search_method: searchMethod,
                use_keyword_filter: useKeywordFilter,
                keyword_filter: keywordFilter,
            }),
        });
        return await response.json();
    }

    async onDemandSearch({
        query,
        numResults = 5,
        useLLM = true,
        googleApiKey = null,
        modelName = "gemini-2.5-flash",
    }) {
        const response = await fetch(`${this.baseURL}/search/on-demand`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                query,
                num_results: numResults,
                use_llm: useLLM,
                google_api_key: googleApiKey,
                model_name: modelName,
            }),
        });
        return await response.json();
    }

    async loadPapers(numPapers = 10) {
        const response = await fetch(`${this.baseURL}/load-papers`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ num_papers: numPapers }),
        });
        return await response.json();
    }

    async resetDatabase() {
        const response = await fetch(`${this.baseURL}/reset-database`, {
            method: "POST",
        });
        return await response.json();
    }
}

// Usage
(async () => {
    const client = new NASARAGClient();

    // Check health
    const health = await client.healthCheck();
    console.log("Health:", health);

    // Load CSV
    const csvResult = await client.loadCSVToDatabase();
    console.log("CSV loaded:", csvResult.stats);

    // Get database stats
    const stats = await client.getDatabaseStats();
    console.log("Database stats:", stats);

    // Load papers
    if (stats.unloaded_papers > 0) {
        const loadResult = await client.loadPapers(10);
        console.log("Loaded papers:", loadResult.papers_loaded);
    }

    // Search in database
    const dbSearch = await client.searchPapersInDB("bone", true);
    console.log("Database search:", dbSearch.count, "papers");

    // Search with LLM
    const results = await client.search({
        query: "bone loss in microgravity",
        numResults: 5,
        useLLM: true,
        googleApiKey: "YOUR_API_KEY",
    });
    console.log("Answer:", results.answer);

    // On-demand search
    const onDemandResults = await client.onDemandSearch({
        query: "bone density in space",
        numResults: 3,
        useLLM: true,
        googleApiKey: "YOUR_API_KEY",
    });
    console.log("On-demand results:");
    console.log("  Newly scraped:", onDemandResults.papers_newly_scraped);
    console.log("  Images found:", onDemandResults.images_found.length);
})();
```

---

## cURL Complete Examples

### Sequential Workflow

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"
API_KEY="YOUR_GOOGLE_API_KEY"

# 1. Health check
echo "=== Health Check ==="
curl -s $BASE_URL/health | jq '.'

# 2. Load CSV into database
echo -e "\n=== Loading CSV to Database ==="
curl -s -X POST "$BASE_URL/database/load-csv" | jq '.'

# 3. Check database stats
echo -e "\n=== Database Stats ==="
curl -s $BASE_URL/database/stats | jq '.'

# 4. Load papers (scrape full content)
echo -e "\n=== Loading Papers ==="
curl -s -X POST "$BASE_URL/load-papers" \
  -H "Content-Type: application/json" \
  -d '{"num_papers": 10}' | jq '.'

# 5. Check vector database status
echo -e "\n=== Vector Database Status ==="
curl -s $BASE_URL/database-status | jq '.'

# 6. List loaded papers
echo -e "\n=== Loaded Papers ==="
curl -s "$BASE_URL/database/papers/loaded?limit=5" | jq '.papers[] | {title, pmcid, chunksCreated}'

# 7. List papers
echo -e "\n=== List Papers ==="
curl -s $BASE_URL/papers | jq '.papers[] | {title, pmcid}'

# 8. Basic search
echo -e "\n=== Basic Search ==="
curl -s -X POST "$BASE_URL/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "bone loss",
    "num_results": 3,
    "use_llm": false
  }' | jq '.source_documents[] | .metadata.title'

# 9. Search with LLM
echo -e "\n=== Search with AI Answer ==="
curl -s -X POST "$BASE_URL/search" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"How does microgravity affect bones?\",
    \"num_results\": 5,
    \"use_llm\": true,
    \"google_api_key\": \"$API_KEY\"
  }" | jq '.answer'

# 10. Keyword filtered search
echo -e "\n=== Keyword Filtered Search ==="
curl -s -X POST "$BASE_URL/search" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"space mission results\",
    \"num_results\": 10,
    \"use_llm\": true,
    \"google_api_key\": \"$API_KEY\",
    \"use_keyword_filter\": true,
    \"keyword_filter\": \"Bion, ISS\"
  }" | jq '.source_documents[] | .metadata.title'

# 11. Search papers in database
echo -e "\n=== Search Papers in Database ==="
curl -s "$BASE_URL/database/papers/search?query=bone&loaded_only=true" | jq '.'

# 12. On-demand search with images
echo -e "\n=== On-Demand Search ==="
curl -s -X POST "$BASE_URL/search/on-demand" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"bone density in space\",
    \"num_results\": 3,
    \"use_llm\": true,
    \"google_api_key\": \"$API_KEY\"
  }" | jq '{answer: .answer, images_found: .images_found, papers_newly_scraped: .papers_newly_scraped}'
```

---

## API Workflow

### Initial Setup

1. **Load CSV to Database**
```bash
curl -X POST "http://localhost:8000/database/load-csv"
```

2. **Check Database Stats**
```bash
curl http://localhost:8000/database/stats
```

3. **Load Papers (Scrape Full Content)**
```bash
curl -X POST "http://localhost:8000/load-papers" \
  -H "Content-Type: application/json" \
  -d '{"num_papers": 10}'
```

4. **Verify Database Status**
```bash
curl http://localhost:8000/database-status
```

### Search Operations

1. **Basic Search**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "bone loss in space",
    "num_results": 5,
    "use_llm": false
  }'
```

2. **Search with AI Answer**
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does microgravity affect bones?",
    "num_results": 5,
    "use_llm": true,
    "google_api_key": "YOUR_API_KEY"
  }'
```

3. **On-Demand Search (with Images)**
```bash
curl -X POST "http://localhost:8000/search/on-demand" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "bone density mechanisms",
    "num_results": 5,
    "use_llm": true,
    "google_api_key": "YOUR_API_KEY"
  }'
```

---

## Testing Checklist

### Core Endpoints
- [ ] **GET /** - Returns API info
- [ ] **GET /health** - Returns healthy status
- [ ] **GET /database-status** - Shows correct chunk count
- [ ] **GET /papers** - Lists all loaded papers
- [ ] **GET /models** - Returns available models

### Database Management
- [ ] **POST /database/load-csv** - Loads CSV into SQLite
- [ ] **GET /database/stats** - Shows database statistics
- [ ] **GET /database/papers/loaded** - Lists loaded papers
- [ ] **GET /database/papers/unloaded** - Lists unloaded papers
- [ ] **GET /database/papers/all** - Lists all papers
- [ ] **GET /database/papers/search** - Searches papers by title
- [ ] **POST /database/append-csv** - Appends new CSV

### Paper Loading
- [ ] **POST /load-papers** - Successfully loads papers
- [ ] **POST /reset-database** - Clears all databases

### Search Features
- [ ] **POST /search** (no LLM) - Returns document results
- [ ] **POST /search** (with LLM) - Returns AI answer + sources
- [ ] **POST /search** (keyword filter) - Filters by title keywords
- [ ] **POST /search** (MMR) - Returns diverse results
- [ ] **POST /search/on-demand** - Scrapes and returns with images

---

**All endpoints are documented in interactive Swagger UI at: http://localhost:8000/docs** 🚀
