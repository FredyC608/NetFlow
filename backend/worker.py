import os
import time
from celery import Celery
import netflow_crypto  # The C++ module

# 1. Configuration
BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://broker:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://broker:6379/0")

celery_app = Celery(
    "netflow_worker",
    broker=BROKER_URL,
    backend=BACKEND_URL
)

# 2. The Real Task Logic
@celery_app.task(name="ocr_task")
def ocr_task(file_path: str, key: str):
    """
    1. Read encrypted file from shared volume.
    2. Decrypt using C++ module (in memory).
    3. (Future) Pass decrypted bytes to OCR.
    """
    try:
        # Step A: Validate file exists
        if not os.path.exists(file_path):
            return {"status": "error", "message": "File not found"}

        # Step B: Read Encrypted Bytes
        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        # Step C: C++ Decryption (CPU Intensive)
        # This runs inside the Worker Container
        print(f"Decrypting {file_path} using C++ extension...")
        start_time = time.time()
        
        # Call the C++ function
        decrypted_bytes = netflow_crypto.decrypt(encrypted_data, key)
        
        duration = time.time() - start_time

        # Step D: (Temporary) Return stats
        # In the next phase, we will pass 'decrypted_bytes' to Tesseract
        return {
            "status": "success",
            "original_file": file_path,
            "decryption_time_sec": duration,
            "decrypted_size": len(decrypted_bytes),
            # WARNING: Don't return the full text in Redis if it's huge. 
            # Just return a snippet or store it in DB.
            "preview": str(decrypted_bytes[:50]) 
        }

    except Exception as e:
        return {"status": "failure", "error": str(e)}