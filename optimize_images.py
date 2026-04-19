#!/usr/bin/env python3
import os
from PIL import Image
import glob

# Image directory
img_dir = "images"

# Settings
MAX_WIDTH = 2000
QUALITY = 75
WEBP_QUALITY = 80

def optimize_image(img_path):
    try:
        img = Image.open(img_path)
        original_size = os.path.getsize(img_path)

        # Resize if too large
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

        # Convert RGBA to RGB if needed (for JPG)
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img

        # Save optimized JPG
        if img_path.lower().endswith(('.jpg', '.jpeg')):
            img.save(img_path, 'JPEG', quality=QUALITY, optimize=True)
        elif img_path.lower().endswith('.png'):
            img.save(img_path, 'PNG', optimize=True)

        new_size = os.path.getsize(img_path)
        reduction = ((original_size - new_size) / original_size) * 100
        print(f"✓ {os.path.basename(img_path)}: {original_size/1024/1024:.1f}MB → {new_size/1024/1024:.1f}MB (-{reduction:.0f}%)")

    except Exception as e:
        print(f"✗ Error with {img_path}: {e}")

# Process all images
print("Optimizing images...")
for img_path in glob.glob(os.path.join(img_dir, "*.*")):
    if img_path.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        optimize_image(img_path)

print("\nDone! Images optimized.")
