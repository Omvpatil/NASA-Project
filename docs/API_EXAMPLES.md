# 📡 Complete API Request/Response Examples

This document contains detailed examples for all 8 API endpoints with complete request/response payloads.

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
    "description": "RAG-powered search API for space biology research papers",
    "docs": "/docs",
    "endpoints": {
        "health": "/health",
        "search": "/search",
        "database_status": "/database-status",
        "papers": "/papers",
        "models": "/models",
        "load_papers": "/load-papers",
        "reset": "/reset-database"
    }
}
```

---

## 2. GET `/health` - Health Check

### Request

```bash
curl http://localhost:8000/health
```

### Response (Healthy)

```json
{
    "status": "healthy",
    "database": "loaded",
    "embeddings": "initialized",
    "timestamp": "2025-10-03T19:45:30.123456"
}
```

### Response (Database Not Loaded)

```json
{
    "status": "healthy",
    "database": "not_loaded",
    "embeddings": "not_initialized",
    "timestamp": "2025-10-03T19:45:30.123456"
}
```

---

## 3. GET `/database-status` - Database Status

### Request

```bash
curl http://localhost:8000/database-status
```

### Response (Database Loaded)

```json
{
    "status": "loaded",
    "total_documents": 45,
    "total_papers": 10,
    "collection_name": "space_biology_papers",
    "persist_directory": "./chroma_db",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "embedding_dimension": 384,
    "sample_papers": [
        {
            "title": "Microgravity induces pelvic bone loss through osteoclastic activity",
            "pmcid": "PMC8234567",
            "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/"
        },
        {
            "title": "Mice in Bion-M 1 space mission: proteomic analysis of liver",
            "pmcid": "PMC7654321",
            "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7654321/"
        }
    ]
}
```

### Response (Database Empty)

```json
{
    "status": "empty",
    "total_documents": 0,
    "total_papers": 0,
    "message": "Database is empty. Use /load-papers to load papers."
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
            "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/",
            "chunks": 5
        },
        {
            "title": "Mice in Bion-M 1 space mission: proteomic analysis of liver",
            "pmcid": "PMC7654321",
            "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7654321/",
            "chunks": 4
        },
        {
            "title": "Effects of spaceflight on the circadian rhythm",
            "pmcid": "PMC9876543",
            "source": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9876543/",
            "chunks": 6
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
    "available_models": [
        {
            "name": "gemini-2.5-flash",
            "description": "Fast and efficient model (default)",
            "recommended": true
        },
        {
            "name": "gemini-1.5-pro",
            "description": "More capable model for complex queries",
            "recommended": false
        },
        {
            "name": "gemini-1.5-flash",
            "description": "Balanced performance and speed",
            "recommended": false
        }
    ],
    "default_model": "gemini-2.5-flash",
    "note": "Requires Google API key. Get one at: https://aistudio.google.com/apikey"
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

## 7. POST `/load-papers` - Load Papers from CSV

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
    "message": "Successfully loaded 10 papers and created 47 chunks",
    "papers": [
        {
            "title": "Microgravity induces pelvic bone loss through osteoclastic activity",
            "pmcid": "PMC8234567",
            "chunks": 5
        },
        {
            "title": "Mice in Bion-M 1 space mission: proteomic analysis of liver",
            "pmcid": "PMC7654321",
            "chunks": 4
        },
        {
            "title": "Effects of spaceflight on the circadian rhythm",
            "pmcid": "PMC9876543",
            "chunks": 6
        }
        // ... 7 more papers
    ],
    "time_taken": "125.5 seconds"
}
```

#### Response (Error - CSV Not Found)

```json
{
    "detail": "CSV file not found. Please check the path: https://raw.githubusercontent.com/jgalazka/SB_publications/main/SB_publications.csv"
}
```

---

### Example 2: Load All Papers

#### Request

```bash
curl -X POST "http://localhost:8000/load-papers" \
  -H "Content-Type: application/json" \
  -d '{
    "num_papers": 0
  }'
