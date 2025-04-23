from playwright.sync_api import sync_playwright, Playwright
import csv
import os
import time

# Hard-Coded values for testing purposes
# channel_link = "https://www.youtube.com/@Sparkykawa/videos"
# channel_name_alias = "sparkykawa"
# limit_pages_to = (
#     0  # Can decide to limit the amount of pages to be loaded, 0 for no limit
# )


# A function to clear the terminal screen.
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


making_selection = True
while making_selection:
    clear_screen()
    print(
        "First we need to select the channel.\nWould you like to\n1. Give me the entire channel link\n2. Provide the channels alias (The part after the @ symbol) e.g https://www.youtube.com/@mustyisabitch"
    )
    link_provide_method = int(input())

    if link_provide_method == 1:
        clear_screen()
        channel_link = input("Okay, paste the link.\n")

        clear_screen()
        channel_name_alias = input(
            "Since you provided a link we still need the channel alias name for naming the csv. What name would you like to choose?\n"
        )
        clear_screen()
    elif link_provide_method == 2:
        clear_screen()
        channel_name_alias = input(
            "Okay give me the alias. Remember this is the part after the @ symbol (DO NOT INCLUDE THE @ SYMBOL), make sure it's right or it's not gonna work.\n"
        )
        channel_link = f"https://www.youtube.com/@{channel_name_alias}/videos"
    else:
        print("You did something wrong. Let's try this again")
        clear_screen()
        continue
    limit_pages_to = int(
        input(
            "Would you like to limit how many pages of videos back we go? If yes just input the limit. Otherwise input 0 to scrape every video.\n(This may take some time depending on the amount of videos).\n"
        )
    )

    clear_screen()

    print("Alright... Let's do this shit then")
    time.sleep(1.5)
    print(
        "The CSV will be outputted in whatever directory this script is ran in. Look at the path in your terminal. That's where it will be."
    )
    break


# The main scraping function.
def run(playwright: Playwright):
    chrome = playwright.chromium
    browser = chrome.launch(headless=True)
    page = browser.new_page()

    print("Loading scraper...")

    page.goto(channel_link)
    page.wait_for_load_state("networkidle")
    pages_loaded = 1

    # Scroll down to get every video
    while True:
        # Find out how many titles there are currently, to be referenced against later
        previous_count = len(
            page.locator(
                "yt-formatted-string#video-title.style-scope.ytd-rich-grid-media"
            ).all()
        )

        # If only wanting one page, don't scroll.
        if limit_pages_to == 1:
            print("Only 1 page was requested, so no scrolling...")
            break

        print(
            f"Scrolling... Out of {pages_loaded} pages, {previous_count} videos have been loaded."
        )

        # Scroll down
        page.evaluate("window.scrollBy(0,2000)")

        # Wait for videos to load
        page.wait_for_timeout(2000)

        # Increase counter for the amount of pages loaded.
        pages_loaded += 1

        # Get the new current number of assets loaded
        current_count = len(
            page.locator(
                "yt-formatted-string#video-title.style-scope.ytd-rich-grid-media"
            ).all()
        )

        # Check the amount of assets to see if no new ones have been loaded
        if current_count == previous_count:
            print("Reached the bottom, stopping scroll.")
            break

        # Also checks for a limit on amount of pages to load
        if pages_loaded == limit_pages_to:
            print("Loaded the requested number of pages, ending scrolling")
            break

    print("Extracting content, this may take a moment...")

    # Extract video titles
    title_elements = page.locator(
        "yt-formatted-string#video-title.style-scope.ytd-rich-grid-media"
    ).all()
    titles = []
    for title in title_elements:
        titles.append(title.inner_text())

    # Extract view counts
    view_count_elements = page.locator(
        "span.inline-metadata-item.style-scope.ytd-video-meta-block"
    ).all()
    view_counts = []
    # Loop through for the amount of title elements. We step by 2 because we are skipping over the upload dates.
    for i in range(0, len(view_count_elements), 2):
        view_counts.append(view_count_elements[i].inner_text())

    min_length = min(len(titles), len(view_counts))
    titles = titles[:min_length]
    view_counts = view_counts[:min_length]

    # Save results as a csv
    with open(f"{channel_name_alias}.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Video Title", "View Count"])

        for title, views in zip(titles, view_counts):
            writer.writerow([title, views])

    print("Data saved has been saved to an initial CSV.")
    time.sleep(2)


# Main function to format the data
def clean_view_count(view_count):
    """Converts YouTube view counts like '12K; into integers (e.g.,).

    Args:
        view_count (_type_): _description_

    Returns:
        _type_: _description_
    """

    view_count = view_count.replace(" views", "").strip()

    if "K" in view_count:
        return int(float(view_count.replace("K", "")) * 1_000)
    elif "M" in view_count:
        return int(float(view_count.replace("M", "")) * 1_000_000)
    else:
        return int(view_count)


def format_csv(file_path):
    """Reads a csv file, formats the view counts, and overwrites the original file.

    Args:
        file_path (str): The path of the csv to convert
    """

    rows = []

    # Read the original file
    with open(file_path, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read header row
        rows.append(header)  # Store header row

        for row in reader:
            title, views = row
            formatted_views = clean_view_count(
                views
            )  # Convert view count to an integer
            rows.append([title, formatted_views])  # Store formatted data

    # Overwrite the file with cleaned data
    with open(file_path, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)  # Write everything back

    print(
        f"CSV file '{file_path}' has been updated and formatted for correct view counts."
    )


with sync_playwright() as playwright:
    run(playwright)
clear_screen()
print("Scraping has completed! Now just to format the data.")
time.sleep(2)
format_csv(f"{channel_name_alias}.csv")
time.sleep(3)
clear_screen()
print("Everything completed successfully.")
time.sleep(2.5)
