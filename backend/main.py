from fastapi import FastAPI
from worker import ocr_task  # We will import the task from Service 2
from celery.result import AsyncResult

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "WealthGuard API is running"}

@app.post("/upload")
def upload_document(filename: str):
    # This sends a message to Redis. The Worker picks it up.
    task = ocr_task.delay(filename)
    return {"task_id": task.id, "message": "File sent to OCR worker"}

@app.get("/status/{task_id}")
def get_status(task_id: str):
    # Check Redis for the result
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }