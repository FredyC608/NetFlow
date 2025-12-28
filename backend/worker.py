import os
import time
from celery import Celery

# Get Redis URL from docker-compose environment variables
BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Initialize the Celery App
celery_app = Celery(
    "wealthguard_worker",
    broker=BROKER_URL,
    backend=BACKEND_URL
)

@celery_app.task(name="ocr_task")
def ocr_task(filename: str):
    """
    Simulate a heavy OCR process.
    In Cycle 1, we just sleep for 5 seconds to pretend we are working.
    In Cycle 2, we will add Tesseract code here.
    """
    print(f"Starting OCR on {filename}...")
    time.sleep(5)  # Simulate processing time
    return {"filename": filename, "text_extracted": "Sample bank statement text..."}
  
  