import os
import json
from datetime import datetime
from backend.services.search_engine import search_web

def bulk_search_questions(company: str, questions: list, save_dir="data/scraped_content") -> str:
    os.makedirs(save_dir, exist_ok=True)
    results = {}

    for idx, question in enumerate(questions, 1):
        print(f"Searching Q{idx}: {question}")
        try:
            search_results = search_web(question)
            results[question] = search_results
        except Exception as e:
            results[question] = [{"error": str(e)}]

    # Save results to a JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{company.replace(' ', '_')}_{timestamp}.json"
    filepath = os.path.join(save_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"All search results saved to: {filepath}")
    return filepath