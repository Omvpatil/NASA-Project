# Workflow Visualization - Research Paper Structure

## New Format Overview

The workflow endpoint now generates a **5-column visualization** showing:

**Papers → Authors → Topics → Methods → Results**

With citation relationships displayed between papers.

## Example Structure

```json
{
    "nodes": [
        // Column 1: Papers
        { "id": "paper_0", "data": { "label": "Paper: Microgravity Gene Studies" }, "position": { "x": 100, "y": 50 } },
        {
            "id": "paper_1",
            "data": { "label": "Paper: Cell Response to Cosmic Rays" },
            "position": { "x": 100, "y": 270 }
        },

        // Column 2: Authors
        { "id": "author_0", "data": { "label": "Author: Dr. Sharma" }, "position": { "x": 380, "y": 40 } },
        { "id": "author_1", "data": { "label": "Author: Prof. Li" }, "position": { "x": 380, "y": 260 } },

        // Column 3: Topics
        { "id": "topic_0", "data": { "label": "Topic: Microgravity Effects" }, "position": { "x": 660, "y": 60 } },
        { "id": "topic_1", "data": { "label": "Topic: Space Radiation" }, "position": { "x": 660, "y": 240 } },

        // Column 4: Methods
        { "id": "method_0", "data": { "label": "Method: Gene Sequencing" }, "position": { "x": 940, "y": 40 } },
        { "id": "method_1", "data": { "label": "Method: Cellular Assays" }, "position": { "x": 940, "y": 260 } },

        // Column 5: Results
        { "id": "result_0", "data": { "label": "Results: New Genes Identified" }, "position": { "x": 1220, "y": 50 } },
        {
            "id": "result_1",
            "data": { "label": "Results: DNA Damage Quantified" },
            "position": { "x": 1220, "y": 230 }
        },

        // Citations (between papers)
        { "id": "citation_0", "data": { "label": "Citation: Paper1 cites Paper0" }, "position": { "x": 320, "y": 160 } }
    ],

    "edges": [
        // Paper0 relationships
        { "id": "e_paper_0_author_0", "source": "paper_0", "target": "author_0", "label": "Written by" },
        { "id": "e_paper_0_topic_0", "source": "paper_0", "target": "topic_0", "label": "Explores" },
        { "id": "e_paper_0_method_0", "source": "paper_0", "target": "method_0", "label": "Uses" },
        { "id": "e_paper_0_result_0", "source": "paper_0", "target": "result_0", "label": "Finds" },

        // Paper1 relationships
        { "id": "e_paper_1_author_1", "source": "paper_1", "target": "author_1", "label": "Written by" },
        { "id": "e_paper_1_topic_1", "source": "paper_1", "target": "topic_1", "label": "Explores" },
        { "id": "e_paper_1_method_1", "source": "paper_1", "target": "method_1", "label": "Uses" },
        { "id": "e_paper_1_result_1", "source": "paper_1", "target": "result_1", "label": "Finds" },

        // Citation links
        { "id": "e_paper_1_citation_0", "source": "paper_1", "target": "citation_0", "label": "Cites" },
        { "id": "e_citation_0_paper_0", "source": "citation_0", "target": "paper_0", "label": "Refers to" }
    ]
}
```

## LLM Extraction Schema

The LLM analyzes papers and extracts:

```json
{
    "papers": [{ "id": "paper_0", "title": "Title", "pmcid": "PMC123" }],
    "authors": [{ "id": "author_0", "name": "Dr. Name", "papers": ["paper_0"] }],
    "topics": [{ "id": "topic_0", "name": "Topic", "papers": ["paper_0"] }],
    "methods": [{ "id": "method_0", "name": "Method", "papers": ["paper_0"] }],
    "results": [{ "id": "result_0", "finding": "Finding", "paper": "paper_0" }],
    "citations": [{ "id": "citation_0", "from_paper": "paper_1", "to_paper": "paper_0", "context": "How cited" }]
}
```

## Layout System

### Column Positions

-   **Papers**: x=100
-   **Authors**: x=380
-   **Topics**: x=660
-   **Methods**: x=940
-   **Results**: x=1220
-   **Citations**: x=320 (between papers)

### Vertical Spacing

-   Y-spacing: 220px between nodes
-   Citation Y: Midpoint between citing papers

## CSS Classes

Frontend applies classes based on label prefix:

### Nodes

-   `paper-node` - Label starts with "Paper:"
-   `author-node` - Label starts with "Author:"
-   `topic-node` - Label starts with "Topic:"
-   `method-node` - Label starts with "Method:"
-   `results-node` - Label starts with "Results:"
-   `citation-node` - Label starts with "Citation:"

### Edges

-   `author-edge` - "Written by"
-   `topic-edge` - "Explores"
-   `method-edge` - "Uses"
-   `results-edge` - "Finds" (dashed)
-   `citation-edge` - "Cites"/"Refers to" (dashed)

## Styling

Monochrome black/white/gray theme with gradients:

-   **Papers & Results**: White → Light gray gradient, dark borders
-   **Authors & Methods**: Light gray gradients
-   **Topics**: Medium gray gradient
-   **Citations**: Dashed borders, lighter styling

Dark mode: Inverted with dark backgrounds and light borders.

## Benefits

1. ✅ Clear research structure visualization
2. ✅ Shows complete paper metadata flow
3. ✅ Citation tracking between papers
4. ✅ Horizontal flow: Papers → ... → Results
5. ✅ ReactFlow compatible (exact format)
6. ✅ Professional monochrome theme
