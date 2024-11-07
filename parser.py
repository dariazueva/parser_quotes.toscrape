import json

import requests
from bs4 import BeautifulSoup


def get_quotes(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    quotes: list = []
    for quote in soup.select(".quote"):
        text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]
        quotes.append({"text": text, "author": author, "tags": tags})
    return quotes


def main():
    base_url = "https://quotes.toscrape.com/"
    all_quotes = []
    page = 1
    while True:
        url = f"{base_url}page/{page}/"
        quotes = get_quotes(url)
        if not quotes:
            break
        all_quotes.extend(quotes)
        page += 1
    with open("qoutes.json", "w") as f:
        json.dump(all_quotes, f, indent=4)
        print("Successfully!")


if __name__ == "__main__":
    main()
