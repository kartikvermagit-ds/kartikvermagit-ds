import os
import sys
import cv2
import numpy as np
from PIL import Image

def prep_photo(image_path="source-photo.jpg", output_path="source-prepped.png"):
    if not os.path.exists(image_path):
        print(f"Error: {image_path} does not exist.")
        sys.exit(1)

    print(f"Loading {image_path}...")
    img = Image.open(image_path).convert("RGB")
    
    # Resize to manageable high-def dimensions while keeping aspect ratio
    img.thumbnail((800, 1000), Image.Resampling.LANCZOS)
    img_np = np.array(img)

    # Convert to BGR for OpenCV
    bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    # 1. Clean background: background in original photo is plain off-white (brightness > 215)
    # Map all background pixels to pure 255 (white)
    mask_bg = gray > 215
    
    # 2. Apply CLAHE on subject for balanced midtones and facial expression detail
    clahe = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # 3. Gamma correction to make facial details (eyes, smile, hair) crisp
    gamma = 1.15
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    enhanced = cv2.LUT(enhanced, table)

    # Apply pure white background
    enhanced[mask_bg] = 255

    cv2.imwrite(output_path, enhanced)
    print(f"Prepped photo saved to {output_path}")

if __name__ == "__main__":
    img_arg = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(img_arg)
