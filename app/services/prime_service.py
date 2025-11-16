"""Service layer for prime number checking logic."""

import uuid
import time
from typing import List
from sqlalchemy.orm import Session
from app.models.prime_check import PrimeCheckRequest as DBPrimeCheckRequest


class PrimeService:
    """Service class containing business logic for prime number operations."""
    
    @staticmethod
    def generate_transaction_id() -> str:
        """
        Generate a unique transaction ID.
        
        Returns:
            str: A unique transaction identifier
        """
        timestamp = int(time.time() * 1000)  # milliseconds
        unique_id = uuid.uuid4().hex[:8].upper()
        return f"TXN-{timestamp}-{unique_id}"
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """
        Check if a number is prime.
        
        Args:
            n: The number to check
            
        Returns:
            bool: True if the number is prime, False otherwise
        """
        # Handle edge cases
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        # Check odd divisors up to sqrt(n)
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        
        return True
    
    @staticmethod
    def create_prime_check(db: Session, number: int, transaction_id: str, is_prime: bool) -> DBPrimeCheckRequest:
        """
        Save a prime check request to the database.
        
        Args:
            db: Database session
            number: The number that was checked
            transaction_id: Unique transaction identifier
            is_prime: Whether the number is prime
            
        Returns:
            DBPrimeCheckRequest: The created database record
        """
        db_record = DBPrimeCheckRequest(
            transaction_id=transaction_id,
            number=number,
            is_prime=is_prime
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    
    @staticmethod
    def get_by_transaction_id(db: Session, transaction_id: str) -> DBPrimeCheckRequest | None:
        """
        Retrieve a prime check request by transaction ID.
        
        Args:
            db: Database session
            transaction_id: The transaction ID to search for
            
        Returns:
            DBPrimeCheckRequest or None: The database record if found
        """
        return db.query(DBPrimeCheckRequest).filter(
            DBPrimeCheckRequest.transaction_id == transaction_id
        ).first()
    
    @staticmethod
    def get_all_checks(db: Session, skip: int = 0, limit: int = 100) -> List[DBPrimeCheckRequest]:
        """
        Retrieve all prime check requests with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[DBPrimeCheckRequest]: List of database records
        """
        return db.query(DBPrimeCheckRequest).order_by(
            DBPrimeCheckRequest.created_at.desc()
        ).offset(skip).limit(limit).all()

