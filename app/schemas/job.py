from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class JobSubmitResponse(BaseModel):
    #Response schema when submitting an async job.
    
    job_id: str = Field(..., description="Unique job identifier for tracking")
    status: str = Field(..., description="Initial job status (pending)")
    message: str = Field(..., description="Human-readable message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "JOB-1700000000000-ABC123",
                "status": "pending",
                "message": "Job submitted successfully. Use job_id to check status."
            }
        }


class JobStatusResponse(BaseModel):
    #Response schema for job status queries.
    
    job_id: str = Field(..., description="Unique job identifier")
    status: str = Field(..., description="Current job status: pending, processing, completed, or failed")
    number: int = Field(..., description="The number being checked")
    is_prime: Optional[bool] = Field(None, description="Whether the number is prime (available when completed)")
    transaction_id: Optional[str] = Field(None, description="Transaction ID from database (available when completed)")
    error: Optional[str] = Field(None, description="Error message if job failed")
    created_at: datetime = Field(..., description="When the job was created")
    completed_at: Optional[datetime] = Field(None, description="When the job completed")
    message: Optional[str] = Field(None, description="Human-readable status message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "JOB-1700000000000-ABC123",
                "status": "completed",
                "number": 17,
                "is_prime": True,
                "transaction_id": "TXN-1700000000000-XYZ789",
                "error": None,
                "created_at": "2024-11-17T12:00:00Z",
                "completed_at": "2024-11-17T12:00:01Z",
                "message": "17 is a prime number"
            }
        }

