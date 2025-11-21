# SummarIQ - Research Paper Summarization and Exploration Tool

A knowledge graph-based research paper analysis platform that uses RAG (Retrieval-Augmented Generation) to help researchers quickly understand new fields and search for specific information.

## Features

- **Paper Ingestion**: Upload and process scientific papers and technical reports
- **Knowledge Graph**: Automatically extract and link entities, concepts, experiments, and findings
- **RAG-Powered Summaries**: Generate intelligent summaries using retrieval-augmented generation
- **Query System**: Answer detailed queries based on graph relations
- **Recommendations**: Suggest related work based on knowledge graph connections
- **Exploration**: Visualize and explore relationships between papers, concepts, and findings

## Technology Stack

### Backend
- **FastAPI**: REST API framework
- **FalkorDB**: Graph database for knowledge graph storage
- **LlamaIndex**: RAG framework for document processing and querying
- **PostgreSQL**: Metadata and user data storage (optional)

### Frontend
- **React**: UI framework
- **TanStack Query**: Data fetching and caching
- **TanStack Router**: Type-safe routing
- **TanStack Table**: Data tables for papers and results
- **D3.js / Cytoscape.js**: Knowledge graph visualization

## Project Structure

```
SummarIQ/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core configuration
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   │   ├── graph/   # FalkorDB graph operations
│   │   │   ├── rag/     # LlamaIndex RAG operations
│   │   │   └── papers/  # Paper processing
│   │   └── schemas/     # Pydantic schemas
│   ├── main.py          # FastAPI entry point
│   ├── requirements.txt # Python dependencies
│   └── docker-compose.yml # FalkorDB and services
│
└── frontend/            # React frontend
    ├── src/
    │   ├── components/  # React components
    │   ├── pages/       # Page components
    │   ├── hooks/       # Custom hooks
    │   ├── services/    # API clients
    │   ├── stores/      # State management
    │   └── utils/       # Utilities
    ├── package.json
    └── vite.config.ts   # Vite configuration
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker and Docker Compose

### Backend Setup

1. Navigate to backend directory:
```bash
cd SummarIQ/backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start FalkorDB with Docker:
```bash
docker-compose up -d
```

5. Access FalkorDB Browser (optional):
   - Open your browser and navigate to: `http://localhost:3000`
   - This provides a web-based interface to visualize and query your knowledge graph
   - You can run Cypher queries, explore nodes and relationships, and visualize the graph structure

5. Create `.env` file:
```bash
FALKORDB_HOST=localhost
FALKORDB_PORT=6379
DATABASE_URL=sqlite+aiosqlite:///./summariq.db
SECRET_KEY=your-secret-key-here

# GROQ API (recommended - fast inference)
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.1-70b-versatile
LLM_PROVIDER=groq

# OpenAI API (for embeddings, optional)
OPENAI_API_KEY=your-openai-api-key
EMBEDDING_MODEL=text-embedding-3-small
```

**Get GROQ API Key**: Sign up at https://console.groq.com/

6. Run the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd SummarIQ/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
VITE_API_URL=http://localhost:8000
```

4. Start development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

## API Endpoints

### Papers
- `POST /api/papers/upload` - Upload a paper (PDF)
- `GET /api/papers` - List all papers
- `GET /api/papers/{paper_id}` - Get paper details
- `POST /api/papers/{paper_id}/process` - Process paper and build graph

### Knowledge Graph
- `GET /api/graph/nodes` - Get graph nodes
- `GET /api/graph/edges` - Get graph edges
- `GET /api/graph/query` - Query graph by entity/concept
- `GET /api/graph/visualization` - Get graph data for visualization

### RAG Operations
- `POST /api/rag/summarize` - Generate summary for a paper
- `POST /api/rag/query` - Query papers using RAG
- `POST /api/rag/recommend` - Get recommendations based on graph

## Development

### Backend Development

The backend uses:
- FastAPI for REST API
- FalkorDB for graph storage
- LlamaIndex for RAG operations
- Pydantic for data validation

### Frontend Development

The frontend uses:
- React 18+ with TypeScript
- TanStack Query for server state
- TanStack Router for routing
- TanStack Table for data tables
- Vite for build tooling

## License

See LICENSE file for details.

