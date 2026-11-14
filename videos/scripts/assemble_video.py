#!/usr/bin/env python3
"""
SAM Video Series - Video Assembly Pipeline
Converts PPTX slides to MP4 video using LibreOffice + MoviePy + FFmpeg
"""

import os
import subprocess
import shutil
from pathlib import Path
from moviepy import ImageSequenceClip, concatenate_videoclips, ColorClip
import json

# ─── Configuration ───
SLIDE_DURATIONS = {
    'title': 3,
    'statement': 5,
    'definition': 8,
    'comparison_table': 12,
    'diagram_placeholder': 10,
    'key_concept': 12,
    'next_video': 3,
}

DEFAULT_SLIDE_DURATION = 5
FPS = 30
RESOLUTION = (1920, 1080)  # 1080p output
TEMP_DIR = Path("temp_frames")
OUTPUT_DIR = Path("output_mp4")

def pptx_to_png(pptx_path, output_dir):
    """Convert PPTX to PNG frames using LibreOffice headless."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # LibreOffice converts to PDF first, then we can extract pages
    # Or use unoconv if available
    cmd = [
        "libreoffice", "--headless", "--convert-to", "pdf",
        "--outdir", str(output_dir), str(pptx_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice PDF conversion failed: {result.stderr}")
    
    # Find the generated PDF
    pdf_files = list(output_dir.glob("*.pdf"))
    if not pdf_files:
        raise RuntimeError("No PDF generated")
    pdf_path = pdf_files[0]
    
    # Convert PDF pages to PNG using pdftoppm (poppler-utils)
    cmd = ["pdftoppm", "-png", "-r", "150", str(pdf_path), str(output_dir / "slide")]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"pdftoppm failed: {result.stderr}")
    
    # Get sorted PNG files
    png_files = sorted(output_dir.glob("slide-*.png"))
    if not png_files:
        png_files = sorted(output_dir.glob("slide*.png"))
    
    # Clean up PDF
    pdf_path.unlink()
    
    return png_files

def load_slide_durations(yaml_path):
    """Load slide durations from YAML content file."""
    import yaml
    with open(yaml_path, 'r') as f:
        content = yaml.safe_load(f)
    
    durations = {}
    for slide in content['slides']:
        slide_type = slide['type']
        duration = slide.get('duration', DEFAULT_SLIDE_DURATION)
        durations[slide['id']] = duration
    return durations

def create_video_from_slides(png_files, durations, output_path, fps=FPS):
    """Create video from PNG frames with specified durations."""
    clips = []
    
    for i, png_file in enumerate(png_files):
        slide_num = i + 1
        # Try to match duration from YAML (approximate by order)
        duration = DEFAULT_SLIDE_DURATION
        # For now use default; could map by slide content analysis
        clip = ImageSequenceClip([str(png_file)], fps=fps).set_duration(duration)
        clips.append(clip)
    
    if not clips:
        raise ValueError("No clips to compose")
    
    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(
        str(output_path),
        fps=fps,
        codec='libx264',
        audio=False,
        preset='medium',
        threads=4
    )
    
    for clip in clips:
        clip.close()
    final_clip.close()

def create_video_with_ffmpeg(png_dir, durations, output_path, fps=FPS):
    """Alternative: Use FFmpeg directly for better control and NVENC."""
    # Create a concat file for FFmpeg
    concat_file = png_dir / "concat.txt"
    png_files = sorted(png_dir.glob("slide-*.png"))
    if not png_files:
        png_files = sorted(png_dir.glob("slide*.png"))
    
    with open(concat_file, 'w') as f:
        for i, png_file in enumerate(png_files):
            duration = DEFAULT_SLIDE_DURATION  # Could map from YAML
            f.write(f"file '{png_file.name}'\n")
            f.write(f"duration {duration}\n")
        # Repeat last frame
        if png_files:
            f.write(f"file '{png_files[-1].name}'\n")
    
    # FFmpeg command with NVENC hardware encoding (try NVENC first, fallback to libx264)
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-vf", f"fps={fps},scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264",
        "-preset", "medium",
        "-b:v", "8M",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        # Fallback to software encoding
        cmd[-6] = "libx264"
        cmd[-5] = "medium"
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {result.stderr}")
    
    return output_path

def process_video(video_num, pptx_path, yaml_path, output_dir):
    """Process a single video: PPTX -> PNG -> MP4."""
    print(f"\n=== Processing Video {video_num} ===")
    
    temp_frames = TEMP_DIR / f"video_{video_num:02d}"
    if temp_frames.exists():
        shutil.rmtree(temp_frames)
    
    try:
        # Step 1: PPTX -> PNG
        print(f"  Converting PPTX to PNG...")
        png_files = pptx_to_png(pptx_path, temp_frames)
        print(f"  Generated {len(png_files)} frames")
        
        # Step 2: Load durations from YAML
        durations = load_slide_durations(yaml_path)
        print(f"  Loaded durations: {durations}")
        
        # Step 3: Create MP4
        output_path = output_dir / f"video_{video_num:02d}.mp4"
        print(f"  Creating MP4: {output_path}")
        create_video_with_ffmpeg(temp_frames, durations, output_path)
        
        # Verify output
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024*1024)
            print(f"  ✓ Success: {size_mb:.1f} MB")
            return True
        else:
            print(f"  ✗ Failed: Output not created")
            return False
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False
    finally:
        # Cleanup temp frames
        if temp_frames.exists():
            shutil.rmtree(temp_frames)

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Process all 12 videos
    success_count = 0
    for i in range(1, 13):
        # Find PPTX and YAML files
        pptx_files = list(Path("output").glob(f"video_{i:02d}*.pptx"))
        if not pptx_files:
            pptx_files = list(Path("output").glob(f"video_{i}_*.pptx"))
        
        yaml_files = list(Path("content").glob(f"video_{i:02d}_*.yaml"))
        if not yaml_files:
            yaml_files = list(Path("content").glob(f"video_{i}_*.yaml"))
        
        if not pptx_files or not yaml_files:
            print(f"Video {i}: Missing PPTX or YAML file")
            continue
        
        success = process_video(i, pptx_files[0], yaml_files[0], OUTPUT_DIR)
        if success:
            success_count += 1
    
    print(f"\n=== Complete: {success_count}/12 videos generated ===")
    print(f"Output directory: {OUTPUT_DIR.absolute()}")

if __name__ == '__main__':
    main()