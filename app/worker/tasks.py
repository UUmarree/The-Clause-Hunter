#python functions that run our ml models in the background using celery
import time
from app.worker.celery_app import celery_task_app
@celery_task_app.task(name="app.worker.tasks.extract_information_task")
def extract_information_task(self,file_path: str,original_filename: str) -> dict:
    """
    Simulates the extraction of information from a document.
    In a real implementation, this would involve processing the file and extracting relevant data.
    """
    # Simulate a time-consuming task
    time.sleep(10)  # Simulate processing time
    print("Finished processing file:", original_filename)
    # Return dummy extracted data
    return {
        "document_metadata": {
            "num_pages": 14,
            "file_name": original_filename
        },
        "extracted_entities": {
            "policy_holder": "Jane Doe",
            "premium_amount": 1450.00,
            "effective_date": "2026-03-01"
        },
        "detected_clauses": [
            {
                "clause_type": "liability_limit",
                "extracted_text": "The maximum bodily injury liability limit is $100,000 per person.",
                "confidence_score": 0.96
            }
        ]
    }