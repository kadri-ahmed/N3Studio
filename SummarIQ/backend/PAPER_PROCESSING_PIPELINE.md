# Paper Processing Pipeline & Storage

## Current Implementation Status

⚠️ **Note**: The pipeline is currently partially implemented with many TODOs. This document describes both the current state and the intended complete pipeline.

## Storage Locations

### 1. **File System Storage**
- **Location**: `./uploads/` (configurable via `UPLOAD_DIR` in `.env`)
- **Format**: PDF files stored with original filename
- **Path**: `{UPLOAD_DIR}/{filename}.pdf`
- **Example**: `./uploads/research_paper_2024.pdf`

### 2. **SQLite Database** (Planned)
- **Location**: `./summariq.db` (configurable via `DATABASE_URL`)
- **Purpose**: Store paper metadata and processing status
- **Schema**: Paper model with fields:
  - `id` (primary key)
  - `title`
  - `authors`
  - `abstract`
  - `filename`
  - `file_path`
  - `upload_date`
  - `processed` (boolean)
  - `processing_date`
  - `graph_node_id` (reference to FalkorDB node)

### 3. **FalkorDB Graph Database**
- **Location**: Redis instance on `localhost:6379`
- **Graph Name**: `summariq` (configurable)
- **Purpose**: Store paper nodes and relationships
- **Node Type**: `Paper` nodes with properties:
  - `id` (paper database ID)
  - `node_id` (unique graph node ID)
  - `title`
  - `authors`
  - `abstract`
  - `filename`

## Current Pipeline (Partial Implementation)

### Step 1: Upload ✅ (Fully Implemented)
**Endpoint**: `POST /api/v1/papers/upload`

**Process**:
1. Receive PDF file via multipart/form-data
2. Validate file extension (must be `.pdf`)
3. Save file to `./uploads/{filename}`
4. Extract basic metadata from filename (title = filename without extension)
5. ✅ Save to SQLite database (`papers` table)
6. ✅ Create Paper node in FalkorDB graph
7. ✅ Store `graph_node_id` in database for reference
8. Return paper metadata with database ID

**Implementation Details**:
- File saved to filesystem: `./uploads/{filename}.pdf`
- Metadata saved to SQLite: `summariq.db` → `papers` table
- Graph node created in FalkorDB with properties: `id`, `node_id`, `title`, `authors`, `abstract`, `filename`
- Graph node ID stored in database for bidirectional reference

### Step 2: Processing ❌ (Not Implemented)
**Endpoint**: `POST /api/v1/papers/{paper_id}/process`

**Intended Process**:
1. Load paper from database
2. Extract text from PDF using `pdfplumber` or `PyPDF2`
3. Use LlamaIndex to:
   - Chunk the document
   - Generate embeddings (using OpenAI embeddings)
   - Store chunks in vector store
4. Extract entities using NER (spaCy or NLTK):
   - Concepts
   - Methods
   - Findings
   - Experiments
   - Authors
   - Citations
5. Build knowledge graph in FalkorDB:
   - Create Paper node (if not exists)
   - Create entity nodes (Concept, Method, Finding, etc.)
   - Create relationships:
     - `Paper -[:CONTAINS]-> Concept`
     - `Paper -[:USES]-> Method`
     - `Paper -[:FINDS]-> Finding`
     - `Concept -[:RELATED_TO]-> Concept`
     - `Paper -[:CITES]-> Paper`
6. Update paper status: `processed = True`

### Step 3: RAG Operations ❌ (Not Implemented)
**Endpoints**:
- `POST /api/v1/rag/summarize`
- `POST /api/v1/rag/query`
- `POST /api/v1/rag/recommend`

**Intended Process**:
1. Use LlamaIndex query engine with GROQ LLM
2. Retrieve relevant chunks from vector store
3. Generate summaries/queries using RAG
4. Return results with citations

## Complete Pipeline Flow

