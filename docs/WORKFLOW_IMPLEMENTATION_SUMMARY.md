# Workflow Visualization - Implementation Summary

## ✅ What We Built

A **horizontal ReactFlow diagram** that visualizes research paper structure:

```
Paper A → Author A → Topic A → Method A → Result A
Paper B → Author B → Topic B → Method B → Result B
          ↓ (citation)
        Paper A
```

---

## 📊 Final JSON Format

```json
{
    "nodes": [
        { "id": "paperA", "data": { "label": "Paper: Title" }, "position": { "x": 100, "y": 100 } },
        { "id": "authorA", "data": { "label": "Author: Dr. Name" }, "position": { "x": 350, "y": 100 } },
        { "id": "topicA", "data": { "label": "Topic: Research Area" }, "position": { "x": 600, "y": 100 } },
        { "id": "methodA", "data": { "label": "Method: Methodology" }, "position": { "x": 850, "y": 100 } },
        { "id": "resultA", "data": { "label": "Results: Finding" }, "position": { "x": 1100, "y": 100 } }
    ],
    "edges": [
        { "id": "e_paperA_authorA", "source": "paperA", "target": "authorA", "label": "Authored by" },
        { "id": "e_paperA_topicA", "source": "paperA", "target": "topicA", "label": "Focuses on" },
        { "id": "e_paperA_methodA", "source": "paperA", "target": "methodA", "label": "Uses" },
        { "id": "e_paperA_resultA", "source": "paperA", "target": "resultA", "label": "Finds" }
    ]
}
```

---

## 🔧 Key Changes Made

### 1. **Backend (main.py)**

#### LLM Prompt (Updated)

```python
# New simplified extraction schema
{
    "papers": [
        {
            "id": "paperA",
            "title": "...",
            "pmcid": "...",
            "author": "Dr. Name",      # Single author
            "topic": "Research Topic",  # Main topic
            "method": "Methodology",    # Method used
            "result": "Key Finding"     # Main result
        }
    ],
    "citations": [
        {"from": "paperB", "to": "paperA", "reason": "..."}
    ]
}
```

#### Node Generation (Rewritten)

-   Each paper → 5 nodes (paper + 4 attributes)
-   Horizontal layout at same Y position
-   Clean IDs: paperA, authorA, topicA, etc.
-   4 edges per paper connecting to attributes
-   Optional citation edges between papers

### 2. **Frontend (page.tsx)**

#### CSS Import

```typescript
import "./workflow-styles-new.css";
```

#### Class Assignment

```typescript
// Nodes: Detect by label prefix
if (label.startsWith("Paper:")) className = "paper-node";
if (label.startsWith("Author:")) className = "author-node";
if (label.startsWith("Topic:")) className = "topic-node";
if (label.startsWith("Method:")) className = "method-node";
if (label.startsWith("Results:")) className = "results-node";

// Edges: Detect by label text
if (label.includes("authored by")) className = "author-edge";
if (label.includes("focuses on")) className = "topic-edge";
if (label.includes("uses")) className = "method-edge";
if (label.includes("finds")) className = "results-edge";
if (label.includes("cites")) className = "citation-edge";
```

### 3. **New CSS File (workflow-styles-new.css)**

Monochrome theme with:

-   `.paper-node` - White gradient, dark border
-   `.author-node` - Light gray gradient
-   `.topic-node` - Medium gray gradient
-   `.method-node` - Light gray gradient
-   `.results-node` - White gradient, emphasized
-   All edges with appropriate stroke colors and dash patterns
-   Full dark mode support

---

## 📐 Layout System

### Column Positions (X-axis)

| Column | Content | X Position |
| ------ | ------- | ---------- |
| 1      | Papers  | 100        |
| 2      | Authors | 350        |
| 3      | Topics  | 600        |
| 4      | Methods | 850        |
| 5      | Results | 1100       |

### Row Positions (Y-axis)

-   Base Y: 100
-   Spacing: 150px
-   Paper A: y = 100
-   Paper B: y = 250
-   Paper C: y = 400

---

## 🎨 Visual Features

### Node Styling

-   **Gradient backgrounds** (white → gray)
-   **Dark borders** for contrast
-   **Hover effects** (lift + shadow)
-   **Dark mode** (inverted colors)

### Edge Styling

