import os
import sys
from PIL import Image  # Fixed import (PTL -> PIL)
import argparse  # Fixed import (angparse -> argparse)

def resize_image(img, target_size):
    """Resize image while maintaining aspect ratio"""
    img.thumbnail(target_size, Image.LANCZOS)
    return img

def convert_image(img, output_format):
    """Convert image to specified format if requested"""
    if output_format:  # Fixed syntax error (space removed)
        # Convert to RGB for JPG format
        return img.convert("RGB") if output_format in ["JPG", "JPEG"] else img
    return img

def process_images(input_folder, output_folder, target_size, output_format=None):
    """
    Process all images in input folder:
    1. Resize to target size while maintaining aspect ratio
    2. Convert to specified format
    3. Save to output folder
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    processed = 0
    skipped = 0
    supported_formats = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif']
    
    print(f"\n{'*' * 50}")
    print(f"Processing images from: {input_folder}")
    print(f"Target size: {target_size[0]}x{target_size[1]}")
    print(f"Output format: {output_format if output_format else 'Original'}")
    print(f"{'*' * 50}\n")
    
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        
        # Skip directories and unsupported files
        if not os.path.isfile(input_path):
            continue
            
        ext = os.path.splitext(filename)[1].lower()
        if ext not in supported_formats:
            skipped += 1
            print(f"Skipped {filename}: Unsupported file format")
            continue
            
        try:
            with Image.open(input_path) as img:
                # Process image
                img = resize_image(img, target_size)
                img = convert_image(img, output_format)
                
                # Create output filename
                name, _ = os.path.splitext(filename)
                new_ext = f".{output_format.lower()}" if output_format else ext
                output_filename = f"{name}{new_ext}"
                output_path = os.path.join(output_folder, output_filename)
                
                # Save with format conversion if requested
                save_format = output_format if output_format else img.format
                img.save(output_path, format=save_format)
                
            processed += 1
            print(f"Processed: {filename} -> {output_filename}")
                
        except (IOError, OSError, Image.DecompressionBombError) as e:
            skipped += 1
            print(f"Error processing {filename}: {str(e)}")
    
    print(f"\n{'=' * 50}")
    print(f"Processing complete!")
    print(f"Processed: {processed} images")
    print(f"Skipped: {skipped} files")
    print(f"Output folder: {os.path.abspath(output_folder)}")
    print(f"{'=' * 50}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Batch Image Resizer and Converter',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-i', '--input', default='input', 
                        help='Input folder containing images')
    parser.add_argument('-o', '--output', default='output',
                        help='Output folder for processed images')
    parser.add_argument('-s', '--size', default=[800, 600], type=int, nargs=2,
                        metavar=('WIDTH', 'HEIGHT'),  # Fixed typo (MIDTH -> WIDTH)
                        help='Target size (width height)')
    parser.add_argument('-f', '--format', 
                        help='Output format (e.g., jpg, png, webp)')
    
    args = parser.parse_args()
    
    # Convert format to uppercase if provided
    output_format = args.format.upper() if args.format else None
    
    # Handle JPG/JPEG aliases
    if output_format in ['JPG', 'JPEG']:
        output_format = 'JPEG'
    
    process_images(
        input_folder=args.input,
        output_folder=args.output,
        target_size=tuple(args.size),
        output_format=output_format
    )