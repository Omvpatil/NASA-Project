# Workflow Visualization - Final Implementation Guide

## 🎯 Overview

The workflow endpoint generates a **horizontal 5-column ReactFlow diagram** showing the complete structure of research papers:

**Paper → Author → Topic → Method → Results**

With optional citation relationships between papers.

---

## 📊 JSON Structure

### Response Format

```json
{
  "nodes": [...],
  "edges": [...],
  "query": "user search query",
  "num_papers": 5,
  "analysis": {...}
}
```

### Example Complete Response

```json
{
    "nodes": [
        // Paper A and its attributes
        {
            "id": "paperA",
            "type": "default",
            "data": { "label": "Paper: Space Plant Growth" },
            "position": { "x": 100, "y": 100 }
        },
        {
            "id": "authorA",
            "type": "default",
            "data": { "label": "Author: Dr. Rao" },
            "position": { "x": 350, "y": 100 }
        },
        {
            "id": "topicA",
            "type": "default",
            "data": { "label": "Topic: Gravity Response" },
            "position": { "x": 600, "y": 100 }
        },
        {
            "id": "methodA",
            "type": "default",
            "data": { "label": "Method: Hydroponics" },
            "position": { "x": 850, "y": 100 }
        },
        {
            "id": "resultA",
            "type": "default",
            "data": { "label": "Results: Enhanced Yield" },
            "position": { "x": 1100, "y": 100 }
        },

        // Paper B and its attributes
        {
            "id": "paperB",
            "type": "default",
            "data": { "label": "Paper: DNA Repair in Orbit" },
            "position": { "x": 100, "y": 250 }
        },
        {
            "id": "authorB",
            "type": "default",
            "data": { "label": "Author: Prof. Smith" },
            "position": { "x": 350, "y": 250 }
        },
        {
            "id": "topicB",
            "type": "default",
            "data": { "label": "Topic: Space Radiation" },
            "position": { "x": 600, "y": 250 }
        },
        {
            "id": "methodB",
            "type": "default",
            "data": { "label": "Method: Genome Sequencing" },
            "position": { "x": 850, "y": 250 }
        },
        {
            "id": "resultB",
            "type": "default",
            "data": { "label": "Results: Stable Repair Mechanism" },
            "position": { "x": 1100, "y": 250 }
        }
    ],

    "edges": [
        // Paper A connections
        { "id": "e_paperA_authorA", "source": "paperA", "target": "authorA", "label": "Authored by" },
        { "id": "e_paperA_topicA", "source": "paperA", "target": "topicA", "label": "Focuses on" },
        { "id": "e_paperA_methodA", "source": "paperA", "target": "methodA", "label": "Uses" },
        { "id": "e_paperA_resultA", "source": "paperA", "target": "resultA", "label": "Finds" },

        // Paper B connections
        { "id": "e_paperB_authorB", "source": "paperB", "target": "authorB", "label": "Authored by" },
        { "id": "e_paperB_topicB", "source": "paperB", "target": "topicB", "label": "Focuses on" },
        { "id": "e_paperB_methodB", "source": "paperB", "target": "methodB", "label": "Uses" },
        { "id": "e_paperB_resultB", "source": "paperB", "target": "resultB", "label": "Finds" },

        // Cross-paper citation
        { "id": "e_paperB_cites_paperA", "source": "paperB", "target": "paperA", "label": "Cites" }
    ]
}
```

---

## 🤖 LLM Analysis Schema

### Input Format (to LLM)

```json
{
    "papers": [
        {
            "id": "paperA",
            "title": "Paper title (max 45 chars)",
            "pmcid": "PMC123456",
            "author": "Dr. Rao",
            "topic": "Gravity Response",
            "method": "Hydroponics",
            "result": "Enhanced Yield"
        }
    ],
    "citations": [
        {
            "from": "paperB",
            "to": "paperA",
            "reason": "Builds on foundational methodology"
        }
    ]
}
```

### Extraction Rules

1. **Papers**: Each paper gets one node + 4 attribute nodes (author, topic, method, result)
2. **ID Format**: `paperA`, `paperB`, `paperC`, etc. (alphabetical sequence)
3. **Author**: Primary author only (e.g., "Dr. Rao", "Prof. Smith")
4. **Topic**: Main research area (max 40 chars)
5. **Method**: Methodology used (max 40 chars)
6. **Result**: Key finding (max 45 chars)
7. **Citations**: Only if papers actually reference each other

