import os
import shutil
from pathlib import Path
import cv2
import numpy as np
import pytest
from softcropper.processor import process_images

ASSET_FILES = ["baby.webp", "kid.jpg"]
TEXT_KWARGS = {
    "left_text": "Left",
    "right_text": "Right",
    "top_text": "Top",
    "bottom_text": "Bottom"
}


def setup_test_assets(tmp_path):
    assets_dir = Path(__file__).parent / "assets"
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    for file_name in ASSET_FILES:
        shutil.copy(assets_dir / file_name, input_dir / file_name)
    return input_dir


def validate_output_images(output_dir, expected_count):
    assert output_dir.exists(), "Output folder was not created"
    output_files = list(output_dir.glob("*"))
    assert len(output_files) == expected_count, f"Expected {expected_count} images, got {len(output_files)}"
    for file in output_files:
        assert file.stat().st_size > 0, f"{file.name} is empty or corrupted"


def test_default_processing(tmp_path):
    input_dir = setup_test_assets(tmp_path)
    process_images(str(input_dir))
    output_dir = input_dir / "output"
    validate_output_images(output_dir, len(ASSET_FILES))


def test_with_border_and_text(tmp_path):
    input_dir = setup_test_assets(tmp_path)
    process_images(
        str(input_dir),
        add_border=True,
        text=True,
        **TEXT_KWARGS
    )
    output_dir = input_dir / "output"
    validate_output_images(output_dir, len(ASSET_FILES))


def test_with_resize_mm(tmp_path):
    input_dir = setup_test_assets(tmp_path)
    # 55x55mm in pixels ≈ 649x649
    process_images(
        str(input_dir),
        target_size=(649, 649)
    )
    output_dir = input_dir / "output"
    validate_output_images(output_dir, len(ASSET_FILES))
    for img_path in output_dir.glob("*"):
        img = cv2.imread(str(img_path))
        assert img.shape[:2] == (649, 649), f"{img_path.name} size is incorrect: {img.shape}"


def test_with_generate_a4(tmp_path):
    input_dir = setup_test_assets(tmp_path)
    process_images(
        str(input_dir),
        add_border=True,
        generate_a4=True,
        text=True,
        **TEXT_KWARGS
    )
    a4_folder = input_dir / "output" / "A4"
    assert a4_folder.exists(), "A4 folder was not created"
    a4_pages = list(a4_folder.glob("*.jpg"))
    assert len(a4_pages) >= 1, "No A4 page was generated"
    for page in a4_pages:
        img = cv2.imread(str(page))
        assert img is not None and img.size > 0, f"A4 page {page.name} is empty"


@pytest.mark.parametrize("mode", ["blur", "solid", "gradient"])
def test_all_border_modes(tmp_path, mode):
    input_dir = setup_test_assets(tmp_path)
    process_images(str(input_dir), mode=mode, add_border=True)
    output_dir = input_dir / "output"
    validate_output_images(output_dir, len(ASSET_FILES))
