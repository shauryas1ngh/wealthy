import uuid
import time
from typing import List
from sqlalchemy.orm import Session
from app.models.prime_check import PrimeCheckRequest as DBPrimeCheckRequest


class PrimeService:
    #Service class containing business logic for prime number operations.
    
    @staticmethod
    def generate_transaction_id() -> str:
        
        timestamp = int(time.time() * 1000)  # milliseconds
        unique_id = uuid.uuid4().hex[:8].upper()
        return f"TXN-{timestamp}-{unique_id}"
    
    @staticmethod
    def is_prime(n: int) -> bool:
        
        
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        
        return True
    
    @staticmethod
    def create_prime_check(db: Session, number: int, transaction_id: str, is_prime: bool) -> DBPrimeCheckRequest:
        # SAVes db record to the database.
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
        
        return db.query(DBPrimeCheckRequest).filter(
            DBPrimeCheckRequest.transaction_id == transaction_id
        ).first()
    
    