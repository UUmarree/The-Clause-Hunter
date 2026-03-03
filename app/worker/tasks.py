import os
from app.worker.celery_app import celery_task_app

# Import our instantiated ML model
from ml_pipeline.inference import inference_engine

@celery_task_app.task(bind=True, name="extract_document_task")
def extract_document_task(self, file_path: str, original_filename: str):
    """
    Executes the machine learning pipeline on the uploaded document.
    """
    print(f"📥 Worker received file: {original_filename}")
    
    try:
        # Pass the file to the ML pipeline
        print("🧠 Running ML Inference...")
        extraction_results = inference_engine.predict(file_path, original_filename)
        
        # MLOps Cleanup: Delete the temporary PDF from the server so we don't run out of disk space!
        if os.path.exists(file_path):
            os.remove(file_path)
            
        print("✅ Extraction complete!")
        return extraction_results
        
    except Exception as e:
        print(f"❌ ML Pipeline failed: {str(e)}")
        # If it fails, raise the exception so Celery marks the task as 'FAILURE'
        raise e