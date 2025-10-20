import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import random
import argparse

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
        quote_url = quote.find("span", class_="text").find_parent("div", class_="quote").find("a")
        quote_link = "http://quotes.toscrape.com" + quote_url["href"] if quote_url else ""
        page_quotes.append({
            "text": text,
            "author": author,
            "tags": tags,
            "url": quote_link,
        })
    return page_quotes

def load_existing_quotes(output_file):
    existing = set()
    if os.path.isfile(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  
            for row in reader:
                if row:
                    existing.add(row[0])  
    return existing

def scrape_quotes(pages=5, output_file="quotes_github.csv", checkpoint=True):
    all_quotes = []
    start_page = 1

    if checkpoint and os.path.isfile("progress.txt"):
        with open("progress.txt", "r") as f:
            val = f.read().strip()
            if val.isdigit():
                start_page = int(val)

    print(f"Starting scraping from page {start_page} / target {pages} pages...")

    existing_quotes = load_existing_quotes(output_file)

    for page in range(start_page, pages + 1):
        print(f"Scraping page {page}...")
        quotes = fetch_page_quotes(page)
        if quotes is None:
            break
        new_quotes = [q for q in quotes if q['text'] not in existing_quotes]
        all_quotes.extend(new_quotes)
        existing_quotes.update(q['text'] for q in new_quotes)
        with open("progress.txt", "w") as f:
            f.write(str(page + 1))
        time.sleep(random.uniform(1, 2.5))

    if not all_quotes:
        print("No new quotes scraped. Exiting.")
        return

    file_exists = os.path.isfile(output_file)
    try:
        with open(output_file, "a" if file_exists else "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Quote", "Author", "Tags", "URL"])
            for q in all_quotes:
                writer.writerow([q["text"], q["author"], ", ".join(q["tags"]), q["url"]])
        print(f"Saved {len(all_quotes)} quotes to {output_file}")
    except IOError as e:
        print(f"Failed to write to file: {e}")

    os.remove("progress.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape quotes from quotes.toscrape.com")
    parser.add_argument("-p", "--pages", type=int, default=5, help="Number of pages to scrape")
    parser.add_argument("-o", "--output", default="quotes_github.csv", help="CSV output file")
    parser.add_argument("--no-checkpoint", action="store_true", help="Disable resume/progress tracking")
    args = parser.parse_args()
    scrape_quotes(pages=args.pages, output_file=args.output, checkpoint=not args.no_checkpoint)
