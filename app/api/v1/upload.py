from fastapi import APIRouter, UploadFile, File, HTTPException
from uuid import uuid4
from pathlib import Path
from typing import List
import json


from app.services.input_data import list_sheets, list_columns, extract_data
from app.services.upload_storage import save_file, save_metadata, get_file_hash

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter()


@router.post("/upload", tags=["Upload"])
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400, detail="Only .xlsx or .xls files are supported."
        )

    # Generate file hash
    file_hash = get_file_hash(file)
    file_path = UPLOAD_DIR / f"{file_hash}.xlsx"

    # Check if file already exists
    if file_path.exists():
        raise HTTPException(status_code=400, detail="File already uploaded.")

    # Save the file and its metadata
    save_file(file_hash, file)
    save_metadata(file_hash, file.filename)

    return {"file_hash": file_hash, "filename": file.filename}


@router.get("/upload/list", tags=["Upload"])
def list_uploaded_files() -> dict:
    """
    Returns a list of uploaded files by reading metadata JSON files.
    """
    files = []

    for meta_path in UPLOAD_DIR.glob("*.meta.json"):
        try:
            with meta_path.open("r", encoding="utf-8") as f:
                metadata = json.load(f)
                files.append(metadata)
        except Exception:
            continue  # Skip corrupted or invalid files

    return {"files": files}


@router.get("/upload/{file_id}/sheets", tags=["Upload"])
def get_sheet_names(file_id: str):
    file_path = UPLOAD_DIR / f"{file_id}.xlsx"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        sheets = list_sheets(file_path)
        return {"sheets": sheets}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to read Excel file: {str(e)}"
        )


@router.get("/upload/{file_id}/sheets/{sheet}/columns", tags=["Upload"])
def get_sheet_columns(file_id: str, sheet: str):
    file_path = UPLOAD_DIR / f"{file_id}.xlsx"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        columns = list_columns(file_path, sheet)
        return {"columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read columns: {str(e)}")


@router.get("/upload/{file_id}/sheets/{sheet}/preview", tags=["Upload"])
def preview_sheet_data(file_id: str, sheet: str, limit: int = 5):
    """
    Returns up to `limit` rows from a given sheet for preview purposes.
    """
    file_path = UPLOAD_DIR / f"{file_id}.xlsx"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        # Grab all columns from the sheet header
        all_columns = list_columns(file_path, sheet)
        all_data = extract_data(file_path, sheet, all_columns)
        return {"preview": all_data[:limit]}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to extract preview: {str(e)}"
        )