```

#### Response

```json
{
    "status": "success",
    "papers_loaded": 156,
    "chunks_created": 823,
    "message": "Successfully loaded 156 papers and created 823 chunks",
    "papers": [
        // ... all papers
    ],
    "time_taken": "1845.2 seconds"
}
```

---

## 8. POST `/reset-database` - Reset Database

### Request

```bash
curl -X POST "http://localhost:8000/reset-database" \
  -H "Content-Type: application/json"
```

### Response (Success)

```json
{
    "status": "success",
    "message": "Database reset successfully. All papers and embeddings have been deleted.",
    "previous_count": 45,
    "current_count": 0
}
```

### Response (Database Already Empty)

```json
{
    "status": "success",
    "message": "Database was already empty",
    "previous_count": 0,
    "current_count": 0
}
```

---

## 9. POST `/search/on-demand` - On-Demand Search with Image Extraction

### Description

Advanced search that:

1. Searches abstract database first
2. Identifies relevant papers
3. Scrapes full content + images on-demand
4. Returns answer with image URLs

### Request

````bash
curl -X POST "http://localhost:8000/search/on-demand" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does microgravity affect bone density?",
    "num_results": 5,
    "use_llm": true,
    "google_api_key": "YOUR_API_KEY",
    "model_name": "gemini-2.5-flash"
  }'


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
    "timestamp": "2025-10-04T10:30:00.123456"
}
```
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

    # 2. Load papers (if needed)
    status = client.database_status()
    if status.get("total_documents", 0) == 0:
        print("Loading papers...")
        result = client.load_papers(num_papers=10)
        print(f"Loaded {result['papers_loaded']} papers")

    # 3. Search without LLM
    results = client.search(
        query="bone loss in space",
        num_results=5,
        use_llm=False
    )
    print(f"\nFound {results['num_results']} papers")

    # 4. Search with LLM
    results = client.search(
        query="How does microgravity affect bones?",
        num_results=5,
        use_llm=True,
        google_api_key="YOUR_API_KEY"
    )
    print(f"\nAI Answer: {results['answer']}")

    # 5. Search with keyword filter
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

    async loadPapers(numPapers = 10) {
        const response = await fetch(`${this.baseURL}/load-papers`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ num_papers: numPapers }),
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

    // Search
    const results = await client.search({
        query: "bone loss in microgravity",
        numResults: 5,
        useLLM: true,
        googleApiKey: "YOUR_API_KEY",
    });
    console.log("Answer:", results.answer);
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

# 2. Check database status
echo -e "\n=== Database Status ==="
curl -s $BASE_URL/database-status | jq '.'

# 3. Load papers if empty
echo -e "\n=== Loading Papers ==="
curl -s -X POST "$BASE_URL/load-papers" \
  -H "Content-Type: application/json" \
  -d '{"num_papers": 10}' | jq '.'

# 4. List papers
echo -e "\n=== List Papers ==="
curl -s $BASE_URL/papers | jq '.papers[] | {title, pmcid, chunks}'

# 5. Basic search
echo -e "\n=== Basic Search ==="
curl -s -X POST "$BASE_URL/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "bone loss",
    "num_results": 3,
    "use_llm": false
  }' | jq '.source_documents[] | .metadata.title'

# 6. Search with LLM
echo -e "\n=== Search with AI Answer ==="
curl -s -X POST "$BASE_URL/search" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"How does microgravity affect bones?\",
    \"num_results\": 5,
    \"use_llm\": true,
    \"google_api_key\": \"$API_KEY\"
  }" | jq '.answer'

# 7. Keyword filtered search
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
```

---

## Testing Checklist

-   [ ] **GET /health** - Returns healthy status
-   [ ] **GET /database-status** - Shows correct document count
-   [ ] **GET /papers** - Lists all loaded papers
-   [ ] **GET /models** - Returns available models
-   [ ] **POST /search** (no LLM) - Returns document results
-   [ ] **POST /search** (with LLM) - Returns AI answer + sources
-   [ ] **POST /search** (keyword filter) - Filters by title keywords
-   [ ] **POST /search** (MMR) - Returns diverse results
-   [ ] **POST /load-papers** - Successfully loads papers
-   [ ] **POST /reset-database** - Clears all documents

---

**All endpoints are documented in interactive Swagger UI at: http://localhost:8000/docs** 🚀
