from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class SummarizeRequest(BaseModel):
    paper_id: int
    focus_areas: Optional[List[str]] = None


class SummarizeResponse(BaseModel):
    paper_id: int
    summary: str
    key_findings: List[str]
    methodology: Optional[str] = None
    citations: List[str] = []


class QueryRequest(BaseModel):
    query: str
    paper_ids: Optional[List[int]] = None
    top_k: int = 5


class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[Dict[str, Any]]  # List of relevant paper sections
    confidence: float


class RecommendRequest(BaseModel):
    paper_id: int
    based_on: str = "similarity"  # similarity, citations, concepts, experiments
    limit: int = 5


class RecommendResponse(BaseModel):
    paper_id: int
    recommendations: List[Dict[str, Any]]
    reasoning: str

