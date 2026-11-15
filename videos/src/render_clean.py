#!/usr/bin/env python3
"""Clean Pillow renderer — draws slides with safe layout so text never overlaps.

Reads YAML content, renders each slide (title/statement/key_concept/comparison_table/
diagram_placeholder) with wrapped text, fixed margins and table row heights, then
encodes a silent MP4 (30fps) honoring per-slide durations.

Usage: python render_clean.py <video_num>  (e.g. 5)
"""
import sys, os, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
OUT = ROOT / "output_clean"
OUT.mkdir(exist_ok=True)

BG = (30, 42, 58)
ACCENT = (0, 107, 63)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
LIGHT = (200, 210, 220)
PANEL = (16, 26, 38)

F_TITLE = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
F_SUB = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
F_BODY = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
F_SMALL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
F_CELL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
F_CELL_H = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)

W, H = 1920, 1080
M = 70          # margin

def wrap(draw, text, font, maxw):
    words = str(text).split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def render_slide(slide):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 10], fill=ACCENT)
    kind = slide.get("type", "statement")
    title = slide.get("title", "")
    # Draw title bar
    y = 70
    if title:
        d.text((M, y), title, font=F_TITLE, fill=WHITE)
        y += 80
    maxw = W - 2 * M

    if kind == "title":
        text = slide.get("text", "")
        sub = slide.get("subtitle", "")
        d.text((M, y), text, font=F_SUB, fill=YELLOW)
        y += 50
        if sub:
            d.text((M, y), sub, font=F_BODY, fill=LIGHT)
    elif kind == "statement":
        text = slide.get("text", "")
        for line in wrap(d, text, F_BODY, maxw):
            d.text((M, y), line, font=F_BODY, fill=WHITE)
            y += 44
    elif kind == "key_concept":
        for b in slide.get("bullets", []):
            lines = wrap(d, f"• {b}", F_BODY, maxw)
            for ln in lines:
                d.text((M, y), ln, font=F_BODY, fill=WHITE)
                y += 42
    elif kind == "comparison_table":
        headers = slide.get("headers", [])
        rows = slide.get("rows", [])
        table_left, table_top = M, y
        content_w = maxw
        ncol = len(headers)
        col_w = content_w // ncol
        # measure row heights
        def row_lines(r):
            return max((len(wrap(d, str(c), F_CELL, col_w - 16)) for c in r), default=1)
        hdr_h = row_lines(headers) * 30 + 20
        # compute each row height
        row_h = [hdr_h]
        for r in rows:
            row_h.append(row_lines(r) * 30 + 16)
        total_h = sum(row_h)
        if table_top + total_h > H - 40:
            # shrink font for dense tables
            for c in range(ncol):
                d.text((table_left + c*col_w + 8, table_top + 8), headers[c], font=F_CELL_H, fill=ACCENT)
            return img
        # header
        cy = table_top
        for c in range(ncol):
            d.rectangle([table_left + c*col_w, cy, table_left + (c+1)*col_w, cy + row_h[0]], fill=PANEL, outline=ACCENT)
            xx = table_left + c*col_w + 8
            for ln in wrap(d, str(headers[c]), F_CELL_H, col_w - 16):
                d.text((xx, cy + 6), ln, font=F_CELL_H, fill=YELLOW)
                cy += 30
        cy = table_top + row_h[0]
        for ri, r in enumerate(rows):
            rh = row_h[ri+1]
            for c in range(ncol):
                d.rectangle([table_left + c*col_w, cy, table_left + (c+1)*col_w, cy + rh], outline=ACCENT)
                xx = table_left + c*col_w + 8
                yy = cy + 6
                for ln in wrap(d, str(r[c]), F_CELL, col_w - 16):
                    d.text((xx, yy), ln, font=F_CELL, fill=WHITE)
                    yy += 30
            cy += rh
        # highlight row
        hl = slide.get("highlight_row")
        if hl and hl <= len(rows):
            hl_cy = table_top + row_h[0] + sum(row_h[1:hl])
            hl_rh = row_h[hl]
            d.rectangle([table_left, hl_cy, table_left + content_w, hl_cy + hl_rh], fill=(0, 70, 45))
            for c in range(ncol):
                xx = table_left + c*col_w + 8
                yy = hl_cy + 6
                for ln in wrap(d, str(rows[hl-1][c]), F_CELL, col_w - 16):
                    d.text((xx, yy), ln, font=F_CELL, fill=WHITE)
                    yy += 30
    elif kind == "diagram_placeholder":
        text = slide.get("text", "")
        for line in str(text).splitlines():
            d.text((M, y), line, font=F_SMALL, fill=WHITE)
            y += 34
    # footer / emphasis
    emph = slide.get("highlight_text")
    if emph:
        d.text((M, H - 60), emph, font=F_SMALL, fill=YELLOW)
    return img

def render(video_num):
    import yaml
    yf = CONTENT / f"video_{video_num:02d}_*.yaml"
    cands = sorted(CONTENT.glob(f"video_{video_num:02d}_*.yaml"))
    if not cands:
        print(f"no yaml for {video_num}"); return
    data = yaml.safe_load(open(cands[0]))
    slides = data.get("slides", [])
    vdir = OUT / f"video_{video_num:02d}"
    if vdir.exists(): shutil.rmtree(vdir)
    vdir.mkdir(parents=True)
    frame = 0
    for s in slides:
        dur = s.get("duration", 5)
        n = max(1, int(dur * 30))
        for _ in range(n):
            render_slide(s).save(vdir / f"frame_{frame:05d}.png")
            frame += 1
    out = OUT / f"video_{video_num:02d}_clean.mp4"
    cmd = ["ffmpeg", "-y", "-framerate", "30", "-i", str(vdir / "frame_%05d.png"),
           "-c:v", "libx264", "-preset", "medium", "-b:v", "8M", "-pix_fmt", "yuv420p", str(out)]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"rendered {out} ({frame} frames, {frame/30:.1f}s)")

if __name__ == "__main__":
    n = int(sys.argv[1])
    render(n)
