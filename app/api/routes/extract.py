from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.schemas.document import TaskResponse
import uuid
from celery.result import AsyncResult
from app.worker.celery_app import celery_task_app
from app.worker.tasks import extract_information_task
import os
import shutil

router = APIRouter()
#create temp directory for uploaded files
UPLOAD_DIR = "temp_uploads"
# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/extract", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
async def extract_information(file: UploadFile = File(...)):
    """
    Endpoint to upload a document and start the extraction process.
    """
    try:
        #1. Validate file type
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Only PDF files are allowed.")
        
        #2. Validate file is not empty
        if not file.filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File must have a valid filename.")
        
        #3. Generate a unique file path
        file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
        
        #4. Save file to disk with error handling
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except IOError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to save file: {str(e)}")
        
        #5. Dispatch the extraction task to Celery
        task = extract_information_task.delay(file_path)

        return TaskResponse(
            task_id=task.id,
            status="processing",
            message="File received and extraction process started. Check back using the task ID for results.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")

@router.get("/extract/{task_id}", response_model=TaskResponse)
async def get_extraction_result(task_id: str):
    """
    Endpoint to check the status of the extraction process and retrieve results.
    """
    ##1. Ask redis for current status of specified task
    task_result = AsyncResult(task_id, app=celery_task_app)
    if task_result.state == "PENDING":
        return TaskResponse(task_id=task_id, status="pending", message="Task is still pending.")
    elif task_result.state == "PROGRESS":
        return TaskResponse(task_id=task_id, status="processing", message="Task is currently being processed.")
    elif task_result.state == "SUCCESS":
        # In a real implementation, you would return the actual extracted data here.
        return TaskResponse(task_id=task_id, status="completed", message="Task completed successfully. Extracted data is ready.")
    elif task_result.state == "FAILURE":
        return TaskResponse(task_id=task_id, status="failed", message="Task failed during processing.")
    else:
        return TaskResponse(task_id=task_id, status=task_result.state.lower(), message=f"Task is in {task_result.state} state.")