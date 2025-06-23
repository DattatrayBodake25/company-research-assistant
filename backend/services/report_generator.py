import json
import google.generativeai as genai
import os

from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Correct usage: model_name instead of model
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def load_json(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def create_report_from_json(filepath: str) -> str:
    data = load_json(filepath)


    prompt = """You are a professional company analyst assistant.

Your task is to write a comprehensive, factual, and well-organized report on the company using only the provided question-answer pairs. These pairs are based on credible sources.

Instructions:
- Structure the report into clear, well-titled sections (e.g., Overview, Leadership, Financials, Products, etc.).
- Avoid summarizing vaguely — instead, create a coherent narrative grounded in the details provided.
- Do not add external information or make assumptions beyond the given data.
- After each section, include source attribution in parentheses using the provided URLs.
- Maintain a formal, analytical, and objective tone.

---"""

    for idx, (question, answers) in enumerate(data.items(), 1):
        content = ""
        for entry in answers[:3]:  # use top 3 results
            title = entry.get("title", "")
            body = entry.get("content", "").strip()
            url = entry.get("url", "")
            if body:
                content += f"Title: {title}\nContent: {body}\nSource: {url}\n\n"

        prompt += f"\nQ{idx}. {question}\n{content}\n---\n"

    response = model.generate_content(prompt)
    return response.text.strip()