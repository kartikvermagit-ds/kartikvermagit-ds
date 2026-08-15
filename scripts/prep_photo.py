import sys
import os
import cv2
import numpy as np
from PIL import Image

def prep_photo(image_path="source-photo.jpg", output_path="source-prepped.png"):
    if not os.path.exists(image_path):
        print(f"Error: {image_path} does not exist.")
        sys.exit(1)

    print(f"Loading {image_path}...")
    img = Image.open(image_path).convert("RGBA")

    # Try background removal with rembg, fallback if rembg model download is slow or unavailable
    try:
        from rembg import remove
        print("Removing background with rembg...")
        nobg = remove(img)
    except Exception as e:
        print(f"rembg notice ({e}), proceeding with original image mask...")
        nobg = img

    # Convert PIL Image to OpenCV numpy array
    nobg_np = np.array(nobg)

    # Extract RGB and Alpha
    if nobg_np.shape[2] == 4:
        r, g, b, a = cv2.split(nobg_np)
        alpha = a / 255.0
    else:
        r, g, b = cv2.split(nobg_np)
        alpha = np.ones(r.shape, dtype=float)

    bgr = cv2.merge([b, g, r])
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE for high local contrast
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(gray)

    # Composite enhanced subject onto pure white background (255)
    white_bg = np.ones_like(enhanced_gray) * 255
    composite = (enhanced_gray * alpha + white_bg * (1.0 - alpha)).astype(np.uint8)

    # Save prepped image
    cv2.imwrite(output_path, composite)
    print(f"Prepped photo saved to {output_path}")

if __name__ == "__main__":
    img_arg = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(img_arg)
