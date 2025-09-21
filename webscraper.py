import requests
from bs4 import BeautifulSoup
import csv
import time

def fetch_page_quotes(page_num):
    url = f"http://quotes.toscrape.com/page/{page_num}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch page {page_num}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.find_all("div", class_="quote")
    page_quotes = []
    for quote in quotes:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
        page_quotes.append({"text": text, "author": author, "tags": tags})
    return page_quotes

def scrape_quotes(pages=5, output_file="quotes_github.csv"):
    all_quotes = []
    print(f"Starting scraping {pages} pages...")
    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        quotes = fetch_page_quotes(page)
        if quotes is None:
            break
        all_quotes.extend(quotes)
        time.sleep(1)

    if not all_quotes:
        print("No quotes scraped. Exiting.")
        return

    try:
        with open(output_file, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Quote", "Author", "Tags"])
            for q in all_quotes:
                writer.writerow([q["text"], q["author"], ", ".join(q["tags"])])
        print(f"Saved {len(all_quotes)} quotes to {output_file}")
    except IOError as e:
        print(f"Failed to write to file: {e}")

if __name__ == "__main__":
    scrape_quotes()
