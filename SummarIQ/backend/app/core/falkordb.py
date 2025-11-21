import redis
from redisgraph import Graph
from app.core.config import settings


class FalkorDBClient:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.FALKORDB_HOST,
            port=settings.FALKORDB_PORT,
            decode_responses=True
        )
        self.graph = Graph(settings.FALKORDB_GRAPH_NAME, self.redis_client)
    
    def get_graph(self) -> Graph:
        """Get the FalkorDB graph instance"""
        return self.graph
    
    def query(self, query: str, params: dict = None):
        """Execute a Cypher query"""
        return self.graph.query(query, params)
    
    def close(self):
        """Close the Redis connection"""
        self.redis_client.close()


# Global instance
falkordb_client = FalkorDBClient()


def get_falkordb() -> FalkorDBClient:
    """Dependency to get FalkorDB client"""
    return falkordb_client

