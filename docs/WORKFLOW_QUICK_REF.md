# 🚀 Workflow Quick Reference

## Node Structure (5 per paper)

```
paperA    authorA    topicA    methodA    resultA
  │          │          │          │          │
 100        350        600        850       1100  (x-position)
```

## Edge Labels

| Edge           | Label         | Style  |
| -------------- | ------------- | ------ |
| Paper → Author | "Authored by" | Solid  |
| Paper → Topic  | "Focuses on"  | Solid  |
| Paper → Method | "Uses"        | Solid  |
| Paper → Result | "Finds"       | Dashed |
| Paper → Paper  | "Cites"       | Dashed |

## CSS Classes

**Nodes** (by label prefix):

-   `Paper:` → `.paper-node`
-   `Author:` → `.author-node`
-   `Topic:` → `.topic-node`
-   `Method:` → `.method-node`
-   `Results:` → `.results-node`

**Edges** (by label text):

-   "Authored by" → `.author-edge`
-   "Focuses on" → `.topic-edge`
-   "Uses" → `.method-edge`
-   "Finds" → `.results-edge`
-   "Cites" → `.citation-edge`

## Layout Formula

```javascript
// For paper index i (0, 1, 2, ...):
paperX:  x=100,  y=100 + (i * 150)
authorX: x=350,  y=100 + (i * 150)
topicX:  x=600,  y=100 + (i * 150)
methodX: x=850,  y=100 + (i * 150)
resultX: x=1100, y=100 + (i * 150)

// ID format:
paper{chr(65+i)}  // paperA, paperB, paperC...
```

## LLM Response Format

```json
{
    "papers": [
        {
            "id": "paperA",
            "title": "Title (45 chars)",
            "pmcid": "PMC123",
            "author": "Dr. Name",
            "topic": "Topic (40 chars)",
            "method": "Method (40 chars)",
            "result": "Finding (45 chars)"
        }
    ],
    "citations": [{ "from": "paperB", "to": "paperA", "reason": "Why" }]
}
```

## API Call

```bash
POST http://localhost:8000/workflow
{
  "query": "your search query",
  "num_results": 5,
  "use_llm": true,
  "google_api_key": "key",
  "model_name": "gemini-2.0-flash-exp"
}
```

## Files Changed

-   ✅ `main.py` (lines 683-850)
-   ✅ `src/app/search/page.tsx` (lines 162-205)
-   ✅ `src/app/search/workflow-styles-new.css` (new)