---

## 📐 Layout System

### Column Positions (X-axis)

-   **Column 1 - Papers**: x = 100
-   **Column 2 - Authors**: x = 350
-   **Column 3 - Topics**: x = 600
-   **Column 4 - Methods**: x = 850
-   **Column 5 - Results**: x = 1100

### Row Positions (Y-axis)

-   **Base Y**: 100
-   **Y Spacing**: 150px between papers
-   **Paper A**: y = 100
-   **Paper B**: y = 250
-   **Paper C**: y = 400
-   etc.

### Node ID Format

Each paper gets 5 nodes with consistent IDs:

-   Paper: `paperA`
-   Author: `authorA`
-   Topic: `topicA`
-   Method: `methodA`
-   Result: `resultA`

---

## 🎨 CSS Styling

### Node Classes (Applied by Frontend)

Detected by label prefix:

```css
.paper-node    /* Label starts with "Paper:" */
/* Label starts with "Paper:" */
.author-node   /* Label starts with "Author:" */
.topic-node    /* Label starts with "Topic:" */
.method-node   /* Label starts with "Method:" */
.results-node; /* Label starts with "Results:" */
```

### Edge Classes (Applied by Frontend)

Detected by label text:

```css
.author-edge   /* "Authored by" */
/* "Authored by" */
.topic-edge    /* "Focuses on" */
.method-edge   /* "Uses" */
.results-edge  /* "Finds" - dashed line */
.citation-edge; /* "Cites" - dashed line */
```

### Monochrome Theme

-   **Papers & Results**: White → Light gray gradient, strong borders
-   **Authors & Methods**: Light gray gradients
-   **Topics**: Medium gray gradient
-   **Dark Mode**: Inverted colors, light borders on dark backgrounds

---

## 🔗 Edge Connections

### Paper-to-Attribute Edges (Always Created)

```javascript
// Every paper has exactly 4 outgoing edges:
paperA → authorA   (label: "Authored by")
paperA → topicA    (label: "Focuses on")
paperA → methodA   (label: "Uses")
paperA → resultA   (label: "Finds")
```

### Citation Edges (Optional)

```javascript
// Direct paper-to-paper connections:
paperB → paperA   (label: "Cites")
```

---

## 💻 Backend Implementation

### Location

File: `/home/om_patil/Desktop/Codes/projects/NASA/NASA Project/main.py`
Endpoint: `/workflow` (POST)

### Key Functions

#### 1. LLM Prompt (lines ~683-710)

```python
workflow_prompt = f"""Analyze these research papers and extract components for a ReactFlow diagram.

Query: "{request.query}"

Papers:
{papers_info}

Extract and return a JSON object with this EXACT structure:
{{
    "papers": [
        {{"id": "paperA", "title": "...", "pmcid": "...", "author": "...", "topic": "...", "method": "...", "result": "..."}}
    ],
    "citations": [
        {{"from": "paperB", "to": "paperA", "reason": "..."}}
    ]
}}
"""
```

#### 2. Node Generation (lines ~760-850)

```python
for idx, paper in enumerate(papers_data):
    paper_id = paper.get("id", f"paper{chr(65+idx)}")  # paperA, paperB, etc.
    y_pos = y_base + (idx * y_spacing)

    # Create 5 nodes per paper
    nodes.append({"id": paper_id, "data": {"label": f"Paper: {title}"}, "position": {"x": 100, "y": y_pos}})
    nodes.append({"id": f"author{chr(65+idx)}", "data": {"label": f"Author: {author}"}, "position": {"x": 350, "y": y_pos}})
    nodes.append({"id": f"topic{chr(65+idx)}", "data": {"label": f"Topic: {topic}"}, "position": {"x": 600, "y": y_pos}})
    nodes.append({"id": f"method{chr(65+idx)}", "data": {"label": f"Method: {method}"}, "position": {"x": 850, "y": y_pos}})
    nodes.append({"id": f"result{chr(65+idx)}", "data": {"label": f"Results: {result}"}, "position": {"x": 1100, "y": y_pos}})

    # Create 4 edges per paper
    edges.append({"id": f"e_{paper_id}_author{chr(65+idx)}", "source": paper_id, "target": f"author{chr(65+idx)}", "label": "Authored by"})
    # ... etc
```

---

## 🎨 Frontend Implementation

### Location

