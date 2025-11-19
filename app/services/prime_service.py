import uuid
import time
from typing import List, Optional, Tuple
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
    def get_by_number(db: Session, number: int) -> Optional[DBPrimeCheckRequest]:
        """
        Retrieve a prime check result by number.
        Returns the most recent check for this number.
        """
        return db.query(DBPrimeCheckRequest).filter(
            DBPrimeCheckRequest.number == number
        ).order_by(DBPrimeCheckRequest.created_at.desc()).first()
    
    @staticmethod
    def check_prime_with_cache(db: Session, number: int) -> Tuple[bool, bool]:
        #Check if a number is prime, using database cache if available.
        #3Check if a number is prime, using database cache if available.
        #Returns: (is_prime, was_cached)
        
        # First, check if we've seen this number before
        cached_result = PrimeService.get_by_number(db, number)
        
        if cached_result:
            # Cache hit! Return the stored result
            return cached_result.is_prime, True
        
        # Cache miss - calculate it with optimization
        is_prime = PrimeService.is_prime_optimized(db, number)
        return is_prime, False
    
    @staticmethod
    def get_known_primes_up_to(db: Session, limit: int) -> List[int]:
        #Get all known prime numbers up to a limit from database.
        results = db.query(DBPrimeCheckRequest.number).filter(
            DBPrimeCheckRequest.is_prime == True,
            DBPrimeCheckRequest.number <= limit,
            DBPrimeCheckRequest.number >= 2
        ).order_by(DBPrimeCheckRequest.number).distinct().all()
        
        return [r[0] for r in results]
    
    @staticmethod
    def is_prime_optimized(db: Session, n: int) -> bool:
        """
        Optimized prime check using known primes from database for trial division.
        Falls back to standard algorithm if no primes in database or for small numbers.
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        # For smaller numbers, use standard algorithm (faster than DB query)
        if n < 1000:
            return PrimeService.is_prime(n)
        
        # Get known primes up to sqrt(n) from database
        limit = int(n ** 0.5) + 1
        known_primes = PrimeService.get_known_primes_up_to(db, limit)
        
        if known_primes and len(known_primes) > 10:
            # Use known primes as trial divisors (faster than checking all odd numbers)
            for prime in known_primes:
                if prime * prime > n:
                    break
                if n % prime == 0:
                    return False
            
            # Continue checking from where known primes end
            start = known_primes[-1] + 2 if known_primes[-1] < limit else limit + 1
        else:
            # Not enough primes in database, use standard algorithm
            start = 3
        
        # Check remaining candidates
        i = start
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
    def get_by_transaction_id(db: Session, transaction_id: str) -> Optional[DBPrimeCheckRequest]:
        
        return db.query(DBPrimeCheckRequest).filter(
            DBPrimeCheckRequest.transaction_id == transaction_id
        ).first()
    