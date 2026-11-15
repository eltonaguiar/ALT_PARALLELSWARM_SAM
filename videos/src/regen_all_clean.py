#!/usr/bin/env python3
"""Regenerate ALL 12 SAM videos with the safe non-overlapping Pillow renderer,
then mux narration audio -> docs/sam-videos/videos/video_XX_clean.mp4"""
import sys, os, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
TMP = ROOT / "output_clean"
DEST = ROOT.parent / "docs/sam-videos/videos"
TMP.mkdir(exist_ok=True)
DEST.mkdir(exist_ok=True)

BG = (30, 42, 58); ACCENT = (0, 107, 63)
WHITE = (255, 255, 255); YELLOW = (255, 215, 0); LIGHT = (200, 210, 220); PANEL = (16, 26, 38)

F_TITLE = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
F_SUB = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
F_BODY = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
F_SMALL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
F_CELL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 21)
F_CELL_H = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 21)

W, H = 1920, 1080; M = 70

def wrap(draw, text, font, maxw):
    words = str(text).split(); lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def render_slide(slide):
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 10], fill=ACCENT)
    kind = slide.get("type", "statement"); title = slide.get("title", "")
    y = 70
    if title:
        d.text((M, y), title, font=F_TITLE, fill=WHITE); y += 80
    maxw = W - 2 * M
    if kind == "title":
        d.text((M, y), slide.get("text",""), font=F_SUB, fill=YELLOW); y += 50
        if slide.get("subtitle"): d.text((M, y), slide["subtitle"], font=F_BODY, fill=LIGHT)
    elif kind == "statement":
        for line in wrap(d, slide.get("text",""), F_BODY, maxw):
            d.text((M, y), line, font=F_BODY, fill=WHITE); y += 44
    elif kind == "key_concept":
        for b in slide.get("bullets", []):
            for ln in wrap(d, f"• {b}", F_BODY, maxw):
                d.text((M, y), ln, font=F_BODY, fill=WHITE); y += 42
    elif kind == "comparison_table":
        headers = slide.get("headers", []); rows = slide.get("rows", [])
        tl, tt = M, y; cw = maxw // len(headers)
        def rlines(r): return max((len(wrap(d, str(c), F_CELL, cw - 16)) for c in r), default=1)
        hdr_h = rlines(headers) * 28 + 18
        row_h = [hdr_h] + [rlines(r) * 28 + 14 for r in rows]
        cy = tt
        for c in range(len(headers)):
            d.rectangle([tl + c*cw, cy, tl + (c+1)*cw, cy + row_h[0]], fill=PANEL, outline=ACCENT)
            xx = tl + c*cw + 8; yy = cy + 5
            for ln in wrap(d, str(headers[c]), F_CELL_H, cw - 16):
                d.text((xx, yy), ln, font=F_CELL_H, fill=YELLOW); yy += 28
        cy += row_h[0]
        for ri, r in enumerate(rows):
            rh = row_h[ri+1]
            for c in range(len(headers)):
                d.rectangle([tl + c*cw, cy, tl + (c+1)*cw, cy + rh], outline=ACCENT)
                xx = tl + c*cw + 8; yy = cy + 5
                for ln in wrap(d, str(r[c]), F_CELL, cw - 16):
                    d.text((xx, yy), ln, font=F_CELL, fill=WHITE); yy += 28
            cy += rh
        hl = slide.get("highlight_row")
        if hl and hl <= len(rows):
            hcy = tt + row_h[0] + sum(row_h[1:hl]); hrh = row_h[hl]
            d.rectangle([tl, hcy, tl + maxw, hcy + hrh], fill=(0, 70, 45))
            for c in range(len(headers)):
                xx = tl + c*cw + 8; yy = hcy + 5
                for ln in wrap(d, str(rows[hl-1][c]), F_CELL, cw - 16):
                    d.text((xx, yy), ln, font=F_CELL, fill=WHITE); yy += 28
    elif kind == "diagram_placeholder":
        for line in str(slide.get("text","")).splitlines():
            d.text((M, y), line, font=F_SMALL, fill=WHITE); y += 34
    if slide.get("highlight_text"):
        d.text((M, H - 60), slide["highlight_text"], font=F_SMALL, fill=YELLOW)
    return img

def render(video_num):
    cands = sorted(CONTENT.glob(f"video_{video_num:02d}_*.yaml"))
    if not cands: print(f"no yaml for {video_num}"); return None
    data = yaml.safe_load(open(cands[0])); slides = data.get("slides", [])
    vdir = TMP / f"video_{video_num:02d}"
    if vdir.exists(): shutil.rmtree(vdir)
    vdir.mkdir(parents=True)
    frame = 0
    for s in slides:
        dur = s.get("duration", 5); n = max(1, int(dur * 30))
        for _ in range(n):
            render_slide(s).save(vdir / f"frame_{frame:05d}.png"); frame += 1
    silent = TMP / f"video_{video_num:02d}_silent.mp4"
    subprocess.run(["ffmpeg","-y","-framerate","30","-i",str(vdir/"frame_%05d.png"),
                    "-c:v","libx264","-preset","medium","-b:v","8M","-pix_fmt","yuv420p",str(silent)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    nar = ROOT/"output_narration"/f"video_{video_num:02d}_narration.wav"
    final = DEST / f"video_{video_num:02d}_clean.mp4"
    if nar.exists():
        subprocess.run(["ffmpeg","-y","-i",str(silent),"-i",str(nar),"-map","0:v","-map","1:a",
                        "-c:v","copy","-c:a","aac","-b:a","192k","-shortest",str(final)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        shutil.copy(silent, final)
    print(f"✓ video_{video_num:02d}_clean.mp4 ({frame/30:.0f}s)")

if __name__ == "__main__":
    nums = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(1, 13))
    for n in nums: render(n)
    print("done")
