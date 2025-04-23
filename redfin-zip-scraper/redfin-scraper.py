# Brings in Playwright to automate the browser
from playwright.sync_api import sync_playwright
import re  # Regular expressions, for finding price strings
from statistics import median  # For finding the middle price in a list

# Pulls a price from text like "$1,234,567"


def extract_price(text):
    # Look for a dollar sign followed by digits and commas
    match = re.search(r"\$([\d,]+)", text)
    if match:
        # Strip commas and return as integer
        return int(match.group(1).replace(",", ""))
    return None  # If no price found, return nothing

# Decides if a listing looks like land based on keywords


def is_land_listing(text):
    land_keywords = ["land", "lot", "vacant",
                     "acre", "parcel"]  # All the red flags
    # True if any keyword is in the text
    return any(keyword in text.lower() for keyword in land_keywords)

# The main scraping engine for one ZIP code


def scrape_zip(page, zip_code):
    all_prices = []  # This is where we store every valid home price we find
    seen_prices = set()  # A set to remember every unique price we’ve already seen (fast lookup)
    page_number = 1  # Start scraping from page 1

    while True:  # Loop until we decide we’ve seen enough
        # Build the URL. Page 1 uses a clean URL. Page 2+ appends '/page-#'
        url = f"https://www.redfin.com/zipcode/{zip_code}/page-{page_number}" if page_number > 1 else f"https://www.redfin.com/zipcode/{zip_code}"
        page.goto(url)  # Load the current page in the browser

        try:
            # Wait until home listings are visible. If they don’t show up, assume it’s dead.
            page.wait_for_selector("div.HomeCardContainer", timeout=8000)
        except:
            # If the page never loaded listings, it’s time to bail.
            print(f"[{zip_code}] No more listings or timeout.")
            break

        # Grab all the listing containers on the page
        cards = page.locator("div.HomeCardContainer")

        # Count how many *new* listings we scrape this round
        listings_this_page = 0

        # Go through each listing one by one
        for i in range(cards.count()):
            # Pull the full text of the listing card
            text = cards.nth(i).inner_text()

            if is_land_listing(text):  # Skip land listings—junk data
                continue

            price = extract_price(text)  # Try to grab the price from the text
            # If it’s valid and we haven’t seen it before...
            if price and price not in seen_prices:
                all_prices.append(price)  # ...keep it
                # Remember it so we don’t count it again
                seen_prices.add(price)
                listings_this_page += 1  # Count it as new

        # If we didn’t get anything new, we’ve hit the end—stop scraping
        if listings_this_page == 0:
            print(f"[{zip_code}] No new listings found. Likely end of results.")
            break

        page_number += 1  # Move to the next page and do it again

    return all_prices  # Send the full list of prices back to the main program


def main():
    zip_codes = ["28041", "28146"]  # ZIP codes we want to search

    with sync_playwright() as p:  # Start the browser engine
        # Launch visible browser (headless=True hides it)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()  # Fresh session with no cookies or cache
        page = context.new_page()  # Open a new tab

        results = []  # List to store the summary of each ZIP

        for zip_code in zip_codes:  # One ZIP at a time
            print(f"\nScraping {zip_code}...")
            prices = scrape_zip(page, zip_code)  # Get the prices for that ZIP

            if prices:  # If we got anything usable
                avg = sum(prices) / len(prices)  # Average price
                med = median(prices)  # Median price
                results.append({  # Store the results
                    "zip": zip_code,
                    "count": len(prices),
                    "average": avg,
                    "median": med
                })
                # Print a quick summary
                print(f"\n[RESULT] {zip_code}")
                print(f"  Listings found: {len(prices)}")
                print(f"  Average price: ${avg:,.0f}")
                print(f"  Median price:  ${med:,.0f}")
            else:
                print(f"\n[RESULT] {zip_code}: No valid prices found.")

        browser.close()  # Clean exit, shut down browser

        if results:
            print("\n--- Price Comparison (Sorted by Median) ---")
            # Sort ZIPs from cheapest to most expensive (median)
            results.sort(key=lambda x: x["median"])

            # Use the cheapest ZIP as a reference point
            baseline = results[0]["median"]
            for r in results:
                # How much more expensive is this ZIP compared to the cheapest one?
                diff = ((r["median"] - baseline) / baseline) * \
                    100 if baseline else 0
                print(
                    f"{r['zip']}: Median ${r['median']:,.0f} ({diff:+.1f}% vs cheapest), {r['count']} listings"
                )


# If we're running this script directly (not importing it), fire main()
if __name__ == "__main__":
    main()
