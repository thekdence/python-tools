# GoBuster Tab Opener

This tool automates directory enumeration using GoBuster and opens all valid results in new browser tabs.

## What It Does

- Runs a GoBuster scan against a target web server
- Filters for useful HTTP status codes (200, 301, 403, 500)
- Opens each discovered directory in Firefox as a new browser tab
- Prints the endpoint name to the terminal (just the final path segment)

## Requirements

- `gobuster` installed and available in your system's PATH
- `firefox` browser
- Python 3

## Usage

1. Edit the script and set your target and wordlist:

    ```python
    target_ip = "http://10.10.128.124/gallery"
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    ```

2. Run the script:

    ```bash
    python3 gobuster_opener.py
    ```

3. Valid results will open in Firefox tabs. Output will also be printed in the terminal.

## Notes

This is useful for quickly reviewing potential entry points during web enumeration. Adjust the HTTP status codes in the script if you want to include or exclude more response types.
