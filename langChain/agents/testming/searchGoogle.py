
#coding=utf8
#pip install beautifulsoup4
# need more improvement

import requests
from bs4 import BeautifulSoup

def google_web_search(query):
    base_url = "https://www.google.com/search"
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        # Parse HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text content
        text_content = soup.get_text()

        # You can save the text content to a file or perform any other processing
        with open('search_results.txt', 'w', encoding='utf-8') as file:
            file.write(text_content)

        return text_content
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
query = "maharishi university"
result = google_web_search(query)
if result:
    print(result)
