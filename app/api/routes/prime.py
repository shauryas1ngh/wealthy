from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db, SessionLocal
from app.schemas.prime import (
    PrimeCheckRequest,
    PrimeCheckResponse
    
)
from app.schemas.job import (
    JobSubmitResponse,
    JobStatusResponse
)
from app.services.prime_service import PrimeService
from app.core.queue_manager import queue_manager

router = APIRouter(
    prefix="/prime",
    tags=["Prime Number Operations"]
)


@router.post("/check", response_model=PrimeCheckResponse, status_code=201)
async def check_prime(
    request: PrimeCheckRequest,
    db: Session = Depends(get_db)
):
    
    #Check if a number is prime (synchronous).
    
    
    # Generate transaction ID
    transaction_id = PrimeService.generate_transaction_id()
    
    # Check if number is prime (with caching and optimization)
    is_prime, was_cached = PrimeService.check_prime_with_cache(db, request.number)
    
    # Save to database
    db_record = PrimeService.create_prime_check(
        db=db,
        number=request.number,
        transaction_id=transaction_id,
        is_prime=is_prime
    )
    
    # Prepare response message
    if is_prime:
        message = f"{request.number} is a prime number"
    else:
        message = f"{request.number} is not a prime number"
    
    if was_cached:
        message += " (cached result)"
    
    return PrimeCheckResponse(
        transaction_id=db_record.transaction_id,
        number=db_record.number,
        is_prime=db_record.is_prime,
        message=message,
        created_at=db_record.created_at
    )


@router.post("/check/async", response_model=JobSubmitResponse, status_code=202)
async def check_prime_async(
    request: PrimeCheckRequest
):
    
    #Submit a prime check job asynchronously .
    #3Returns immediately with a job_id that can be used to check status.
    
    
    
    # Submit job to queue
    job_id = queue_manager.submit_job(request.number)
    
    return JobSubmitResponse(
        job_id=job_id,
        status="pending",
        message=f"Job submitted successfully. Use job_id to check status at /api/v1/prime/job/{job_id}"
    )


@router.get("/job/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """
    Get the status of an async prime check job.
    
    - **job_id**: The unique job identifier returned from /check/async
    - Returns job status: pending, processing, completed, or failed
    """
    job_status = queue_manager.get_job_status(job_id)
    
    if not job_status:
        raise HTTPException(
            status_code=404,
            detail=f"Job ID '{job_id}' not found"
        )
    
    # Prepare message based on status
    if job_status["status"] == "completed":
        if job_status["is_prime"]:
            message = f"{job_status['number']} is a prime number"
        else:
            message = f"{job_status['number']} is not a prime number"
    elif job_status["status"] == "failed":
        message = f"Job failed: {job_status.get('error', 'Unknown error')}"
    elif job_status["status"] == "processing":
        message = "Job is currently being processed"
    else:
        message = "Job is pending in queue"
    
    return JobStatusResponse(
        job_id=job_status["job_id"],
        status=job_status["status"],
        number=job_status["number"],
        is_prime=job_status.get("is_prime"),
        transaction_id=job_status.get("transaction_id"),
        error=job_status.get("error"),
        created_at=job_status["created_at"],
        completed_at=job_status.get("completed_at"),
        message=message
    )


@router.get("/check/{transaction_id}", response_model=PrimeCheckResponse)
async def get_check_by_transaction(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve a prime check result by transaction ID.
    
    - **transaction_id**: The unique transaction identifier
    """
    db_record = PrimeService.get_by_transaction_id(db=db, transaction_id=transaction_id)
    
    if not db_record:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction ID '{transaction_id}' not found"
        )
    
    # Prepare response message
    if db_record.is_prime:
        message = f"{db_record.number} is a prime number"
    else:
        message = f"{db_record.number} is not a prime number"
    
    return PrimeCheckResponse(
        transaction_id=db_record.transaction_id,
        number=db_record.number,
        is_prime=db_record.is_prime,
        message=message,
        created_at=db_record.created_at
    )



