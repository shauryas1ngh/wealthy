from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PrimeCheckRequest(BaseModel):
    #Request schema for prime number checking.This is the request body for the prime check endpoint.
    
    number: int = Field(..., description="The number to check if it's prime", example=17)
    
    class Config:
        json_schema_extra = {
            "example": {
                "number": 17
            }
        }


class PrimeCheckResponse(BaseModel):
    #Response schema for prime number checking.
    
    transaction_id: str = Field(..., description="Unique transaction identifier")
    number: int = Field(..., description="The number that was checked")
    is_prime: bool = Field(..., description="Whether the number is prime or not")
    message: str = Field(..., description="Message about the result")
    created_at: datetime = Field(..., description="Timestamp of the request")
    
    class Config:
        from_attributes = True


