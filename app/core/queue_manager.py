import queue
import threading
import time
import uuid
from typing import Dict, Optional, Callable, Any
from datetime import datetime
from enum import Enum


class JobStatus(Enum):
    """Job status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Job:
    #Represents a job in the queue.
    
    def __init__(self, job_id: str, number: int):
        self.job_id = job_id
        self.number = number
        self.status = JobStatus.PENDING
        self.result: Optional[bool] = None
        self.error: Optional[str] = None
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
        self.transaction_id: Optional[str] = None


class QueueManager:
    
    #Manages an in-memory job queue with background worker threads.
    
    
    def __init__(self, num_workers: int = 4):
        self.job_queue: queue.Queue = queue.Queue()
        self.jobs: Dict[str, Job] = {}
        self.jobs_lock = threading.Lock()
        self.num_workers = num_workers
        self.workers = []
        self.running = False
        self.process_job_callback: Optional[Callable] = None
    
    def set_job_processor(self, callback: Callable):
        """
        Set the callback function that processes jobs.
        Callback should accept (job_id, number, db_session) and return (is_prime, transaction_id, error).
        """
        self.process_job_callback = callback
    
    def start(self):
        #Start background worker threads.
        if self.running:
            return
        
        self.running = True
        for i in range(self.num_workers):
            worker = threading.Thread(
                target=self._worker,
                name=f"QueueWorker-{i+1}",
                daemon=True
            )
            worker.start()
            self.workers.append(worker)
        
        print(f"✓ Queue manager started with {self.num_workers} workers")
    
    def stop(self):
        #Stop all worker threads gracefully.
        self.running = False
        
        # Add poison pills to wake up all workers
        for _ in range(self.num_workers):
            self.job_queue.put(None)
        
        # Wait for all workers to finish
        for worker in self.workers:
            worker.join(timeout=5)
        
        self.workers.clear()
        print("✓ Queue manager stopped")
    
    def submit_job(self, number: int) -> str:
        #Submit a new prime checking job to the queue.
        #Returns the job_id immediately.
        job_id = self._generate_job_id()
        job = Job(job_id=job_id, number=number)
        
        with self.jobs_lock:
            self.jobs[job_id] = job
        
        self.job_queue.put(job_id)
        return job_id
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        #Get the status of a job by its ID.
        #Returns None if job doesn't exist.
        with self.jobs_lock:
            job = self.jobs.get(job_id)
            if not job:
                return None
            
            return {
                "job_id": job.job_id,
                "status": job.status.value,
                "number": job.number,
                "is_prime": job.result,
                "transaction_id": job.transaction_id,
                "error": job.error,
                "created_at": job.created_at,
                "completed_at": job.completed_at
            }
    
    def _worker(self):
        #Worker thread that processes jobs from the queue.
        print(f"Worker {threading.current_thread().name} started")
        
        while self.running:
            try:
                # Get job from queue with timeout
                job_id = self.job_queue.get(timeout=1)
                
                # Poison pill check
                if job_id is None:
                    break
                
                self._process_job(job_id)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Worker error: {e}")
    
    def _process_job(self, job_id: str):
        #Process a single job.
        with self.jobs_lock:
            job = self.jobs.get(job_id)
            if not job:
                return
            job.status = JobStatus.PROCESSING
        
        try:
            # Call the job processor callback
            if self.process_job_callback:
                is_prime, transaction_id, error = self.process_job_callback(job_id, job.number)
                
                with self.jobs_lock:
                    if error:
                        job.status = JobStatus.FAILED
                        job.error = error
                    else:
                        job.status = JobStatus.COMPLETED
                        job.result = is_prime
                        job.transaction_id = transaction_id
                    job.completed_at = datetime.now()
            else:
                with self.jobs_lock:
                    job.status = JobStatus.FAILED
                    job.error = "No job processor configured"
                    job.completed_at = datetime.now()
        
        except Exception as e:
            with self.jobs_lock:
                job.status = JobStatus.FAILED
                job.error = str(e)
                job.completed_at = datetime.now()
    
    def _generate_job_id(self) -> str:
        """Generate a unique job ID."""
        return f"JOB-{int(time.time() * 1000)}-{uuid.uuid4().hex[:8].upper()}"
    
    def cleanup_old_jobs(self, max_age_seconds: int = 3600):
        """Remove jobs older than max_age_seconds from memory."""
        cutoff_time = datetime.now().timestamp() - max_age_seconds
        
        with self.jobs_lock:
            jobs_to_remove = [
                job_id for job_id, job in self.jobs.items()
                if job.created_at.timestamp() < cutoff_time
            ]
            
            for job_id in jobs_to_remove:
                del self.jobs[job_id]
        
        if jobs_to_remove:
            print(f"Cleaned up {len(jobs_to_remove)} old jobs")


# Global queue manager instance
queue_manager = QueueManager()

