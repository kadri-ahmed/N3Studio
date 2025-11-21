from typing import List, Optional, Dict, Any
import uuid
from app.core.falkordb import FalkorDBClient
from app.schemas.graph import GraphNode, GraphEdge, GraphQueryResponse, GraphVisualizationData


class GraphService:
    def __init__(self, falkordb: FalkorDBClient):
        self.falkordb = falkordb
        self.graph = falkordb.get_graph()
    
    def create_paper_node(
        self,
        paper_id: int,
        title: str,
        authors: Optional[str] = None,
        abstract: Optional[str] = None,
        filename: Optional[str] = None
    ) -> str:
        """Create a Paper node in the graph"""
        node_id = f"paper_{paper_id}_{uuid.uuid4().hex[:8]}"
        
        # Use parameterized query for safety
        query = """
        CREATE (p:Paper {
            id: $paper_id,
            node_id: $node_id,
            title: $title,
            authors: $authors,
            abstract: $abstract,
            filename: $filename
        })
        RETURN p
        """
        
        params = {
            "paper_id": paper_id,
            "node_id": node_id,
            "title": title or "",
            "authors": authors or "",
            "abstract": abstract or "",
            "filename": filename or ""
        }
        
        try:
            result = self.graph.query(query, params)
            return node_id
        except Exception as e:
            print(f"Error creating paper node: {e}")
            # If parameterized query fails, try direct string interpolation (less safe but works)
            # Escape single quotes
            def escape(s: str) -> str:
                return s.replace("'", "\\'") if s else ""
            
            query_direct = f"""
            CREATE (p:Paper {{
                id: {paper_id},
                node_id: '{node_id}',
                title: '{escape(title or "")}',
                authors: '{escape(authors or "")}',
                abstract: '{escape(abstract or "")}',
                filename: '{escape(filename or "")}'
            }})
            RETURN p
            """
            try:
                result = self.graph.query(query_direct)
                return node_id
            except Exception as e2:
                print(f"Error with direct query: {e2}")
                raise
    
    async def get_nodes(self, label: Optional[str] = None, limit: int = 100) -> List[GraphNode]:
        """Get graph nodes"""
        if label:
            query = f"MATCH (n:{label}) RETURN n LIMIT {limit}"
        else:
            query = f"MATCH (n) RETURN n LIMIT {limit}"
        
        result = self.graph.query(query)
        nodes = []
        for record in result.result_set:
            node = record[0]
            nodes.append(GraphNode(
                id=str(node.id),
                label=list(node.labels)[0] if node.labels else "Node",
                properties=node.properties
            ))
        return nodes
    
    async def get_edges(self, relationship: Optional[str] = None, limit: int = 100) -> List[GraphEdge]:
        """Get graph edges"""
        if relationship:
            query = f"MATCH (a)-[r:{relationship}]->(b) RETURN a, r, b LIMIT {limit}"
        else:
            query = f"MATCH (a)-[r]->(b) RETURN a, r, b LIMIT {limit}"
        
        result = self.graph.query(query)
        edges = []
        for record in result.result_set:
            source, rel, target = record
            edges.append(GraphEdge(
                id=str(rel.id),
                source=str(source.id),
                target=str(target.id),
                relationship=rel.relation,
                properties=rel.properties
            ))
        return edges
    
    async def query_entity(self, entity: str, depth: int = 2) -> GraphQueryResponse:
        """Query graph by entity/concept"""
        query = f"""
        MATCH path = (start)-[*1..{depth}]-(connected)
        WHERE start.name CONTAINS $entity OR start.title CONTAINS $entity
        RETURN path
        LIMIT 100
        """
        
        result = self.graph.query(query, {"entity": entity})
        # TODO: Process result and extract nodes, edges, paths
        return GraphQueryResponse(
            nodes=[],
            edges=[],
            paths=[]
        )
    
    async def get_visualization_data(self, paper_id: Optional[int] = None, limit: int = 500) -> dict:
        """Get graph data formatted for visualization"""
        if paper_id:
            query = f"""
            MATCH (p:Paper {{id: $paper_id}})-[*1..2]-(connected)
            RETURN p, connected
            LIMIT {limit}
            """
            result = self.graph.query(query, {"paper_id": paper_id})
        else:
            query = f"MATCH (n)-[r]->(m) RETURN n, r, m LIMIT {limit}"
            result = self.graph.query(query)
        
        # TODO: Format for visualization library (D3.js / Cytoscape.js)
        return {
            "nodes": [],
            "edges": []
        }

