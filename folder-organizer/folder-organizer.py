import os
import shutil
import easygui
import sys


class FileOrganizer:
    def __init__(self):
        self.directory = easygui.diropenbox(
            "Choose the folder to clean up.", "Folder Organizer"
        )
        if not self.directory:
            sys.exit("No folder selected. Exiting.")
        self.file_types = {
            "Documents": [".pdf", ".txt", ".docx", ".csv", ".md", ".xls", ".xlsx"],
            "Images": [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".bmp",
                ".webp",
                ".svg",
                ".avif",
            ],
            "Videos": [".mp4", ".mov", ".avi", ".mkv"],
            "Audio": [".mp3", ".wav", ".ogg", ".flac", ".m4a"],
            "Archives": [".zip", ".rar", ".7z", ".tar.gz"],
            "Executables": [".exe", ".msi"],
            "Fonts": [".ttf", ".otf"],
            "3D Models": [".3mf", ".stl"],
            "Project Files": [".psd", ".prproj", ".blend", ".aep"],
            "Code Files": [
                ".py",
                ".js",
                ".java",
                ".cpp",
                ".html",
                ".css",
                ".ahk",
                ".c",
                ".h",
            ],
        }

    def categorize_file(self, filename):
        file_extension = os.path.splitext(filename)[1].lower()

        for category, extensions in self.file_types.items():
            if file_extension in extensions:
                return category

        return "Miscellaneous"

    def list_all_files(self):
        print("Files found:")
        for file in os.listdir(self.directory):
            file_path = os.path.join(self.directory, file)
            if os.path.isfile(file_path):
                print(file)

    def organize_files(self):
        user_confirmed = easygui.ynbox(
            "Are you sure you want to organize this folder?", "Folder organizer"
        )

        if user_confirmed:

            for file in os.listdir(self.directory):
                file_path = os.path.join(self.directory, file)

                if os.path.isfile(file_path):
                    category = self.categorize_file(file)
                    category_folder = os.path.join(self.directory, category)

                    os.makedirs(category_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(category_folder, file))

                    print(f"Moved {file} → {category}/")
        else:
            sys.exit(0)


# Create the FileOrganizer object
organizer = FileOrganizer()  # Change path if needed

organizer.organize_files()
