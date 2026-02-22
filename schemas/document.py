from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DocumentMetadata(BaseModel):
    num_pages: int = Field(..., description="Total number of pages in the PDF", ge=1)
    file_name: str = Field(..., description="Original name of the uploaded file")

class ExtractedEntities(BaseModel):
    policy_holder: Optional[str] = Field(None, description="Name of the primary policyholder")
    premium_amount: Optional[float] = Field(None, description="Total premium amount extracted")
    effective_date: Optional[str] = Field(None, description="Date the policy goes into effect (YYYY-MM-DD)")

class DetectedClause(BaseModel):
    clause_type: str = Field(..., description="Category of the clause (e.g., liability, exclusion)")
    extracted_text: str = Field(..., description="The raw text extracted from the document")
    confidence_score: float = Field(..., description="Model confidence score", ge=0.0, le=1.0)

class ExtractionResult(BaseModel):
    document_metadata: DocumentMetadata
    extracted_entities: ExtractedEntities
    detected_clauses: List[DetectedClause]

class TaskResponse(BaseModel):
    task_id: str = Field(..., description="Unique Celery task identifier")
    status: str = Field(..., description="Current status: pending, processing, completed, or failed")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    result: Optional[ExtractionResult] = None