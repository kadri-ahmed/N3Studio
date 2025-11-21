from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from datetime import datetime
import os
import aiofiles
from pathlib import Path
from typing import List

from app.core.config import settings
from app.schemas.paper import PaperResponse, PaperListResponse


class PaperService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)
    
    async def upload_paper(self, file: UploadFile) -> PaperResponse:
        """Upload and save a paper file"""
        # Save file
        file_path = self.upload_dir / file.filename
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # TODO: Extract metadata from PDF (title, authors, abstract)
        # For now, use filename as title
        paper_data = {
            "title": file.filename.replace('.pdf', ''),
            "filename": file.filename,
            "file_path": str(file_path),
            "upload_date": datetime.utcnow(),
            "processed": False
        }
        
        # TODO: Save to database
        # For now, return mock data
        return PaperResponse(
            id=1,
            **paper_data
        )
    
    async def list_papers(self, skip: int = 0, limit: int = 100) -> List[PaperListResponse]:
        """List all papers"""
        # TODO: Query database
        return []
    
    async def get_paper(self, paper_id: int) -> PaperResponse:
        """Get paper by ID"""
        # TODO: Query database
        return None
    
    async def process_paper(self, paper_id: int) -> PaperResponse:
        """Process paper: extract text, entities, build graph"""
        # TODO: Implement paper processing
        # 1. Extract text from PDF
        # 2. Use LlamaIndex to chunk and embed
        # 3. Extract entities using NER
        # 4. Build knowledge graph in FalkorDB
        # 5. Update paper status
        return None

