from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PaperBase(BaseModel):
    title: str
    authors: Optional[str] = None
    abstract: Optional[str] = None


class PaperCreate(PaperBase):
    pass


class PaperResponse(PaperBase):
    id: int
    filename: str
    file_path: str
    upload_date: datetime
    processed: bool
    processing_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PaperListResponse(BaseModel):
    id: int
    title: str
    authors: Optional[str] = None
    upload_date: datetime
    processed: bool
    
    class Config:
        from_attributes = True

