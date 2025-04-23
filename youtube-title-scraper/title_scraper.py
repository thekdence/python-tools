from playwright.sync_api import sync_playwright, Playwright
import csv

channel = "https://www.youtube.com/@Sparkykawa/videos"


def run(playwright: Playwright):
    chrome = playwright.chromium
    browser = chrome.launch(headless=True)
    page = browser.new_page()
    page.goto(channel)
    page.wait_for_load_state("networkidle")

    # Scroll down to get every video
    while True:
        # Find out how many titles there are currently
        previous_count = len(
            page.locator(
                "yt-formatted-string#video-title.style-scope.ytd-rich-grid-media"
            ).all()
        )

        print(f"Scrolling... Videos loaded so far: {previous_count}")

        # Scroll down
        page.evaluate("window.scrollBy(0,2000)")

        # Wait for videos to load
        page.wait_for_timeout(2000)

        current_count = len(
            page.locator(
                "yt-formatted-string#video-title.style-scope.ytd-rich-grid-media"
            ).all()
        )

        if current_count == previous_count:
            print("Reached the bottom, stopping scroll.")
            break

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
    for i in range(0, len(view_count_elements), 2):
        view_counts.append(view_count_elements[i].inner_text())

    min_length = min(len(titles), len(view_counts))
    titles = titles[:min_length]
    view_counts = view_counts[:min_length]

    # Save results as a csv
    with open("channelname_scrapes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Video Title", "View Count"])

        for title, views in zip(titles, view_counts):
            writer.writerow([title, views])

    print("Data saved.")

    # Print results (formatted for a spreadsheet)
    # print("\nFormatted Output (Google Sheets Style):")
    # print(f"{'Video Title':<70} | {'View Count'}")  # Header row
    # print("-" * 85)

    # for title, views in zip(titles, view_counts):
    #     print(f"{title:<70} | {views}")

    # print(f"Total videos loaded: {current_count}")

    # input("Press Enter to close the browser...")
    # browser.close()


with sync_playwright() as playwright:
    run(playwright)
