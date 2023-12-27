
#coding=utf8
# formating is not good
import requests

def google_web_search(query):
    base_url = "https://www.google.com/search"
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
query = "web search postman"
result = google_web_search(query)
if result:
    print(result)
