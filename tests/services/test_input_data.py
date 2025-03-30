import pytest
from pathlib import Path
from openpyxl import Workbook
import tempfile

from app.services import input_data
from app.services.input_data import UnsupportedFileTypeError


@pytest.fixture
def structured_excel_file() -> Path:
    """
    Creates a temporary Excel file with two sheets
    """
    wb = Workbook()

    # Sheet A: Control Procedures
    sheet_a = wb.active
    sheet_a.title = "Control Procedures"
    sheet_a.append(["id", "name", "description"])
    sheet_a.append(
        ["CP-123", "User Access Control", "Defines how user access is managed."]
    )
    sheet_a.append(
        ["CP-456", "Network Segmentation", "Describes network isolation policies."]
    )

    # Sheet B: Control Objectives
    sheet_b = wb.create_sheet(title="Control Objectives")
    sheet_b.append(["ID", "Objective Name", "Objective"])
    sheet_b.append(
        ["CO-001", "Endpoint Protection", "To protect endpoint devices from threats."]
    )
    sheet_b.append(
        ["CO-002", "Data Encryption", "To secure data at rest and in transit."]
    )

    # Save to disk for inspection
    debug_path = Path("./tests/test_input_data.xlsx")
    wb.save(debug_path)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        wb.save(tmp.name)
        return Path(tmp.name)


def test_list_sheets(structured_excel_file):
    sheets = input_data.list_sheets(structured_excel_file)
    assert set(sheets) == {"Control Procedures", "Control Objectives"}


def test_list_columns_cp_sheet(structured_excel_file):
    columns = input_data.list_columns(structured_excel_file, "Control Procedures")
    assert columns == ["id", "name", "description"]


def test_list_columns_co_sheet(structured_excel_file):
    columns = input_data.list_columns(structured_excel_file, "Control Objectives")
    assert columns == ["ID", "Objective Name", "Objective"]


def test_extract_data_from_cp_sheet(structured_excel_file):
    data = input_data.extract_data(
        structured_excel_file, "Control Procedures", ["id", "name"]
    )
    assert data == [
        {"id": "CP-123", "name": "User Access Control"},
        {"id": "CP-456", "name": "Network Segmentation"},
    ]


def test_extract_data_from_co_sheet(structured_excel_file):
    data = input_data.extract_data(
        structured_excel_file, "Control Objectives", ["ID", "Objective"]
    )
    assert data == [
        {"ID": "CO-001", "Objective": "To protect endpoint devices from threats."},
        {"ID": "CO-002", "Objective": "To secure data at rest and in transit."},
    ]


def test_construct_sentences_cp(structured_excel_file):
    sentences = input_data.construct_sentences(
        structured_excel_file, "Control Procedures", ["name", "description"]
    )
    assert sentences == [
        "User Access Control Defines how user access is managed.",
        "Network Segmentation Describes network isolation policies.",
    ]


def test_construct_sentences_co(structured_excel_file):
    sentences = input_data.construct_sentences(
        structured_excel_file, "Control Objectives", ["Objective Name", "Objective"]
    )
    assert sentences == [
        "Endpoint Protection To protect endpoint devices from threats.",
        "Data Encryption To secure data at rest and in transit.",
    ]


def test_unsupported_file_type():
    fake_file = Path("fake.csv")
    with pytest.raises(UnsupportedFileTypeError):
        input_data.list_sheets(fake_file)
