from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from backend.services.query_generator import generate_query_list
from backend.services.search_engine import search_web
from backend.services.bulk_search import bulk_search_questions
from backend.services.parser import load_search_results
from backend.services.rag_pipeline import build_faiss_index
from backend.services.report_generator import create_report_from_json
from backend.services.rag_qa import answer_with_rag

app = FastAPI()

# Allow frontend to connect (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set specific frontend origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate-queries/")
def get_queries(company: str = Query(..., description="Company name")):
    queries = generate_query_list(company)
    return {"company": company, "queries": queries}

@app.get("/search/")
def run_search(query: str):
    try:
        results = search_web(query)
        return {"query": query, "results": results}
    except Exception as e:
        return {"error": str(e)}

class BulkSearchRequest(BaseModel):
    company: str
    questions: list

@app.post("/search-all/")
def search_all_questions(payload: BulkSearchRequest):
    try:
        path = bulk_search_questions(payload.company, payload.questions)
        return {"status": "success", "filepath": path}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    

@app.get("/load-results/")
def get_search_results(filepath: str):
    try:
        docs = load_search_results(filepath)
        return {"status": "success", "docs": docs}
    except Exception as e:
        return {"status": "error", "error": str(e)}


class RAGBuildRequest(BaseModel):
    company: str
    filepath: str

@app.post("/build-rag/")
def build_rag_index(payload: RAGBuildRequest):
    try:
        path = build_faiss_index(payload.company, payload.filepath)
        return {"status": "success", "index_path": path}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    

@app.get("/generate-report/")
def generate_company_report(filepath: str):
    try:
        report = create_report_from_json(filepath)
        return {"status": "success", "report": report}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.post("/ask/")
def ask_rag(company: str = Body(...), question: str = Body(...)):
    try:
        answer = answer_with_rag(company, question)
        return {"status": "success", "answer": answer}
    except Exception as e:
        return {"status": "error", "error": str(e)}
