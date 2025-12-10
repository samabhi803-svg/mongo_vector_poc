from googlesearch import search
import sys

def test_search():
    query = "What is the stock price of Tata Motors?"
    print(f"Testing search for: '{query}'")
    try:
        # Try advanced=True first
        print("Attempting advanced=True...")
        results = search(query, num_results=3, advanced=True)
        count = 0
        for r in results:
            print(f"Result {count+1}: {r.title} - {r.url}")
            count += 1
        print(f"Total advanced results: {count}")
        
        if count == 0:
            print("\nAttempting advanced=False (URLs only)...")
            results = search(query, num_results=3, advanced=False)
            for url in results:
                print(f"URL: {url}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
