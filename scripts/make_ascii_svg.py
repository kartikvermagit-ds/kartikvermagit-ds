import os
import sys
import cv2
import numpy as np

# Crisp density ramp from bright (space) to dark (@)
RAMP = " .`:-=+*cs#%@"

def make_ascii_svg(image_path="source-prepped.png", output_path="kartik-ascii.svg", cols=95, aspect_ratio_correction=0.55):
    if not os.path.exists(image_path):
        if os.path.exists("source-photo.jpg"):
            image_path = "source-photo.jpg"
        else:
            print(f"Error: {image_path} not found.")
            sys.exit(1)

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Failed to read image {image_path}")
        sys.exit(1)

    h, w = img.shape
    rows = int((h / w) * cols * aspect_ratio_correction)
    resized = cv2.resize(img, (cols, rows), interpolation=cv2.INTER_AREA)

    ascii_rows = []
    ramp_len = len(RAMP)
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            val = resized[r, c]
            # Map brightness 255 -> 0 (space), dark 0 -> RAMP[-1]
            idx = int((255 - val) / 255.0 * (ramp_len - 1))
            char = RAMP[idx]
            # XML escape
            if char == '<': char = '&lt;'
            elif char == '>': char = '&gt;'
            elif char == '&': char = '&amp;'
            elif char == '"': char = '&quot;'
            elif char == ' ': char = '&#160;'
            row_chars.append(char)
        ascii_rows.append("".join(row_chars))

    # SVG dimensions
    font_size = 7.5
    line_height = 8.5
    char_width = 4.4
    svg_width = int(cols * char_width + 16)
    svg_height = int(rows * line_height + 20)

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; rx: 8px; stroke: #30363d; stroke-width: 1px; }')
    svg.append('    .ascii-text { font-family: "Fira Code", "Courier New", Consolas, monospace; font-size: 7.5px; fill: #c9d1d9; letter-spacing: 0px; white-space: pre; }')
    svg.append('  </style>')

    # Outer border/container
    svg.append(f'  <rect width="100%" height="100%" class="bg"/>')

    # Render ASCII rows cleanly
    svg.append('  <g class="ascii-text">')
    for i, row_str in enumerate(ascii_rows):
        y_pos = round(14 + i * line_height, 1)
        svg.append(f'    <text x="10" y="{y_pos}">{row_str}</text>')
    svg.append('  </g>')
    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Generated ASCII SVG at {output_path} ({cols}x{rows})")

if __name__ == "__main__":
    make_ascii_svg()
