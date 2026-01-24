import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from celery.result import AsyncResult
from worker import ocr_task, celery_app  # Importing the Celery task signature
app = FastAPI()

# Ensure we have a shared directory to store uploads
UPLOAD_DIR = "/app/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def health_check():
    return {"status": "NetFlow API is running"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...), key: str = "secret_key"):
    """
    1. Receive the encrypted file stream.
    2. Save it to disk (Shared Volume).
    3. Offload the processing to Celery.
    4. Return a Task ID immediately.
    """
    try:
        # Generate a unique filename to prevent collisions
        file_id = str(uuid.uuid4())
        # Preserve the extension or use .enc
        filename = f"{file_id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # 1. Write the uploaded file to the shared volume
        # In production, use aiofiles for non-blocking I/O, but this is fine for MVP
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Dispatch the task to Celery (Redis)
        # We pass the PATH, not the bytes. Redis cannot handle large blobs efficiently.
        task = ocr_task.delay(file_path, key)

        return {
            "message": "File uploaded and processing started.",
            "task_id": task.id,
            "file_id": file_id,
            "status_check_url": f"/status/{task.id}"
        }

    except Exception as e:
        # Clean up file if dispatch failed
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{task_id}")
def get_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    
    response = {
        "task_id": task_id,
        "status": task_result.status,
    }

    # If the task finished successfully, include the result
    if task_result.status == "SUCCESS":
        response["result"] = task_result.result
    # If it failed, include the error
    elif task_result.status == "FAILURE":
        response["error"] = str(task_result.result)

    return response