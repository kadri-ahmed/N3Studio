from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.rag import SummarizeRequest, SummarizeResponse, QueryRequest, QueryResponse, RecommendRequest, RecommendResponse
from app.services.rag import RAGService

router = APIRouter()


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_paper(
    request: SummarizeRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate summary for a paper using RAG"""
    rag_service = RAGService(db)
    summary = await rag_service.summarize_paper(
        paper_id=request.paper_id,
        focus_areas=request.focus_areas
    )
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found or not processed"
        )
    return summary


@router.post("/query", response_model=QueryResponse)
async def query_papers(
    request: QueryRequest,
    db: AsyncSession = Depends(get_db)
):
    """Query papers using RAG"""
    rag_service = RAGService(db)
    result = await rag_service.query_papers(
        query=request.query,
        paper_ids=request.paper_ids,
        top_k=request.top_k
    )
    return result


@router.post("/recommend", response_model=RecommendResponse)
async def recommend_papers(
    request: RecommendRequest,
    db: AsyncSession = Depends(get_db)
):
    """Get recommendations based on knowledge graph"""
    rag_service = RAGService(db)
    recommendations = await rag_service.recommend_papers(
        paper_id=request.paper_id,
        based_on=request.based_on,
        limit=request.limit
    )
    if not recommendations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found"
        )
    return recommendations

