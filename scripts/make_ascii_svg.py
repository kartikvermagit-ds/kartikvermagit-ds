import os
import sys
import cv2
import numpy as np

RAMP = " .`:-=+*cs#%@"  # Bright (255 -> space) to dark (0 -> @)

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

    # SVG geometry dimensions
    font_size = 7.5
    line_height = 8.5
    char_width = 4.4
    svg_width = int(cols * char_width + 16)
    svg_height = int(rows * line_height + 20)

    # SMIL animation calculation
    total_duration = 3.5  # seconds
    row_delay = total_duration / max(1, rows)

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; rx: 8px; }')
    svg.append('    .ascii-text { font-family: "Fira Code", "Courier New", Consolas, monospace; font-size: 7.5px; fill: #c9d1d9; letter-spacing: 0px; white-space: pre; }')
    svg.append('    .cursor { fill: #58a6ff; }')
    svg.append('  </style>')

    # Clip Paths for row-by-row left-to-right typing effect
    svg.append('  <defs>')
    for i in range(rows):
        begin_t = round(i * row_delay, 2)
        dur_t = 0.12
        svg.append(f'    <clipPath id="clip-{i}">')
        svg.append(f'      <rect x="0" y="{i * line_height}" width="0" height="{line_height + 2}">')
        svg.append(f'        <animate attributeName="width" from="0" to="{svg_width}" begin="{begin_t}s" dur="{dur_t}s" fill="freeze" />')
        svg.append('      </rect>')
        svg.append('    </clipPath>')
    svg.append('  </defs>')

    # Outer border/container
    svg.append(f'  <rect width="100%" height="100%" class="bg" stroke="#30363d" stroke-width="1"/>')

    # Render animated ASCII rows
    svg.append('  <g class="ascii-text">')
    for i, row_str in enumerate(ascii_rows):
        y_pos = round(14 + i * line_height, 1)
        begin_t = round(i * row_delay, 2)
        dur_t = 0.12
        
        # Row text clipped left to right
        svg.append(f'    <g clip-path="url(#clip-{i})">')
        svg.append(f'      <text x="10" y="{y_pos}">{row_str}</text>')
        svg.append('    </g>')

        # Block cursor riding the wipe edge
        svg.append(f'    <rect class="cursor" y="{y_pos - 6.5}" width="5" height="7.5">')
        svg.append(f'      <animate attributeName="x" from="10" to="{svg_width - 10}" begin="{begin_t}s" dur="{dur_t}s" fill="freeze" />')
        svg.append(f'      <animate attributeName="opacity" values="1;1;0" keyTimes="0;0.99;1" begin="{begin_t}s" dur="{dur_t + 0.05}s" fill="freeze" />')
        svg.append('    </rect>')

    svg.append('  </g>')
    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Generated ASCII SVG at {output_path} ({cols}x{rows})")

if __name__ == "__main__":
    make_ascii_svg()
