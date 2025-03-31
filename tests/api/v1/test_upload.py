import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path
from openpyxl import Workbook
import shutil
from io import BytesIO

from app.services.upload_storage import get_file_hash

client = TestClient(app)
UPLOAD_DIR = Path("uploads")


@pytest.fixture(scope="module")
def sample_excel_file() -> Path:
    # Create a sample Excel file with known structure
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Control Procedures"
    ws1.append(["id", "name", "description"])
    ws1.append(["CP-001", "Access Control", "Manage access rights"])
    ws2 = wb.create_sheet("Control Objectives")
    ws2.append(["id", "name", "objective"])
    ws2.append(["CO-001", "Endpoint Protection", "Protect endpoints"])

    file_path = UPLOAD_DIR / "test_sample.xlsx"
    wb.save(file_path)
    return file_path


def test_upload_valid_xlsx_file(sample_excel_file):
    with sample_excel_file.open("rb") as f:
        response = client.post(
            "/api/v1/upload",
            files={
                "file": (
                    "test_sample.xlsx",
                    f,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            },
        )
    assert response.status_code in (200, 400)
    if response.status_code == 200:
        assert "file_hash" in response.json()
        assert "filename" in response.json()
    else:
        assert response.json()["detail"] == "File already uploaded."


def test_upload_invalid_file_extension():
    response = client.post(
        "/api/v1/upload", files={"file": ("test.txt", b"invalid", "text/plain")}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Only .xlsx or .xls files are supported."


def test_list_uploaded_files():
    response = client.get("/api/v1/upload/list")
    assert response.status_code == 200
    assert isinstance(response.json()["files"], list)
    assert any("file_hash" in f for f in response.json()["files"])


def test_get_sheets_for_uploaded_file(sample_excel_file):
    # Read file content and wrap as UploadFile
    file_bytes = sample_excel_file.read_bytes()
    upload_file = UploadFile(filename="test_sample.xlsx", file=BytesIO(file_bytes))

    # Compute file hash from UploadFile
    file_hash = get_file_hash(upload_file)

    # Save a copy to uploads folder using correct hash
    dest_path = Path("uploads") / f"{file_hash}.xlsx"
    shutil.copy(sample_excel_file, dest_path)

    # Call the API to get sheets
    response = client.get(f"/api/v1/upload/{file_hash}/sheets")
    assert response.status_code == 200
    assert "Control Procedures" in response.json()["sheets"]
    assert "Control Objectives" in response.json()["sheets"]


def test_preview_sheet_data(sample_excel_file):
    # Wrap test file in UploadFile for hashing
    file_bytes = sample_excel_file.read_bytes()
    upload_file = UploadFile(filename="test_sample.xlsx", file=BytesIO(file_bytes))

    file_hash = get_file_hash(upload_file)

    # Copy sample file to expected upload location
    file_path = Path("uploads") / f"{file_hash}.xlsx"
    shutil.copy(sample_excel_file, file_path)

    # Hit the preview endpoint
    response = client.get(
        f"/api/v1/upload/{file_hash}/sheets/Control%20Procedures/preview?limit=2"
    )
    assert response.status_code == 200
    assert isinstance(response.json()["preview"], list)
    assert len(response.json()["preview"]) <= 2