```
┌─────────────────┐
│  User Uploads   │
│     PDF File    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Save to Disk   │  ← ./uploads/{filename}.pdf
│  (File System)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Save Metadata   │  ← SQLite Database (summariq.db)
│  to Database    │     - Paper record with metadata
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Create Paper    │  ← FalkorDB Graph
│  Node in Graph  │     - Paper node with properties
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Process Paper  │  ← Manual trigger or auto
│   (Optional)   │
└────────┬────────┘
         │
         ├─────────────────┬─────────────────┬─────────────────┐
         ▼                 ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Extract Text │  │   Chunk &    │  │ Extract      │  │ Build        │
│ from PDF     │  │   Embed      │  │ Entities     │  │ Knowledge    │
│              │  │              │  │ (NER)         │  │ Graph        │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
     pdfplumber      LlamaIndex         spaCy/NLTK      FalkorDB
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND                                │
│  PaperUpload Component → POST /api/v1/papers/upload        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND API                              │
│  papers.py → PaperService.upload_paper()                    │
└────────┬───────────────────────────┬────────────────────────┘
         │                           │
         ▼                           ▼
┌─────────────────┐         ┌─────────────────┐
│  File System    │         │  SQLite DB      │
│  ./uploads/     │         │  summariq.db    │
│  {filename}.pdf │         │  papers table   │
└─────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │   FalkorDB      │
                            │   Graph DB      │
                            │   Paper Node    │
                            └─────────────────┘
```

## Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| File Upload | ✅ Implemented | Saves PDFs to `./uploads/` |
| Database Model | ✅ Implemented | Paper model created in `app/models/paper.py` |
| Database Storage | ✅ Implemented | Papers saved to SQLite database |
| FalkorDB Integration | ✅ Implemented | Paper nodes created in graph on upload |
| PDF Text Extraction | ❌ Not Implemented | TODO in `process_paper()` |
| LlamaIndex Integration | ❌ Not Implemented | Setup exists but not used |
| Entity Extraction (NER) | ❌ Not Implemented | TODO in `process_paper()` |
| Knowledge Graph Building | ❌ Not Implemented | TODO in `process_paper()` |
| RAG Operations | ❌ Not Implemented | Service exists but methods are placeholders |

## Next Steps to Complete Pipeline

1. **Recreate Paper Database Model**
   - Create `app/models/paper.py` with SQLAlchemy model
   - Add to `app/main.py` for table creation

2. **Implement Database Storage**
   - Update `PaperService.upload_paper()` to save to database
   - Update `PaperService.list_papers()` to query database
   - Update `PaperService.get_paper()` to query database

3. **Implement FalkorDB Integration**
   - Create Paper node in graph during upload
   - Store `graph_node_id` in database

4. **Implement PDF Processing**
   - Add PDF text extraction using `pdfplumber`
   - Integrate LlamaIndex document loader
   - Generate embeddings and store in vector store

5. **Implement Entity Extraction**
   - Use spaCy for NER
   - Extract: concepts, methods, findings, citations
   - Create entity nodes in FalkorDB

6. **Build Knowledge Graph**
   - Create relationships between papers and entities
   - Create relationships between entities
   - Update graph visualization endpoint

7. **Implement RAG Operations**
   - Set up LlamaIndex query engine
   - Implement summarization
   - Implement query functionality
   - Implement recommendations based on graph

## Configuration

All storage paths and settings are configured in `app/core/config.py`:

```python
UPLOAD_DIR = "./uploads"              # File storage directory
DATABASE_URL = "sqlite+aiosqlite:///./summariq.db"  # SQLite database
FALKORDB_HOST = "localhost"           # FalkorDB host
FALKORDB_PORT = 6379                   # FalkorDB port
FALKORDB_GRAPH_NAME = "summariq"      # Graph name
```

## File Structure

```
backend/
├── uploads/                    # PDF files stored here
│   └── paper1.pdf
│   └── paper2.pdf
├── summariq.db                 # SQLite database
└── app/
    ├── models/
    │   └── paper.py            # Paper database model (TODO)
    ├── services/
    │   ├── papers.py           # Paper upload/processing service
    │   ├── graph.py             # Graph operations
    │   └── rag.py               # RAG operations
    └── core/
        ├── database.py          # SQLite connection
        └── falkordb.py          # FalkorDB connection
```

