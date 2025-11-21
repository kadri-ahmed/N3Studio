from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class GraphNode(BaseModel):
    id: str
    label: str
    properties: Dict[str, Any]


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    relationship: str
    properties: Dict[str, Any]


class GraphQueryResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    paths: List[List[str]]  # List of paths found


class GraphVisualizationData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

