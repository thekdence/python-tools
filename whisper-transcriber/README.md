# Whisper Transcriber

Uses OpenAI's Whisper model to transcribe video and audio files to plain text. Works in single-file mode or batch mode for entire folders.

## What It Does

- Transcribes `.mp4`, `.mp3`, `.wav`, `.mkv`, `.mov`
- Supports Whisper models: `tiny`, `base`, `small`, `medium`, `large`
- Outputs transcript as `.txt` file next to the original media
- Supports transcribing a single file or a full folder

## Requirements

- Python 3
- `openai-whisper` library  
  Install with:  
  ```bash
  pip install -U openai-whisper
  ```

## Usage

Edit the script before running:

```python
mode = "single"  # or "folder"
input_path = "/path/to/file/or/folder"
model_size = "large"
```

Then run:

```bash
python3 whisper-transcriber.py
```

Each transcript is saved in the same directory as the media file, with `-transcript.txt` appended to the filename.

## Notes

- `mode = "single"` transcribes one video or audio file.
- `mode = "folder"` will process all supported media files in the specified folder.