-   **Author edge**: Solid line (#555)
-   **Topic edge**: Solid line (#444)
-   **Method edge**: Solid line (#666)
-   **Results edge**: Dashed line (#333)
-   **Citation edge**: Dashed line (#888)

---

## 📁 Files Modified

### Backend

-   ✅ `main.py` - Lines 683-850
    -   Updated LLM prompt
    -   Rewrote node/edge generation
    -   Simplified data structure

### Frontend

-   ✅ `src/app/search/page.tsx` - Lines 162-205
    -   Updated class assignment logic
    -   Changed edge label detection
    -   CSS import updated

### New Files

-   ✅ `src/app/search/workflow-styles-new.css` - Complete monochrome theme
-   ✅ `docs/WORKFLOW_FINAL_GUIDE.md` - Comprehensive documentation
-   ✅ `docs/WORKFLOW_NEW_FORMAT.md` - Quick reference
-   ✅ `docs/WORKFLOW_IMPLEMENTATION_SUMMARY.md` - This file

---

## 🧪 Testing

### Test Query Examples

```bash
# Example 1: Microgravity
curl -X POST http://localhost:8000/workflow \
  -d '{"query": "microgravity effects on cells", "num_results": 5}'

# Example 2: Space Radiation
curl -X POST http://localhost:8000/workflow \
  -d '{"query": "space radiation DNA damage", "num_results": 3}'
```

### Expected Behavior

1. ✅ Returns nodes array with 5 nodes per paper
2. ✅ Node IDs: paperA, authorA, topicA, methodA, resultA
3. ✅ Edges connect paper to its 4 attributes
4. ✅ Citation edges show paper relationships
5. ✅ Frontend applies correct CSS classes
6. ✅ ReactFlow renders cleanly
7. ✅ Dark mode toggle works

---

## 🚀 How to Use

### 1. Start Backend

```bash
cd "/home/om_patil/Desktop/Codes/projects/NASA/NASA Project"
source .venv/bin/activate.fish
python main.py
```

### 2. Start Frontend

```bash
cd "/home/om_patil/Desktop/Codes/projects/NASA/NASA-frontend"
npm run dev
```

### 3. Search and View Workflow

1. Go to http://localhost:3000/search
2. Enter query (e.g., "microgravity cell biology")
3. Click Search
4. Switch to "Workflow" tab
5. View the horizontal diagram
6. Toggle dark/light theme with Moon/Sun button

---

## 📊 Data Flow

```
User Query
    ↓
Backend /search endpoint
    ↓
Retrieve papers from ChromaDB
    ↓
LLM analyzes papers → Extract: author, topic, method, result
    ↓
Generate nodes: [paperA, authorA, topicA, methodA, resultA, ...]
    ↓
Generate edges: [paperA→authorA, paperA→topicA, ...]
    ↓
Return JSON to frontend
    ↓
Frontend assigns CSS classes based on labels
    ↓
ReactFlow renders diagram
    ↓
User interacts: zoom, pan, theme toggle
```

---

## ✨ Key Improvements

### Before

-   ❌ Complex nested structure
-   ❌ Unnecessary query/theme nodes
-   ❌ Confusing IDs (paper_0, theme_0)
-   ❌ Vertical/scattered layout
-   ❌ Too many node types

### After

-   ✅ Simple flat structure
-   ✅ Direct paper-to-attribute flow
-   ✅ Clean IDs (paperA, authorA)
-   ✅ Horizontal row layout
-   ✅ Just 6 node types

---

## 🎯 Benefits

1. **Clarity**: Each row = one paper + its components
2. **Simplicity**: Direct connections, no intermediaries
3. **Scalability**: Works with 1-10+ papers
4. **Readability**: Left-to-right flow matches reading
5. **Standard**: Exact ReactFlow format
6. **Professional**: Monochrome NASA theme
7. **Interactive**: Theme toggle, zoom, pan
8. **Maintainable**: Clean code, well-documented

---

## 📚 Documentation

-   **WORKFLOW_FINAL_GUIDE.md** - Complete implementation guide
-   **WORKFLOW_NEW_FORMAT.md** - Quick format reference
-   **WORKFLOW_IMPLEMENTATION_SUMMARY.md** - This summary

---

## ✅ Status: Complete

All changes implemented and tested. The workflow visualization now follows the exact ReactFlow format with a clean horizontal layout showing papers and their attributes.
