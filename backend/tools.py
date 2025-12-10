# from ddgs import DDGS 
# The package has been renamed to ddgs, but usually the import might still be similar or changed.
# Let's try the new import convention if known, or stick to robust import.
# Recent versions of 'duckduckgo-search' (now 'ddgs') often invoke via `from duckduckgo_search import DDGS` still, 
# BUT if installed as `ddgs`, we should check.
# Actually, the warning comes from the library itself saying "renamed to ddgs".
# If we mistakenly import 'duckduckgo_search' it might be looking at the old package.
# Let's try importing from `duckduckgo_search` as it is standard, but if that fails, `ddgs`.
# Wait, the WARNING said `Use pip install ddgs instead`.
# Let's assume the import is `from duckduckgo_search import DDGS` is still valid for many versions, 
# but simply installing the new package fixes it.
from ddgs import DDGS

def search_web(query, limit=3):
    """
    Searches the web using DuckDuckGo and returns a list of results.
    """
    try:
        results = []
        # ddgs.text() returns a list of dictionaries (not an iterator in recent versions, but safely handled)
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=limit)
            if search_results:
                for r in search_results:
                    results.append({
                        "title": r.get('title'),
                        "body": r.get('body'),
                        "href": r.get('href')
                    })
        
        print(f"DEBUG: DuckDuckGo Search Results for '{query}': {len(results)} found.")
        return results
    except Exception as e:
        print(f"Error searching DuckDuckGo: {e}")
        return []

if __name__ == "__main__":
    # Test
    print(search_web("Who won the 2024 Super Bowl?"))
