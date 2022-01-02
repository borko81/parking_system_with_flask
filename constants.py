import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_FILE_FOLDER = os.path.join(ROOT_DIR, "temp_files")
photo_url = "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"
photo_ext = "jpg"
