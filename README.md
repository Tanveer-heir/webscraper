# Quotes Scraper

A Python script to scrape quotes, authors, tags, and URLs from [quotes.toscrape.com](http://quotes.toscrape.com/), with smart features including checkpoint/resume, duplicate avoidance, and command-line configurability.

---

## Features

- **Scrapes quote text, author, tags, and detail URL.**
- **Avoids duplicates**—does not re-save existing quotes.
- **Checkpointing:** Progress is saved, so you can safely resume interrupted runs.
- **Randomized delay** between requests to be polite to servers.
- **Command-line arguments:** Choose number of pages and output filename easily.
- **CSV output**—ready for Excel, pandas, or analysis.

---

## Requirements

- Python 3.x
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- Install dependencies via pip

---

## Output Format

- CSV with columns:
  - **Quote** (text)
  - **Author**
  - **Tags** (comma separated)
  - **URL** (detail page link)

---

## Notes

- Randomized delay helps reduce server load and potential blocking.
- Script saves a small `progress.txt` file during its run for checkpointing (automatically deleted at completion).
- Input is sanitized to avoid duplicates, making repeated runs safe.

---

## License

MIT License. See `LICENSE` for details.

---

## Author

Maintained by Tanveer Singh.  
Feedback, issues, and pull requests are welcomed!
