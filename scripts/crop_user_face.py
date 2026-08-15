import os
from PIL import Image

def crop_user_face():
    img_path = r"C:\Users\hp\.gemini\antigravity-ide\brain\830e6c5b-ac21-4797-9c02-7473e102d3fb\.user_uploaded\media_1786796319031.png"
    if not os.path.exists(img_path):
        print("User uploaded image not found")
        return

    img = Image.open(img_path)
    w, h = img.size
    print(f"Original screenshot size: {w}x{h}")

    # Crop avatar area from the left column of GitHub profile screenshot
    # The avatar circle in the screenshot media_1786796319031.png
    # Bounding box coordinates for the circular profile picture
    left = int(w * 0.02)
    top = int(h * 0.14)
    right = int(w * 0.31)
    bottom = int(h * 0.44)

    avatar = img.crop((left, top, right, bottom))
    output_path = "source-photo.jpg"
    avatar.convert("RGB").save(output_path, quality=95)
    print(f"Cropped user face saved to {output_path}")

if __name__ == "__main__":
    crop_user_face()
