import os
import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def search_web(query: str, max_results: int = 5) -> list:
    sources = [
        search_tavily,
        search_serpapi,
        search_brave,
        search_newsapi,
        search_rapidapi,
        search_wikipedia,
    ]

    for source in sources:
        try:
            results = source(query, max_results)
            if results:
                print(f"[INFO] {source.__name__} succeeded.")
                return results
        except Exception as e:
            print(f"[WARN] {source.__name__} failed: {e}")

    print("[ERROR] All search engines failed.")
    return []

def search_tavily(query, max_results):
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "max_results": max_results,
        "include_answer": False,
        "include_images": False
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return [
        {"url": r["url"], "title": r["title"], "content": r.get("content", "")}
        for r in response.json().get("results", [])
    ]

def search_serpapi(query, max_results):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": max_results,
        "engine": "google"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return [
        {
            "url": res.get("link"),
            "title": res.get("title"),
            "content": res.get("snippet", "")
        }
        for res in data.get("organic_results", [])[:max_results]
    ]

def search_brave(query, max_results):
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    params = {"q": query, "count": max_results}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return [
        {
            "url": item["url"],
            "title": item["title"],
            "content": item.get("description", "")
        }
        for item in response.json().get("web", {}).get("results", [])
    ]

def search_newsapi(query, max_results):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "pageSize": max_results,
        "apiKey": NEWSAPI_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return [
        {
            "url": a["url"],
            "title": a["title"],
            "content": a.get("description", "")
        }
        for a in response.json().get("articles", [])
    ]

def search_rapidapi(query, max_results):
    url = "https://bing-web-search1.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "bing-web-search1.p.rapidapi.com"
    }
    params = {"q": query, "count": max_results}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return [
        {
            "url": item["url"],
            "title": item["name"],
            "content": item.get("snippet", "")
        }
        for item in data.get("webPages", {}).get("value", [])
    ]

def search_wikipedia(query, max_results):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json().get("query", {}).get("search", [])
    return [
        {
            "url": f"https://en.wikipedia.org/wiki/{r['title'].replace(' ', '_')}",
            "title": r["title"],
            "content": r["snippet"]
        }
        for r in results[:max_results]
    ]







# import os
# import requests
# from dotenv import load_dotenv
# load_dotenv()

# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# SERPAPI_KEY = os.getenv("SERPAPI_KEY")
# BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
# NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
# RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# def search_web(query: str, max_results: int = 5) -> list:
#     sources = [
#         search_tavily,
#         search_serpapi,
#         search_brave,
#         search_newsapi,
#         search_rapidapi,
#         search_wikipedia,
#     ]
#     for source in sources:
#         try:
#             results = source(query, max_results)
#             if results:
#                 return results
#         except Exception as e:
#             print(f"[WARN] {source.__name__} failed: {e}")
#     return []

# # ------------------------
# # Individual Search Methods
# # ------------------------

# def search_tavily(query, max_results):
#     url = "https://api.tavily.com/search"
#     payload = {
#         "api_key": TAVILY_API_KEY,
#         "query": query,
#         "search_depth": "advanced",
#         "max_results": max_results,
#         "include_answer": False,
#         "include_images": False
#     }
#     response = requests.post(url, json=payload)
#     response.raise_for_status()
#     return [
#         {"url": r["url"], "title": r["title"], "content": r.get("content", "")}
#         for r in response.json().get("results", [])
#     ]

# def search_serpapi(query, max_results):
#     url = "https://serpapi.com/search"
#     params = {
#         "q": query,
#         "api_key": SERPAPI_KEY,
#         "num": max_results,
#         "engine": "google"
#     }
#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     data = response.json()
#     return [
#         {
#             "url": res.get("link"),
#             "title": res.get("title"),
#             "content": res.get("snippet", "")
#         }
#         for res in data.get("organic_results", [])[:max_results]
#     ]

# def search_brave(query, max_results):
#     url = "https://api.search.brave.com/res/v1/web/search"
#     headers = {"Accept": "application/json", "X-Subscription-Token": BRAVE_API_KEY}
#     params = {"q": query, "count": max_results}
#     response = requests.get(url, headers=headers, params=params)
#     response.raise_for_status()
#     return [
#         {
#             "url": item["url"],
#             "title": item["title"],
#             "content": item.get("description", "")
#         }
#         for item in response.json().get("web", {}).get("results", [])
#     ]

# def search_newsapi(query, max_results):
#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q": query,
#         "pageSize": max_results,
#         "apiKey": NEWSAPI_KEY
#     }
#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     return [
#         {
#             "url": a["url"],
#             "title": a["title"],
#             "content": a.get("description", "")
#         }
#         for a in response.json().get("articles", [])
#     ]

# def search_rapidapi(query, max_results):
#     url = "https://bing-web-search1.p.rapidapi.com/search"
#     headers = {
#         "X-RapidAPI-Key": RAPIDAPI_KEY,
#         "X-RapidAPI-Host": "bing-web-search1.p.rapidapi.com"
#     }
#     params = {"q": query, "count": max_results}
#     response = requests.get(url, headers=headers, params=params)
#     response.raise_for_status()
#     data = response.json()
#     return [
#         {
#             "url": item["url"],
#             "title": item["name"],
#             "content": item.get("snippet", "")
#         }
#         for item in data.get("webPages", {}).get("value", [])
#     ]

# def search_wikipedia(query, max_results):
#     url = "https://en.wikipedia.org/w/api.php"
#     params = {
#         "action": "query",
#         "list": "search",
#         "srsearch": query,
#         "format": "json"
#     }
#     response = requests.get(url, params=params)
#     response.raise_for_status()
#     results = response.json().get("query", {}).get("search", [])
#     return [
#         {
#             "url": f"https://en.wikipedia.org/wiki/{r['title'].replace(' ', '_')}",
#             "title": r["title"],
#             "content": r["snippet"]
#         }
#         for r in results[:max_results]
#     ]