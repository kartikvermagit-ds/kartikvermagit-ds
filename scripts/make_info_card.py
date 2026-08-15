import os

def make_info_card(output_path="info-card.svg"):
    width = 490
    height = 472

    card_data = [
        ("USER", "kartikvermagit-ds (Kartik Verma)", "#58a6ff"),
        ("ROLE", "B.Tech CSE (Data Science) Student", "#79c0ff"),
        ("LOCATION", "Kanpur, UP, India 🇮🇳", "#a5d6ff"),
        ("EMAIL", "kv5612872@gmail.com", "#7ee787"),
        ("NOW", "B.Tech CS-DS | Web Dev & Open Source", "#56d364"),
        ("PREV", "C Programming & Data Structures Basics", "#e3b341"),
        ("STACK", "Python, C, JavaScript, TypeScript, HTML, CSS, Git", "#bc8cff"),
        ("HIGHLIGHTS", "23 Public Repos | Problem Solver (PSA)", "#ff7b72"),
        ("SOCIALS", "LinkedIn: in/kartik-verma-ds | IG: kv561287", "#ffa657")
    ]

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; rx: 8px; stroke: #30363d; stroke-width: 1px; }')
    svg.append('    .title-bar { fill: #161b22; }')
    svg.append('    .title-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; font-size: 13px; fill: #8b949e; font-weight: 600; }')
    svg.append('    .dot-red { fill: #ff5f56; }')
    svg.append('    .dot-yellow { fill: #ffbd2e; }')
    svg.append('    .dot-green { fill: #27c93f; }')
    svg.append('    .term-text { font-family: "Fira Code", Consolas, "Courier New", monospace; font-size: 12.5px; font-weight: 500; }')
    svg.append('    .label { fill: #8b949e; font-weight: 600; }')
    svg.append('    .prompt { fill: #3fb950; font-weight: 700; }')
    svg.append('  </style>')

    # Card background
    svg.append(f'  <rect width="{width}" height="{height}" class="bg"/>')

    # Header title bar
    svg.append(f'  <path d="M 0 8 Q 0 0 8 0 L {width-8} 0 Q {width} 0 {width} 8 L {width} 36 L 0 36 Z" class="title-bar"/>')
    svg.append('  <line x1="0" y1="36" x2="490" y2="36" stroke="#30363d" stroke-width="1"/>')
    
    # Terminal control dots
    svg.append('  <circle cx="18" cy="18" r="6" class="dot-red"/>')
    svg.append('  <circle cx="38" cy="18" r="6" class="dot-yellow"/>')
    svg.append('  <circle cx="58" cy="18" r="6" class="dot-green"/>')
    svg.append('  <text x="78" y="22" class="title-text">kartik@github ~ neofetch --user kartikvermagit-ds</text>')

    # Terminal prompt & body content
    svg.append('  <g class="term-text" transform="translate(20, 58)">')
    
    # OS / Host ascii banner small header
    svg.append('    <text x="0" y="0" class="prompt">kartik@developer-laptop</text>')
    svg.append('    <text x="180" y="0" fill="#484f58">-----------------------</text>')

    y_start = 26
    row_height = 43
    for i, (key, value, val_color) in enumerate(card_data):
        y = y_start + i * row_height
        svg.append('    <g>')
        # Label block
        svg.append(f'      <text x="0" y="{y}" class="label">{key.ljust(11)}:</text>')
        # Value block
        val_display = value[:45] + "..." if len(value) > 48 else value
        svg.append(f'      <text x="105" y="{y}" fill="{val_color}">{val_display}</text>')
        svg.append('    </g>')

    svg.append('  </g>')
    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Generated info card SVG at {output_path}")

if __name__ == "__main__":
    make_info_card()
