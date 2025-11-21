from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from app.core.falkordb import get_falkordb, FalkorDBClient
from app.schemas.graph import GraphNode, GraphEdge, GraphQueryResponse
from app.services.graph import GraphService

router = APIRouter()


@router.get("/nodes", response_model=List[GraphNode])
async def get_nodes(
    label: Optional[str] = Query(None, description="Filter by node label"),
    limit: int = Query(100, ge=1, le=1000),
    falkordb: FalkorDBClient = Depends(get_falkordb)
):
    """Get graph nodes"""
    graph_service = GraphService(falkordb)
    nodes = await graph_service.get_nodes(label=label, limit=limit)
    return nodes


@router.get("/edges", response_model=List[GraphEdge])
async def get_edges(
    relationship: Optional[str] = Query(None, description="Filter by relationship type"),
    limit: int = Query(100, ge=1, le=1000),
    falkordb: FalkorDBClient = Depends(get_falkordb)
):
    """Get graph edges"""
    graph_service = GraphService(falkordb)
    edges = await graph_service.get_edges(relationship=relationship, limit=limit)
    return edges


@router.get("/query", response_model=GraphQueryResponse)
async def query_graph(
    entity: str = Query(..., description="Entity or concept to search for"),
    depth: int = Query(2, ge=1, le=5, description="Traversal depth"),
    falkordb: FalkorDBClient = Depends(get_falkordb)
):
    """Query graph by entity/concept"""
    graph_service = GraphService(falkordb)
    result = await graph_service.query_entity(entity, depth=depth)
    return result


@router.get("/visualization", response_model=dict)
async def get_visualization_data(
    paper_id: Optional[int] = Query(None, description="Filter by paper ID"),
    limit: int = Query(500, ge=1, le=2000),
    falkordb: FalkorDBClient = Depends(get_falkordb)
):
    """Get graph data formatted for visualization"""
    graph_service = GraphService(falkordb)
    data = await graph_service.get_visualization_data(paper_id=paper_id, limit=limit)
    return data

