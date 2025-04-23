import csv
import re


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

    print(f"CSV file '{file_path}' has been updated with formatted view counts.")


format_csv("y4mi_scrapes.csv")
