# YouTube Title Scraper

Scrapes all video titles and view counts from a YouTube channel and saves them to a CSV. Supports custom channel links or aliases, optional page limit, and formats view counts into integers.

## What It Does

- Scrolls through a full YouTube channel's video list
- Extracts video titles and view counts
- Saves data to a CSV named after the channel
- Converts view counts like `12K` or `1.3M` into raw integers

## Requirements

- Python 3
- Playwright  
  Install and set up with:  
  ```bash
  pip install playwright
  playwright install
  ```

## Usage

Run the script:

```bash
python3 main.py
```

Then follow the prompts:
- Choose to input a full channel URL or just the alias (e.g. `Sparkykawa`)
- Set a page limit or enter `0` to scrape all available videos

## Output

A CSV named after the channel will be saved in the current directory:

```
sparkykawa.csv
```

Each row contains:
- Video Title
- View Count (converted to integer)

## Notes

- Works in headless mode (no visible browser)
- If the CSV already exists, it will be overwritten
- View count formatting is applied after scraping
