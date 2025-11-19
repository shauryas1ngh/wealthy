from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db, SessionLocal
from app.core.queue_manager import queue_manager
from app.api.routes import prime
from app.services.prime_service import PrimeService


def process_prime_job(job_id: str, number: int):
    """
    Job processor callback for the queue manager.
    Processes prime checking jobs with database persistence.
    Returns: (is_prime, transaction_id, error)
    """
    db = SessionLocal()
    try:
        # Generate transaction ID
        transaction_id = PrimeService.generate_transaction_id()
        
        # Check if number is prime (with caching and optimization)
        is_prime, was_cached = PrimeService.check_prime_with_cache(db, number)
        
        # Save to database
        PrimeService.create_prime_check(
            db=db,
            number=number,
            transaction_id=transaction_id,
            is_prime=is_prime
        )
        
        return is_prime, transaction_id, None
        
    except Exception as e:
        return None, None, str(e)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup: Initialize database tables
    print("🚀 Starting up application...")
    print(f"📊 Initializing database at {settings.DATABASE_URL}")
    init_db()
    print("✓ Database initialized successfully")
    
    # Initialize queue manager
    print(f"🔧 Initializing queue manager with {settings.QUEUE_WORKERS} workers...")
    queue_manager.num_workers = settings.QUEUE_WORKERS
    queue_manager.set_job_processor(process_prime_job)
    queue_manager.start()
    print("✓ Queue manager initialized successfully")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down application...")
    queue_manager.stop()
    print("✓ Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "A REST API service that checks if a number is prime, "
        "assigns a unique transaction ID to each request, "
        "and persists the data to PostgreSQL."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# Include routers
app.include_router(prime.router, prefix="/api/v1")


@app.get("/", tags=["Health Check"])
async def root():
    """Root endpoint - health check."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "database": "connected"
    }

