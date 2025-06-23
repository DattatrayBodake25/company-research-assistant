import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# Load Gemini API key from .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini model setup
model = genai.GenerativeModel("models/gemini-2.0-flash")

def generate_query_list(company_name: str) -> list:
    prompt = f"""
    You are a company research assistant.
    Your task is to generate a detailed list of 12–15 insightful research questions for building a comprehensive company profile **only if** the input '{company_name}' refers to a **real, registered company** (e.g., Tech Mahindra, Infosys, Apple, Siemens, etc.).
    If the input does **not** correspond to a valid company or seems like a celebrity, place, or generic term (e.g., "Virat Kohli", "India", "Cricket"), then respond with:
    "This does not appear to be a real company. Please enter a valid organization or business."

    If it is a real company, generate questions covering the following areas:
    - Company background and mission
    - Leadership team and board members
    - Financial performance (revenue, profit trends)
    - Business segments and product categories
    - Key products and services
    - Competitor landscape
    - Latest news, legal issues, or acquisitions
    - Employee size and culture
    - Historical or current funding events
    - Global operations and market presence
    - Research & development efforts
    - ESG, CSR, and sustainability practices
    - Supply chain structure and ethics
    - Recent innovations, patents, or partnerships

    Format the output as a **numbered bullet list** (1. to 15.). Do **not** include any explanation or introduction before the list.

    Return only the questions.
    """


    response = model.generate_content(prompt)
    questions = response.text.strip().split("\n")
    return [q.strip() for q in questions if q.strip()]