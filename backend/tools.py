from duckduckgo_search import DDGS

def search_web(query, limit=3):
    """
    Searches the web using DuckDuckGo and returns a list of results.
    """
    try:
        results = []
        with DDGS() as ddgs:
            # text() returns an iterator
            for r in ddgs.text(query, max_results=limit):
                results.append(r)
        return results
    except Exception as e:
        print(f"Error searching web: {e}")
        return []

if __name__ == "__main__":
    # Test
    print(search_web("Who won the 2024 Super Bowl?"))
