from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.schemas.document import TaskResponse
import uuid

router = APIRouter()
@router.post("/extract", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
async def extract_information(file: UploadFile = File(...)):
    """
    Endpoint to upload a document and start the extraction process.
    """
    #1. Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Only PDF files are allowed.")
    #2. Generate a unique task ID
    task_id = str(uuid.uuid4())
    #3. Save the file to a temporary location (for demonstration, we won't actually save it)
    return TaskResponse(
        task_id=task_id,
        status="processing",
        message="File received and extraction process started. Check back using the task ID for results.",
    )

@router.get("/extract/{task_id}", response_model=TaskResponse)
async def get_extraction_result(task_id: str):
    """
    Endpoint to check the status of the extraction process and retrieve results.
    """
    # For demonstration, we'll return a dummy response. 
    return TaskResponse(
        task_id=task_id,
        status="completed",
       
    )