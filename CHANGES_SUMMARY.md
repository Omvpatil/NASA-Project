# Changes Summary - Image Display & Smart Caching

## Issues Fixed

### 1. Images Not Showing in Frontend

**Problem**: ChromaDB was rejecting list-type metadata (image URLs), causing errors.

**Solution**:

-   Store image URLs as JSON strings in metadata (`image_urls_json`)
-   Parse JSON strings back to lists when returning API responses
-   Frontend receives proper array of image URLs

### 2. Papers Being Re-Scraped on Every Query

**Problem**: System was always searching abstracts first, then checking if papers are loaded, leading to unnecessary re-scraping.

**Solution**:

-   **Smart search logic**: First search in main vector store (full papers)
-   If enough results found (>= num_results), use those directly (no scraping needed)
-   Only search abstracts if main store doesn't have enough results
-   Track loaded papers properly to avoid duplicate scraping

## Backend Changes (`main.py`)

### Imports Added

```python
import json
from langchain_community.vectorstores.utils import filter_complex_metadata
```

### Image Storage Format

-   **Before**: `"image_urls": [list]` → ❌ ChromaDB rejected
-   **After**: `"image_urls_json": json.dumps([list])` → ✅ ChromaDB accepts

### Search Endpoint Improvements

#### New Search Flow:

1. **First**: Search main vector store (full papers)

    - If ≥ num_results found → Use them (no scraping)
    - If < num_results → Continue to step 2

2. **Second**: Search abstract database

    - Check if papers already loaded
    - Only scrape if not loaded

3. **Response**: Parse JSON strings back to lists
    - `image_urls_json` → `image_urls` (list)

### Code Changes

#### In `/search` endpoint:

```python
# Smart search - try main store first
if vector_store:
    main_docs = main_retriever.invoke(request.query)
    if len(main_docs) >= request.num_results:
        # Enough results, no scraping needed!
        all_relevant_docs = main_docs
        loaded_papers = [...]
        print(f"✅ Found {len(main_docs)} results in main vector store")
```

#### Image storage:

```python
# Store as JSON string
doc = Document(
    page_content=text,
    metadata={
        "title": paper["title"],
        "source": paper["link"],
        "pmcid": paper["pmcid"] or "",
        "image_urls_json": json.dumps(image_urls) if image_urls else "",
    },
)
```

#### Image retrieval:

```python
# Parse JSON string back to list
image_urls_json = doc.metadata.get("image_urls_json", "")
try:
    image_urls = json.loads(image_urls_json) if image_urls_json else []
except:
    image_urls = paper_images_map.get(doc_title, [])
```

## Frontend (Already Working)

The frontend code in `search/page.tsx` already has proper image display:

-   Shows up to 3 thumbnail previews
-   Click to open full image
-   Shows "+N more" for additional images
-   Displays image count badges

## Benefits

### Performance Improvements

1. **No re-scraping**: Already loaded papers retrieved from vector store
2. **Faster responses**: Main store searched first
3. **Reduced API calls**: PMC website not hit unnecessarily

### Data Integrity

1. **Images preserved**: JSON string format compatible with ChromaDB
2. **Metadata maintained**: All paper information intact
3. **No data loss**: Images available for all papers

### User Experience

1. **Consistent results**: Same query returns same data
2. **Image previews**: Visual context for papers
3. **Faster searches**: Cached papers load instantly

## Testing

### To verify the fixes:

1. Make a search query → Images should display
2. Make the same query again → Should NOT re-scrape (check logs)
3. Check response in Network tab → `image_urls` should be an array

### Expected console output:

```
✅ Found 10 results in main vector store (full papers)
```

(Instead of re-scraping messages)

## Migration Notes

**Existing Data**: Papers loaded before this change won't have `image_urls_json`. They will:

-   Show no images (metadata missing)
-   Need to be re-scraped to get images

**New Data**: All newly scraped papers will have images properly stored and displayed.
