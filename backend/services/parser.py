import json
import os
import re

def load_search_results(filepath: str, top_k: int = 3):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    parsed_docs = []

    for idx, (question, results) in enumerate(data.items()):
        combined_content = ""
        for item in results[:top_k]:
            title = item.get("title", "")
            content = item.get("content", "")
            url = item.get("url", "")
            # Clean up excessive whitespace or markdown
            content = re.sub(r'\n+', '\n', content.strip())
            combined_content += f"### {title}\n{content}\n(Source: {url})\n\n"

        parsed_docs.append({
            "question": question.strip("* ").strip(),
            "content": combined_content,
            "metadata": {
                "question_id": idx + 1
            }
        })

    return parsed_docs