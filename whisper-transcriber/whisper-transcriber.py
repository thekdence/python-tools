import os
import whisper
import time

# === SETTINGS ===
mode = "single"  # "single" or "folder"
model_size = "large"  # "tiny", "base", "small", "medium", "large"
# folder or file depending on mode
input_path = "Linux_Privilege_Escalation\\09_Escalation_Path_Other_SUID_Escalation\\28 Escalation via Binary Symlinks.mp4"
# =================

model = whisper.load_model(model_size)
print(f"Loaded Whisper model: {model_size}")


def transcribe(video_file):
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    output_file = os.path.join(os.path.dirname(
        video_file), f"{base_name}-transcript.txt")

    print(f"Transcribing: {base_name}")
    start = time.time()

    result = model.transcribe(video_file, verbose=False)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result["text"])

    duration = round(time.time() - start, 2)
    print(f"Saved: {output_file} ({duration}s)")


if mode == "single":
    if os.path.isfile(input_path):
        transcribe(input_path)
    else:
        print("Error: Single mode selected, but input path is not a file.")
elif mode == "folder":
    for file in os.listdir(input_path):
        if file.lower().endswith((".mp4", ".mkv", ".mov", ".wav", ".mp3")):
            full_path = os.path.join(input_path, file)
            transcribe(full_path)
else:
    print("Invalid mode. Use 'single' or 'folder'.")
