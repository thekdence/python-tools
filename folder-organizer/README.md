# Folder Organizer

Sorts all files in a selected folder into categorized subfolders based on file type. Useful for cleaning up cluttered directories like Downloads or project folders.

## What It Does

- Automatically creates folders by file type (Documents, Images, Code Files, etc.)
- Moves files into the appropriate category
- Uses a simple GUI (via `easygui`) for folder selection and confirmation
- Prints all moved files to the terminal

## Requirements

- Python 3
- `easygui` module  
  Install with:  
  ```bash
  pip install easygui
  ```

## Usage

Just run the script:

```bash
python3 folder-organizer.py
```

1. A GUI will prompt you to select the folder to organize.
2. You’ll be asked to confirm before anything is moved.
3. Files are then sorted by type and placed into subfolders.

## File Categories (Examples)

- Documents: `.pdf`, `.docx`, `.txt`, `.md`, `.xls`
- Images: `.jpg`, `.png`, `.gif`, `.webp`, `.svg`
- Videos: `.mp4`, `.mov`, `.mkv`
- Audio: `.mp3`, `.wav`, `.ogg`
- Code Files: `.py`, `.js`, `.cpp`, `.html`, `.ahk`
- Archives: `.zip`, `.rar`, `.7z`
- Miscellaneous: everything else
