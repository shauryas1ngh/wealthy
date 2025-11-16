from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.prime import (
    PrimeCheckRequest,
    PrimeCheckResponse,
    PrimeCheckHistoryResponse
)
from app.services.prime_service import PrimeService

router = APIRouter(
    prefix="/prime",
    tags=["Prime Number Operations"]
)


@router.post("/check", response_model=PrimeCheckResponse, status_code=201)
async def check_prime(
    request: PrimeCheckRequest,
    db: Session = Depends(get_db)
):
    
    #Check if a number is prime and save the result to the database.
    
    
    # Generate transaction ID
    transaction_id = PrimeService.generate_transaction_id()
    
    # Check if number is prime
    is_prime = PrimeService.is_prime(request.number)
    
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
    
    return PrimeCheckResponse(
        transaction_id=db_record.transaction_id,
        number=db_record.number,
        is_prime=db_record.is_prime,
        message=message,
        created_at=db_record.created_at
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



