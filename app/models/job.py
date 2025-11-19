from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class PrimeCheckJob(Base):
    """Model to store async prime check job history."""
    
    __tablename__ = "prime_check_jobs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column(String, unique=True, index=True, nullable=False)
    transaction_id = Column(String, index=True, nullable=True)
    number = Column(Integer, nullable=False, index=True)
    is_prime = Column(Boolean, nullable=True)
    status = Column(String, nullable=False, default="pending")  # pending, processing, completed, failed
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<PrimeCheckJob(job_id={self.job_id}, number={self.number}, status={self.status})>"

