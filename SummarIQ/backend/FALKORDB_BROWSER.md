# FalkorDB Browser Guide

## Connecting to FalkorDB Browser

FalkorDB includes a built-in web-based browser interface for visualizing and querying your knowledge graph.

### Quick Start

1. **Start FalkorDB with Browser**:
   ```bash
   cd SummarIQ/backend
   docker-compose up -d
   ```

2. **Access the Browser**:
   Open your web browser and navigate to:
   ```
   http://localhost:3000
   ```

### Using the Browser Interface

The FalkorDB Browser provides:

- **Graph Visualization**: Interactive visualization of nodes and relationships
- **Cypher Query Editor**: Run Cypher queries directly in the browser
- **Graph Explorer**: Navigate through your knowledge graph
- **Statistics**: View graph statistics and metrics

### Example Queries

Once connected, you can run Cypher queries like:

```cypher
// View all nodes
MATCH (n) RETURN n LIMIT 100

// View all relationships
MATCH (a)-[r]->(b) RETURN a, r, b LIMIT 100

// Find specific entity
MATCH (n {name: "Machine Learning"}) RETURN n

// Get neighbors of a node
MATCH (n {name: "Machine Learning"})-[r]-(connected) RETURN n, r, connected

// Count nodes by label
MATCH (n) RETURN labels(n) as label, count(n) as count
```

### Alternative: Using redis-cli

You can also connect using the Redis CLI:

```bash
docker exec -it summariq-falkordb redis-cli
```

Then run graph queries:
```bash
GRAPH.QUERY summariq "MATCH (n) RETURN n LIMIT 10"
```

### Troubleshooting

- **Browser not accessible**: Make sure port 3000 is not already in use
- **Connection refused**: Verify the container is running: `docker ps`
- **Graph not found**: Make sure your graph name matches `FALKORDB_GRAPH_NAME` in your `.env` file (default: "summariq")

### Stopping the Browser

To stop FalkorDB and the browser:
```bash
docker-compose down
```

To stop but keep data:
```bash
docker-compose stop
```

