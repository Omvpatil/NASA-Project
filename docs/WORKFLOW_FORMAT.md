# Workflow JSON Format

## Overview

The workflow endpoint (`/workflow`) returns a simplified ReactFlow-compatible JSON structure for visualizing research paper relationships.

## Response Format

```json
{
  "nodes": [...],
  "edges": [...],
  "query": "original search query",
  "num_papers": 10,
  "analysis": {...}
}
```

## Nodes Structure

Each node follows the exact ReactFlow format:

```json
{
    "id": "unique_id",
    "type": "input|default|output", // optional
    "data": {
        "label": "Display text"
        // ... other metadata
    },
    "position": {
        "x": 400,
        "y": 100
    }
}
```

### Node Types

1. **Query Node** (Starting Point)

```json
{
    "id": "query",
    "type": "input",
    "data": { "label": "What is microgravity..." },
    "position": { "x": 400, "y": 0 }
}
```

2. **Theme Nodes** (Research Themes)

```json
{
    "id": "theme_0",
    "data": {
        "label": "Cellular Response to Microgravity",
        "description": "Studies focusing on cell behavior..."
    },
    "position": { "x": 275, "y": 200 }
}
```

3. **Paper Nodes** (Research Papers)

```json
{
    "id": "paper_0",
    "data": {
        "label": "Effects of Microgravity on Cell...",
        "pmcid": "PMC1234567",
        "category": "methodology",
        "methodology": "in vitro cell culture",
        "finding": "Reduced cell proliferation observed"
    },
    "position": { "x": 150, "y": 400 }
}
```

## Edges Structure

Each edge follows the exact ReactFlow format:

```json
{
    "id": "unique_edge_id",
    "source": "source_node_id",
    "target": "target_node_id",
    "label": "Connection description" // optional
}
```

### Edge Types

1. **Query to Theme**

```json
{
    "id": "query-theme_0",
    "source": "query",
    "target": "theme_0",
    "label": "Theme"
}
```

2. **Theme to Paper**

```json
{
    "id": "theme_0-paper_1",
    "source": "theme_0",
    "target": "paper_1",
    "label": "Related"
}
```

3. **Paper Relationships**

```json
{
    "id": "paper_0-paper_3",
    "source": "paper_0",
    "target": "paper_3",
    "label": "Builds upon foundational methodology"
}
```

## LLM Analysis Schema

The backend LLM generates this analysis structure (stored in `analysis` field):

```json
{
    "themes": [
        {
            "id": "theme_0",
            "label": "Theme Name",
            "description": "Detailed description..."
        }
    ],
    "papers": [
        {
            "id": "paper_0",
            "category": "methodology|results|review|case_study",
            "methodology": "experimental approach used",
            "key_finding": "main contribution",
            "research_stage": "foundational|developmental|validation|advanced"
        }
    ],
    "relationships": [
        {
            "from": "paper_0",
            "to": "paper_1",
            "type": "builds_on|extends|validates|contradicts|related",
            "reason": "Why they're connected"
        }
    ],
    "theme_connections": [
        {
            "theme": "theme_0",
            "papers": ["paper_0", "paper_1", "paper_2"]
        }
    ]
}
```

## Layout Algorithm

### Position Calculation

-   **Query**: Center top (x=400, y=0)
-   **Themes**: Row below query, max 3 columns, auto-centered
-   **Papers**: Positioned by `research_stage`:
    -   `foundational` → Level 2 (y≈400)
    -   `developmental` → Level 3 (y≈600)
    -   `validation` → Level 4 (y≈800)
    -   `advanced` → Level 5 (y≈1000)

### Smart Spacing

```python
def calculate_position(index, total, level):
    cols = min(3, total)  # Max 3 columns
    row = index // cols
    col = index % cols

    x_spacing = 350
    y_spacing = 200
    x_offset = (cols - 1) * x_spacing / 2

    x = (col * x_spacing) - x_offset + 400
    y = level * y_spacing + row * 180

    return {"x": int(x), "y": int(y)}
```

## Frontend Styling

The frontend adds CSS classes based on node/edge patterns:

### Node Classes

-   `query-node` - Query starting point
-   `theme-node` - Research theme groupings
-   `paper-node` - Individual papers

### Edge Classes

-   `query-edge` - Query to theme connections
-   `theme-paper-edge` - Theme to paper connections
-   `relationship-builds_on` - Papers building on each other
-   `relationship-extends` - Papers extending concepts
-   `relationship-validates` - Validation studies
-   `relationship-contradicts` - Contradictory findings

### Dark Mode

Classes automatically get ` dark` suffix when dark theme active.

## Example Full Response

```json
{
  "nodes": [
    {
      "id": "query",
      "type": "input",
      "data": {"label": "microgravity effects on cells"},
      "position": {"x": 400, "y": 0}
    },
    {
      "id": "theme_0",
      "data": {
        "label": "Cellular Mechanisms",
        "description": "How cells respond at molecular level"
      },
      "position": {"x": 275, "y": 200}
    },
    {
      "id": "paper_0",
      "data": {
        "label": "Microgravity Alters Cell Signaling...",
        "pmcid": "PMC7654321",
        "category": "methodology",
        "methodology": "RNA sequencing analysis",
        "finding": "Altered gene expression in 200+ genes"
      },
      "position": {"x": 150, "y": 400}
    }
  ],
  "edges": [
    {
      "id": "query-theme_0",
      "source": "query",
      "target": "theme_0",
      "label": "Theme"
    },
    {
      "id": "theme_0-paper_0",
      "source": "theme_0",
      "target": "paper_0",
      "label": "Related"
    }
  ],
  "query": "microgravity effects on cells",
  "num_papers": 10,
  "analysis": {
    "themes": [...],
    "papers": [...],
    "relationships": [...],
    "theme_connections": [...]
  }
}
```

## Benefits of This Format

1. **ReactFlow Compatible** - Direct drop-in, no transformation needed
2. **Simple & Clean** - No unnecessary nesting or metadata
3. **Flexible** - Easy to extend with custom node types
4. **Efficient** - Minimal data transfer
5. **Standard** - Follows ReactFlow documentation exactly
6. **Type-Safe** - Clear TypeScript interfaces

## API Usage

```bash
curl -X POST http://localhost:8000/workflow \
  -H "Content-Type: application/json" \
  -d '{
    "query": "microgravity effects on cells",
    "num_results": 10
  }'
```

## LLM Prompt Strategy

-   **Temperature**: 0.2 (deterministic, consistent)
-   **Instructions**: "Return ONLY valid JSON, no markdown"
-   **Content Preview**: 600 chars per paper
-   **Max Labels**: 60 chars for readability
-   **Clear Categories**: Predefined types and stages
-   **Relationship Focus**: Only meaningful connections
