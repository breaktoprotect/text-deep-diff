import hashlib
from pathlib import Path
import shutil
from fastapi import UploadFile
import json

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def get_file_hash(upload_file: UploadFile) -> str:
    """Generate SHA-256 hash of the uploaded file content and rewind."""
    sha256 = hashlib.sha256()
    upload_file.file.seek(0)  # ensure start
    for chunk in iter(lambda: upload_file.file.read(4096), b""):
        sha256.update(chunk)
    upload_file.file.seek(0)  # rewind after read
    return sha256.hexdigest()


def save_file(file_hash: str, upload_file: UploadFile) -> Path:
    """Save the file using the file hash as the name."""
    file_path = UPLOAD_DIR / f"{file_hash}.xlsx"
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path


def save_metadata(file_hash: str, filename: str) -> None:
    """Save metadata for the uploaded file."""
    metadata = {
        "file_hash": file_hash,
        "filename": filename,
    }
    metadata_path = UPLOAD_DIR / f"{file_hash}.meta.json"
    metadata_path.write_text(json.dumps(metadata))
