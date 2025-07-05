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

    parser.add_argument("--border", action="store_true", help="Add border around each photo")
    parser.add_argument("--a4", action="store_true", help="Generate A4 sheets with cropped photos")
    
    parser.add_argument("--size", type=str, help="Final photo size (e.g., 5.5x5.5cm or 55x55mm)")
    parser.add_argument("--text", action="store_true", help="Allow add text")
    parser.add_argument("--left", type=str, default="@CanvaMagnet", help="Left edge vertical text")
    parser.add_argument("--right", type=str, default="+971 545800462", help="Right edge vertical text")
    parser.add_argument("--top", type=str, default="@CanvaMagnet", help="Top edge horizontal text")
    parser.add_argument("--bottom", type=str, default="www.CanvaMagnet.com", help="Bottom edge horizontal text")

    parser.add_argument("-v", "--version", action="version", version=f"SoftCropper {__version__}")

    args = parser.parse_args()

    # Fallback to blur if no mode is specified
    if not args.mode:
        args.mode = "blur"

    # Convert size to pixels if specified
    target_px = None
    if args.size:
        value, unit = args.size.lower().replace("cm", " cm").replace("mm", " mm").split()
        w, h = map(float, value.split("x"))
        factor = 11.81 if unit.strip() == "mm" else 118.1
        target_px = (int(w * factor), int(h * factor))
        
    process_images(
        input_folder=args.input_folder,
        output_folder=args.output_folder,
        mode=args.mode,
        generate_a4=args.a4,
        add_border=args.border,
        target_size=target_px,
        text=args.text,
        left_text=args.left,
        right_text=args.right,
        top_text=args.top,
        bottom_text=args.bottom,
    )

if __name__ == "__main__":
    main()
