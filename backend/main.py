from fastapi import FastAPI
from worker import ocr_task  # We will import the task from Service 2
from celery.result import AsyncResult
from fastapi import UploadFile
import wealthguard_crypto  # Import our compiled C++ module

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "WealthGuard API is running"}

@app.post("/upload")
async def upload_document(file: UploadFile, key: str = "secret_key"):
    # Read the file content (Simulating encrypted blob)
    encrypted_blob = await file.read()
    
    # Pass to C++ for memory-safe decryption
    # In a real scenario, this 'decrypted_data' stays in memory, never written to disk
    decrypted_bytes = wealthguard_crypto.decrypt(encrypted_blob, key)
    
    # Send the raw bytes (or path) to Celery
    # For now, we just verify it worked
    return {
        "filename": file.filename, 
        "message": "Decryption successful via C++",
        "size_bytes": len(decrypted_bytes)
    }

@app.get("/status/{task_id}")
def get_status(task_id: str):
    # Check Redis for the result
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }