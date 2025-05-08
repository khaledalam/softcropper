import sys
from .processor import process_images

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("SoftCropper CLI - Resize images to square with blurred borders")
        print("Usage:")
        print("  softcropper <input_folder> [output_folder (optional)]")
        print()
        print("Example:")
        print("  softcropper ./input_photos ./output_ready")
        sys.exit(0)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else None
    process_images(input_folder, output_folder)