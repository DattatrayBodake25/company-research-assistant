import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from google.generativeai import GenerativeModel
from dotenv import load_dotenv

load_dotenv()
model = GenerativeModel("models/gemini-2.0-flash")

def answer_with_rag(company: str, question: str, index_dir="embeddings/faiss_index", k: int = 5) -> str:
    index_path = os.path.join(index_dir, f"{company.replace(' ', '_')}_faiss_index")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    docs = vectorstore.similarity_search(question, k=k)
    context = "\n\n".join([doc.page_content for doc in docs])


    prompt = f"""
You are a strict and factual company research assistant.

Use only the information provided in the context below to answer the user's question. Do not guess, assume, or fabricate any details. If the context does not contain enough information to answer the question, respond with:
"Sorry, there is not enough information available to answer this question based on the provided company research."

Instructions:
- Be accurate, concise, and specific.
- Avoid repetition or generic statements.
- Do not use outside knowledge or hallucinate facts.

Context:
{context}

Question:
{question}

Answer:
"""

    response = model.generate_content(prompt)
    return response.text.strip()