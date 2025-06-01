import argparse
from .processor import process_images
from . import __version__

def main():
    parser = argparse.ArgumentParser(description="SoftCropper CLI - Resize images to square with blurred, solid, or gradient borders")

    parser.add_argument("input_folder", help="Path to input folder (required)")
    parser.add_argument("--output", dest="output_folder", help="Optional path to output folder")

    # Mutually exclusive group for -b, -s, -g and --mode
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("-b", action="store_const", dest="mode", const="blur", help="Use blur borders")
    mode_group.add_argument("-s", action="store_const", dest="mode", const="solid", help="Use solid borders")
    mode_group.add_argument("-g", action="store_const", dest="mode", const="gradient", help="Use gradient borders")
    parser.add_argument("--mode", choices=["blur", "solid", "gradient"], dest="mode", help="Explicitly set border mode")

    parser.add_argument("-v", "--version", action="version", version=f"SoftCropper {__version__}")

    args = parser.parse_args()

    # Fallback to blur if no mode is specified
    if not args.mode:
        args.mode = "blur"

    process_images(args.input_folder, args.output_folder, args.mode)

if __name__ == "__main__":
    main()