File: `/home/om_patil/Desktop/Codes/projects/NASA/NASA-frontend/src/app/search/page.tsx`

### CSS Import

```typescript
import "./workflow-styles-new.css";
```

### Class Assignment Logic (lines ~162-205)

```typescript
// Add className to nodes based on label prefix
const nodesWithClass = result.nodes.map((node: any) => {
    let className = "";
    const label = node.data?.label || "";

    if (label.startsWith("Paper:")) className = "paper-node";
    else if (label.startsWith("Author:")) className = "author-node";
    else if (label.startsWith("Topic:")) className = "topic-node";
    else if (label.startsWith("Method:")) className = "method-node";
    else if (label.startsWith("Results:")) className = "results-node";

    className += workflowTheme === "dark" ? " dark" : "";
    return { ...node, className };
});

// Add className to edges based on label
const edgesWithClass = result.edges.map((edge: any) => {
    let className = "";
    const label = edge.label?.toLowerCase() || "";

    if (label.includes("authored by")) className = "author-edge";
    else if (label.includes("focuses on")) className = "topic-edge";
    else if (label.includes("uses")) className = "method-edge";
    else if (label.includes("finds")) className = "results-edge";
    else if (label.includes("cites")) className = "citation-edge";

    className += workflowTheme === "dark" ? " dark" : "";
    return { ...edge, className };
});
```

---

## 📋 API Request Example

```bash
curl -X POST http://localhost:8000/workflow \
  -H "Content-Type: application/json" \
  -d '{
    "query": "space radiation effects on DNA",
    "num_results": 5,
    "use_llm": true,
    "google_api_key": "your-google-api-key",
    "model_name": "gemini-2.0-flash-exp"
  }'
```

---

## ✅ Key Features

### 1. **Horizontal Flow Layout**

Papers on the left → Results on the right (natural reading direction)

### 2. **One Row Per Paper**

Each paper and all its attributes align horizontally at same Y position

### 3. **Direct Connections**

Paper directly connects to its 4 attributes (no intermediate nodes)

### 4. **Citation Tracking**

Direct paper-to-paper edges show citation relationships

### 5. **Clean IDs**

Alphabetical sequence: paperA, paperB, authorA, authorB, etc.

### 6. **ReactFlow Compatible**

Exact format matches ReactFlow documentation - no transformation needed

### 7. **Monochrome Theme**

Professional black/white/gray palette with dark mode support

---

## 🔧 Configuration

### LLM Settings

-   **Model**: `gemini-2.0-flash-exp` (or `gemini-2.5-flash`)
-   **Temperature**: 0.2 (deterministic extraction)
-   **Instructions**: "Return ONLY valid JSON, no markdown"

### Character Limits

-   Paper title: 45 chars
-   Author name: Natural length
-   Topic name: 40 chars
-   Method name: 40 chars
-   Result finding: 45 chars
-   Citation reason: 40 chars

---

## 🎯 Benefits

1. ✅ **Clear Structure**: Papers → Authors → Topics → Methods → Results
2. ✅ **Simple IDs**: paperA, authorA format (easy to debug)
3. ✅ **Horizontal Flow**: Natural left-to-right reading
4. ✅ **Citation Visibility**: Direct paper-to-paper connections
5. ✅ **ReactFlow Standard**: Exact format, no transformation
6. ✅ **Scalable**: Works with 1-10+ papers
7. ✅ **Professional**: Monochrome NASA theme
8. ✅ **Interactive**: Dark/light theme toggle

---

## 📝 Testing Checklist

-   [ ] Backend returns correct JSON structure
-   [ ] Node IDs follow paperA, authorA format
-   [ ] All papers have 5 nodes (paper + 4 attributes)
-   [ ] All papers have 4 edges (to their attributes)
-   [ ] Citation edges work correctly
-   [ ] Frontend applies correct CSS classes
-   [ ] Dark mode toggle works
-   [ ] ReactFlow renders without errors
-   [ ] Layout is clean and readable
-   [ ] Labels are truncated properly

---

## 🚀 Future Enhancements

1. **Shared Attributes**: Connect multiple papers to same author/topic if shared
2. **Node Clustering**: Group related papers visually
3. **Interactive Filters**: Show/hide by topic or method
4. **Export Options**: PNG, PDF, SVG export
5. **Zoom to Paper**: Auto-focus on selected paper
6. **Tooltips**: Show full text on hover
7. **Custom Layouts**: Vertical, circular, hierarchical options
