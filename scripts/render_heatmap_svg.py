import os
import json
from datetime import datetime

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap_svg(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)

    width = 860
    height = 205
    box_size = 11
    box_gap = 3.5
    start_x = 35
    start_y = 48

    # Process days into weeks (53 columns x 7 rows)
    weeks = []
    current_week = []
    
    for d in days:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        day_of_week = (dt.weekday() + 1) % 7 # 0 = Sun, 1 = Mon, ..., 6 = Sat
        
        if day_of_week == 0 and current_week:
            weeks.append(current_week)
            current_week = []
        current_week.append(d)

    if current_week:
        weeks.append(current_week)

    # Limit to 53 weeks
    weeks = weeks[-53:]

    # Build SVG
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg.append('  <style>')
    svg.append('    .bg { fill: #0d1117; rx: 8px; stroke: #30363d; stroke-width: 1px; }')
    svg.append('    .title-bar { fill: #161b22; }')
    svg.append('    .title-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace; font-size: 13px; fill: #8b949e; font-weight: 600; }')
    svg.append('    .label-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10px; fill: #7d8590; }')
    svg.append('    .stats-text { font-family: "Fira Code", Consolas, monospace; font-size: 11px; fill: #3fb950; font-weight: 600; }')
    svg.append('    .dot-red { fill: #ff5f56; }')
    svg.append('    .dot-yellow { fill: #ffbd2e; }')
    svg.append('    .dot-green { fill: #27c93f; }')
    svg.append('    .day-box { rx: 2.5px; }')
    svg.append('  </style>')

    # Outer container
    svg.append(f'  <rect width="{width}" height="{height}" class="bg"/>')

    # Header bar
    svg.append(f'  <path d="M 0 8 Q 0 0 8 0 L {width-8} 0 Q {width} 0 {width} 8 L {width} 34 L 0 34 Z" class="title-bar"/>')
    svg.append(f'  <line x1="0" y1="34" x2="{width}" y2="34" stroke="#30363d" stroke-width="1"/>')
    svg.append('  <circle cx="18" cy="17" r="5.5" class="dot-red"/>')
    svg.append('  <circle cx="36" cy="17" r="5.5" class="dot-yellow"/>')
    svg.append('  <circle cx="54" cy="17" r="5.5" class="dot-green"/>')
    svg.append(f'  <text x="74" y="21" class="title-text">kartik@github ~ ./contributions.sh --year 2026</text>')

    # Weekday labels on left
    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for lbl, row_idx in day_labels:
        y_pos = start_y + row_idx * (box_size + box_gap) + 9
        svg.append(f'  <text x="10" y="{y_pos}" class="label-text">{lbl}</text>')

    # Render Month Labels
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    last_month = -1
    for w_idx, week in enumerate(weeks):
        if week:
            dt = datetime.strptime(week[0]["date"], "%Y-%m-%d")
            if dt.month != last_month:
                last_month = dt.month
                x_pos = start_x + w_idx * (box_size + box_gap)
                svg.append(f'  <text x="{x_pos}" y="{start_y - 8}" class="label-text">{month_names[dt.month - 1]}</text>')

    # Render Heatmap Cells
    for w_idx, week in enumerate(weeks):
        x_pos = start_x + w_idx * (box_size + box_gap)
        for d_idx, d in enumerate(week):
            dt = datetime.strptime(d["date"], "%Y-%m-%d")
            row_idx = (dt.weekday() + 1) % 7
            y_pos = start_y + row_idx * (box_size + box_gap)
            
            level = min(d.get("level", 0), 5)
            color = PALETTE[level]

            svg.append(f'  <rect x="{round(x_pos,1)}" y="{round(y_pos,1)}" width="{box_size}" height="{box_size}" fill="{color}" class="day-box">')
            svg.append(f'    <title>{d["count"]} contributions on {d["date"]}</title>')
            svg.append('  </rect>')

    # Footer Statistics & Legend
    footer_y = height - 16
    svg.append(f'  <text x="12" y="{footer_y}" class="stats-text">⚡ {total_contribs:,} contributions in last year | Streak: {current_streak} days (Max: {longest_streak})</text>')

    # Legend on bottom right
    legend_x = width - 150
    svg.append(f'  <text x="{legend_x - 32}" y="{footer_y}" class="label-text">Less</text>')
    for idx, col in enumerate(PALETTE):
        lx = legend_x + idx * 14
        svg.append(f'  <rect x="{lx}" y="{footer_y - 9}" width="10" height="10" rx="2" fill="{col}"/>')
    svg.append(f'  <text x="{legend_x + len(PALETTE) * 14 + 6}" y="{footer_y}" class="label-text">More</text>')

    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Generated heatmap SVG at {output_path}")

if __name__ == "__main__":
    render_heatmap_svg()
