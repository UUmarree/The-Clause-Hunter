# 🕵️‍♂️ The Clause Hunter

An asynchronous, scalable Machine Learning API designed to extract critical entities and liability clauses from unstructured insurance and legal PDF documents.



## 🏗️ System Architecture

This project implements an enterprise-grade asynchronous polling architecture to prevent heavy Machine Learning workloads from blocking the main web server thread.

1. **Ingestion (FastAPI):** Validates incoming PDFs via Pydantic and assigns a unique `task_id`.
2. **Message Broker (Redis/Docker):** Acts as the intermediary, holding the task payload.
3. **Background Worker (Celery):** Picks up the task, parses the document using `PyMuPDF`, and runs the ML inference wrapper.
4. **Retrieval:** The client polls the API with their `task_id` to retrieve the final structured JSON extraction.

## 🛠️ Tech Stack

* **Web Framework:** FastAPI, Pydantic, Uvicorn
* **Task Queue & Broker:** Celery, Redis (Dockerized)
* **ML & Processing:** PyMuPDF (`fitz`), Python `re` (Regex heuristic proxy for NLP models)
* **Environment:** Python 3.10+, Virtualenv

## 🚀 Local Setup & Installation (Windows)

**1. Clone the repository and set up the environment**
```bash
git clone [https://github.com/yourusername/the-clause-hunter.git](https://github.com/yourusername/the-clause-hunter.git)
cd "The Clause Hunter"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt