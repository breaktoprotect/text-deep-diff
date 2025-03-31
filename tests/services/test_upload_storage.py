import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import UploadFile
from io import BytesIO
import json
import hashlib

from app.services.upload_storage import (
    get_file_hash,
    save_file,
    save_metadata,
    UPLOAD_DIR,
)


@pytest.fixture
def test_upload_file() -> UploadFile:
    content = b"dummy file content"
    file = BytesIO(content)
    return UploadFile(filename="test.xlsx", file=file)


def test_get_file_hash_generates_expected_sha256(test_upload_file):
    test_upload_file.file.seek(0)
    expected_hash = hashlib.sha256(b"dummy file content").hexdigest()
    actual_hash = get_file_hash(test_upload_file)
    assert actual_hash == expected_hash


def test_save_file_creates_file_with_correct_content(test_upload_file):
    file_hash = get_file_hash(test_upload_file)
    test_upload_file.file.seek(0)
    saved_path = save_file(file_hash, test_upload_file)

    assert saved_path.exists()
    assert saved_path.read_bytes() == b"dummy file content"

    saved_path.unlink()  # cleanup


def test_save_metadata_creates_json_file():
    file_hash = "abc123test"
    test_filename = "uploaded.xlsx"
    save_metadata(file_hash, test_filename)

    metadata_path = UPLOAD_DIR / f"{file_hash}.meta.json"
    assert metadata_path.exists()

    with metadata_path.open("r") as f:
        metadata = json.load(f)
    assert metadata["file_hash"] == file_hash
    assert metadata["filename"] == test_filename

    metadata_path.unlink()  # cleanup
