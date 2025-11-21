from typing import List, Optional
from app.core.falkordb import FalkorDBClient
from app.schemas.graph import GraphNode, GraphEdge, GraphQueryResponse, GraphVisualizationData


class GraphService:
    def __init__(self, falkordb: FalkorDBClient):
        self.falkordb = falkordb
        self.graph = falkordb.get_graph()
    
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

