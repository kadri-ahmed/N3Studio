from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.paper import PaperCreate, PaperResponse, PaperListResponse
from app.services.papers import PaperService

router = APIRouter()


@router.post("/upload", response_model=PaperResponse, status_code=status.HTTP_201_CREATED)
async def upload_paper(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload a research paper (PDF)"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )
    
    paper_service = PaperService(db)
    paper = await paper_service.upload_paper(file)
    return paper


@router.get("", response_model=List[PaperListResponse])
async def list_papers(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all uploaded papers"""
    paper_service = PaperService(db)
    papers = await paper_service.list_papers(skip=skip, limit=limit)
    return papers


@router.get("/{paper_id}", response_model=PaperResponse)
async def get_paper(
    paper_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get paper details"""
    paper_service = PaperService(db)
    paper = await paper_service.get_paper(paper_id)
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found"
        )
    return paper


@router.post("/{paper_id}/process", response_model=PaperResponse)
async def process_paper(
    paper_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Process paper: extract entities, build knowledge graph"""
    paper_service = PaperService(db)
    paper = await paper_service.process_paper(paper_id)
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found"
        )
    return paper

