import os
import shutil
from pathlib import Path
from softcropper.processor import process_images

def test_process_images_with_real_photos(tmp_path):
    assets_dir = Path(__file__).parent / "assets"
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    # Copy test images to temp input folder
    for file_name in ["baby.webp", "kid.jpg"]:
        shutil.copy(assets_dir / file_name, input_dir / file_name)

    # Run processing
    process_images(str(input_dir))

    output_dir = input_dir / "output"
    assert output_dir.exists(), "Output folder was not created"

    output_files = list(output_dir.glob("*"))
    assert len(output_files) == 2, "Not all images were processed"

    for file in output_files:
        assert file.stat().st_size > 0, f"{file.name} is empty or corrupted"

    print(f"✅ Test passed: Processed {len(output_files)} real images")
