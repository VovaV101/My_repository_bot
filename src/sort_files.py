import re
import rarfile
import sys
from pathlib import Path
import shutil
from transliterate import translit

class FileOrganizer:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.categories = {
            "Audio": [".mp3", ".wav", ".ogg", ".amr"],
            "Docs": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
            "Images": [".jpeg", ".png", ".jpg", ".svg"],
            "Video": [".avi", ".mp4", ".mov", ".mkv"],
            "Archives": [".zip", ".gz", ".tar", ".rar"]
        }

    def normalize(self, text):
        transliterated_text = translit(text, 'uk', reversed=True)
        normalized_text = re.sub(r'[^a-zA-Z0-9]', '_', transliterated_text)
        normalized_text = normalized_text.lower()
        return normalized_text

    def get_category(self, file):
        ext = file.suffix.lower()
        for cat, exts in self.categories.items():
            if ext in exts:
                return cat
        return "Other"

    def move_file(self, file, category):
        target_dir = self.root_dir.joinpath(category)
        if not target_dir.exists():
            target_dir.mkdir()
        new_filename = self.normalize(file.stem) + file.suffix
        new_path = target_dir.joinpath(new_filename)
        if not new_path.exists():
            file.replace(new_path)

    def remove_empty_folders(self, root_path=None):
        if root_path is None:
            root_path = self.root_dir

        for folder_path in root_path.iterdir():
            if folder_path.is_dir():
                self.remove_empty_folders(folder_path)
                if not list(folder_path.iterdir()):
                    folder_path.rmdir()

    def extract_and_move_archives(self):
        archive_dir = self.root_dir / "Archives"
        for archive_path in self.root_dir.glob("**/*.*"):
            try:
                archive_name = archive_path.stem
                archive_subdir = archive_dir / archive_name
                archive_subdir.mkdir(exist_ok=True)
                if archive_path.suffix.lower() == ".rar":
                    with rarfile.RarFile(archive_path) as rf:
                        rf.extractall(archive_subdir)
                    archive_path.unlink()
                elif archive_path.suffix.lower() in {".zip", ".gz", ".tar"}:
                    shutil.unpack_archive(archive_path, archive_subdir)
                    archive_path.unlink()

            except (shutil.ReadError, rarfile.Error) as e:
                print(f"Error extracting {archive_path}: {e}")
                print(f"Skipping file: {archive_path}")

    def organize_files(self):
        for element in self.root_dir.glob("**/*"):
            if element.is_file():
                category = self.get_category(element)
                self.move_file(element, category)

    def organize(self):
        self.organize_files()
        self.extract_and_move_archives()
        self.remove_empty_folders()
        print("All ok")


def main():
    try:
        if len(sys.argv) < 2:
            raise IndexError("No path to folder")
        path = Path(sys.argv[1])
    except IndexError as e:
        print(f"Error: {e}")
        return

    if not path.exists():
        print("Error: Folder does not exist")
        return

    organizer = FileOrganizer(path)
    organizer.organize()


if __name__ == '__main__':
    main()