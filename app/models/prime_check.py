from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class PrimeCheckRequest(Base):
    #Model to store prime number check requests and results.
    
    __tablename__ = "prime_check_requests"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transaction_id = Column(String, unique=True, index=True, nullable=False)
    number = Column(Integer, nullable=False, index=True)
    is_prime = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<PrimeCheckRequest(transaction_id={self.transaction_id}, number={self.number}, is_prime={self.is_prime})>"

