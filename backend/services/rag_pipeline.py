import os
import uuid
from typing import List
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.services.parser import load_search_results

def build_faiss_index(
    company: str,
    filepath: str,
    save_dir="embeddings/faiss_index/",
    chunk_size=500,
    chunk_overlap=50,
    embedding_model_name="sentence-transformers/all-MiniLM-L6-v2"
):
    # Step 1: Load parsed docs
    parsed_docs = load_search_results(filepath)
    
    # Step 2: Chunk each content block
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    documents = []
    for doc in parsed_docs:
        chunks = text_splitter.split_text(doc["content"])
        for chunk in chunks:
            documents.append(Document(
                page_content=chunk,
                metadata={
                    "company": company,
                    "question": doc["question"],
                    "qid": doc["metadata"]["question_id"]
                }
            ))

    print(f"Total Chunks Created: {len(documents)}")

    # Step 3: Embed chunks
    embedder = HuggingFaceEmbeddings(model_name=embedding_model_name)

    # Step 4: Build FAISS index
    vectorstore = FAISS.from_documents(documents, embedder)

    # Step 5: Save index
    os.makedirs(save_dir, exist_ok=True)
    index_path = os.path.join(save_dir, f"{company.replace(' ', '_')}_faiss_index")
    vectorstore.save_local(index_path)

    print(f"FAISS index saved to: {index_path}")
    return index_path