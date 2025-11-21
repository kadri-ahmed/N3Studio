from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import UploadFile
from datetime import datetime
import os
import aiofiles
from pathlib import Path
from typing import List, Optional

from app.core.config import settings
from app.core.falkordb import get_falkordb
from app.models.paper import Paper
from app.schemas.paper import PaperResponse, PaperListResponse
from app.services.graph import GraphService


class PaperService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)
        self.graph_service = GraphService(get_falkordb())
    
    async def upload_paper(self, file: UploadFile) -> PaperResponse:
        """Upload and save a paper file, then create node in graph"""
        # Save file
        file_path = self.upload_dir / file.filename
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Extract basic metadata from filename
        title = file.filename.replace('.pdf', '').replace('_', ' ').title()
        
        # Create paper record in database
        paper = Paper(
            title=title,
            filename=file.filename,
            file_path=str(file_path),
            upload_date=datetime.utcnow(),
            processed=False
        )
        
        self.db.add(paper)
        await self.db.commit()
        await self.db.refresh(paper)
        
        # Create Paper node in FalkorDB graph
        try:
            graph_node_id = self.graph_service.create_paper_node(
                paper_id=paper.id,
                title=paper.title,
                authors=paper.authors,
                abstract=paper.abstract,
                filename=paper.filename
            )
            
            # Update paper with graph node ID
            paper.graph_node_id = graph_node_id
            await self.db.commit()
            await self.db.refresh(paper)
        except Exception as e:
            # Log error but don't fail the upload
            print(f"Error creating graph node: {e}")
        
        return PaperResponse(
            id=paper.id,
            title=paper.title,
            authors=paper.authors,
            abstract=paper.abstract,
            filename=paper.filename,
            file_path=paper.file_path,
            upload_date=paper.upload_date,
            processed=paper.processed,
            processing_date=paper.processing_date
        )
    
    async def list_papers(self, skip: int = 0, limit: int = 100) -> List[PaperListResponse]:
        """List all papers"""
        result = await self.db.execute(
            select(Paper)
            .order_by(Paper.upload_date.desc())
            .offset(skip)
            .limit(limit)
        )
        papers = result.scalars().all()
        
        return [
            PaperListResponse(
                id=paper.id,
                title=paper.title,
                authors=paper.authors,
                upload_date=paper.upload_date,
                processed=paper.processed
            )
            for paper in papers
        ]
    
    async def get_paper(self, paper_id: int) -> Optional[PaperResponse]:
        """Get paper by ID"""
        result = await self.db.execute(
            select(Paper).where(Paper.id == paper_id)
        )
        paper = result.scalar_one_or_none()
        
        if not paper:
            return None
        
        return PaperResponse(
            id=paper.id,
            title=paper.title,
            authors=paper.authors,
            abstract=paper.abstract,
            filename=paper.filename,
            file_path=paper.file_path,
            upload_date=paper.upload_date,
            processed=paper.processed,
            processing_date=paper.processing_date
        )
    
    async def process_paper(self, paper_id: int) -> PaperResponse:
        """Process paper: extract text, entities, build graph"""
        # TODO: Implement paper processing
        # 1. Extract text from PDF
        # 2. Use LlamaIndex to chunk and embed
        # 3. Extract entities using NER
        # 4. Build knowledge graph in FalkorDB
        # 5. Update paper status
        return None

