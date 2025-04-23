# Redfin ZIP Code Scraper

Scrapes home listings from Redfin for a list of ZIP codes and calculates average and median prices. Filters out land listings to focus only on valid home sales.

## What It Does

- Uses Playwright to browse Redfin listings
- Extracts and filters actual home prices (skips land/vacant lots)
- Calculates and compares average and median prices per ZIP code
- Outputs a sorted summary by median price

## Requirements

- Python 3
- Playwright  
  Install and set up with:  
  ```bash
  pip install playwright
  playwright install
  ```

## Usage

Edit the ZIP code list at the top of the script:

```python
zip_codes = ["28041", "28146"]
```

Then run:

```bash
python3 redfin-scraper.py
```

The browser will open, scrape each ZIP, and print results in the terminal.

## Output Example

```
[RESULT] 28041
  Listings found: 23
  Average price: $291,304
  Median price:  $276,000

--- Price Comparison (Sorted by Median) ---
28041: Median $276,000 (+0.0% vs cheapest), 23 listings
28146: Median $321,000 (+16.3% vs cheapest), 19 listings
```

## Notes

- Skips duplicate prices and land listings to keep data clean
- You can add more ZIP codes or change the filtering logic as needed
