import subprocess
import webbrowser
import re

# Target details
target_ip = "http://10.10.128.124/gallery"
wordlist = "/usr/share/wordlists/dirb/common.txt"

# Run Gobuster
command = [
    "gobuster", "dir",
    "-u", target_ip,
    "-w", wordlist,
    "-q"
]

print("[*] Running Gobuster...")
process = subprocess.run(command, capture_output=True, text=True)
output = process.stdout

# Regex to grab path and status
pattern = re.compile(r"(/[^ ]+)\s+\(Status:\s+(\d{3})")
good_codes = {"200", "301", "403", "500"}
urls_to_open = []

# Parse Gobuster output
for line in output.splitlines():
    match = pattern.search(line)
    if match:
        path, code = match.groups()
        if code in good_codes:
            full_url = f"{target_ip}{path}"
            urls_to_open.append(full_url)

# Output
print(f"[*] Found {len(urls_to_open)} URLs:\n")
for url in urls_to_open:
    print(url.rsplit("/", 1)[-1])  # just the last part
    webbrowser.get("firefox").open_new_tab(url)
