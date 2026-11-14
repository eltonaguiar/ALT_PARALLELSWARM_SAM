# Phase 2: Audio Integration Plan for SAM Video Series

**Complements:** `videos/MASTER_PLAN.md` (existing python-pptx/Manim pipeline)
**Hardware:** ASUS ROG Zephyrus GX10 (RTX 4090 16GB, 64GB RAM)
**Budget:** $0 (all local + free tier tools)

---

## Overview

Phase 1 (existing MASTER_PLAN) produces **silent 4K/1080p MP4s** via:
`python-pptx → LibreOffice → PNG → MoviePy → FFmpeg (NVENC)`

Phase 2 adds **natural voice narration + subtitles** to produce final deliverables.

---

## Phase 2 Architecture

```
┌─────────────────────┐     ┌──────────────────┐     ┌────────────────────┐
│  Silent Video MP4   │     │  Narration Script │     │   TTS Engine       │
│  (Phase 1 output)   │     │  (per slide/      │     │   (XTTS v2 /       │
│                     │     │   scene timing)   │     │    Edge TTS)       │
└──────────┬──────────┘     └────────┬─────────┘     └────────┬───────────┘
           │                         │                      │
           │                         ▼                      ▼
           │              ┌──────────────────┐     ┌────────────────────┐
           │              │  Timestamp JSON  │     │  Narration WAV/MP3 │
           │              │  (word-level)    │     │  + prosody control │
           │              └────────┬─────────┘     └────────┬───────────┘
           │                       │                      │
           ▼                       ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FFmpeg Mux Pipeline                           │
│  1. video.mp4 + narration.wav → video_with_audio.mp4            │
│  2. Generate SRT from timestamps → subtitles.srt                │
│  3. Burn subtitles (optional) + soft SRT embed                  │
│  4. YouTube/LinkedIn optimized encodes (H.264, AAC, chapters)  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────┴───────────────┐
              ▼                               ▼
    ┌─────────────────────┐         ┌─────────────────────┐
    │ YouTube Upload      │         │ LinkedIn Upload     │
    │ (with chapters,     │         │ (professional tone, │
    │  cards, end screens)│         │  native captions)   │
    └─────────────────────┘         └─────────────────────┘
```

---

## TTS Engine Selection (ASUS GX10 Optimized)

### Primary: XTTS v2 (Coqui) - Local, Best Quality
```bash
# Install
pip install TTS

# Generate narration with voice cloning
python -c "
from TTS.api import TTS
tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', gpu=True)
tts.tts_to_file(
    text='SAM reconciles what you own against what exists.',
    speaker_wav='reference_voice.wav',  # 10-30s clean sample
    language='en',
    file_path='narration.wav'
)
"
```
- **Quality:** ⭐⭐⭐⭐⭐ (near-human, expressive)
- **Speed:** ~2x real-time on RTX 4090
- **VRAM:** 4-6GB
- **Voice cloning:** Yes (3-10s reference)
- **Languages:** 16+

### Fallback 1: Edge TTS (Free, Unlimited, Cloud)
```python
import edge_tts
import asyncio

async def generate(text, voice="en-US-AriaNeural", output="narration.mp3"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output)

asyncio.run(generate("SAM reconciles entitlements against installs."))
```
- **Quality:** ⭐⭐⭐⭐ (Microsoft Neural voices, very natural)
- **Cost:** $0, unlimited
- **Voices:** 400+ (en-US-AriaNeural, en-US-GuyNeural, en-GB-LibbyNeural, etc.)
- **No GPU needed**

### Fallback 2: Piper TTS (Fastest Local, CPU)
```bash
# Install
pip install piper-tts

# Generate
piper --model en_US-lessac-medium --output_file narration.wav <<< "SAM reconciles entitlements against installs."
```
- **Quality:** ⭐⭐⭐⭐ (good, slightly robotic)
- **Speed:** ~50x real-time (CPU only)
- **VRAM:** <1GB
- **Voices:** 1000+ across 100+ languages

---

## Narration Script Extraction

From existing YAML content structure (per MASTER_PLAN):

```yaml
# content/video_03_normalization.yaml
slides:
  - id: title
    type: title
    narration: "Welcome to the Normalization Deep Dive. This is where most SAM implementations live or die."
    duration: 5
  
  - id: problem
    type: problem_statement
    narration: "Discovery finds forty variants of Microsoft Office. Office16, Office15, O365ProPlus, MSOffice2019. Without normalization, reconciliation against one Office entitlement shows catastrophic under-licensing."
    duration: 10
  
  - id: workflow
    type: process_flow
    narration: "The normalization workflow has five steps. First, discovery collects raw fingerprints creating Discovery Models. Second, SUMN matches these to Software Models in the Content Library using publisher packs. Third, unmatched models land in the normalization queue for manual review. Fourth, the SAM admin maps them manually or ignores them. Fifth, normalized installs finally participate in reconciliation."
    duration: 18
```

**Extraction script** generates per-video narration text file with timestamps.

---

## Subtitle Generation (SRT)

```python
# Generate SRT from narration timestamps
# XTTS v2 and Edge TTS both support word-level timestamps

def generate_srt(timestamps, output_path):
    """timestamps = [{'word': 'SAM', 'start': 0.5, 'end': 0.8}, ...]"""
    srt_lines = []
    chunk_size = 8  # words per subtitle line
    for i in range(0, len(timestamps), chunk_size):
        chunk = timestamps[i:i+chunk_size]
        start = chunk[0]['start']
        end = chunk[-1]['end']
        text = ' '.join(w['word'] for w in chunk)
        index = i // chunk_size + 1
        srt_lines.append(f"{index}\n{format_time(start)} --> {format_time(end)}\n{text}\n")
    Path(output_path).write_text('\n'.join(srt_lines))
```

---

## FFmpeg Mux Commands

### 1. Combine Video + Audio
```bash
# NVENC hardware encode, preserve quality
ffmpeg -i video_silent.mp4 -i narration.wav \
  -c:v h264_nvenc -preset p6 -cq 18 \
  -c:a aac -b:a 192k \
  -map 0:v:0 -map 1:a:0 \
  -shortest \
  -movflags +faststart \
  video_with_audio.mp4
```

### 2. Add Soft Subtitles (SRT embedded)
```bash
ffmpeg -i video_with_audio.mp4 -i subtitles.srt \
  -c copy -c:s mov_text \
  -metadata:s:s:0 language=eng \
  video_final.mp4
```

### 3. Burn Subtitles (for platforms without soft sub support)
```bash
ffmpeg -i video_silent.mp4 -i narration.wav -vf "subtitles=subtitles.srt:force_style='FontSize=24,PrimaryColour=&HFFFFFF'" \
  -c:v h264_nvenc -preset p6 -cq 18 \
  -c:a aac -b:a 192k \
  video_burned_subs.mp4
```

### 4. YouTube Chapter Markers (from slide structure)
```bash
# Generate chapters.txt from YAML slide timings
# FFmpeg metadata injection
ffmpeg -i video_final.mp4 -f ffmetadata -i chapters.txt -map_metadata 1 -c copy video_chaptered.mp4
```

---

## Voice Profile for Series Consistency

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Voice** | `en-US-GuyNeural` (Edge TTS) or XTTS cloned from 30s sample | Professional, authoritative male voice |
| **Rate** | -5% (slightly slower) | Technical content needs processing time |
| **Pitch** | 0% (natural) | Avoids "AI voice" artifacts |
| **Volume** | +2dB | Clear over background music |
| **Style** | "narration" or "documentary" | If supported by TTS |

**Reference sample:** Record 30s of yourself reading SAM content, or use a clean podcast clip with permission.

---

## Implementation Timeline (4 Weeks from Phase 1 Completion)

### Week 1: TTS Selection & Pipeline Build
| Day | Task | Deliverable |
|-----|------|-------------|
| 1 | Install TTS, Edge TTS, Piper; test all three on GX10 | Quality comparison matrix |
| 2 | Select primary/fallback TTS; create voice profile | `voice_profile.json` |
| 3 | Build narration extractor from YAML content | `scripts/extract_narration.py` |
| 4 | Build SRT generator from TTS timestamps | `scripts/generate_srt.py` |
| 5 | Build FFmpeg mux pipeline (video + audio + subs) | `scripts/mux_audio_video.py` |
| 6 | Test full pipeline with Video 1 pilot | `output_phase2/video_01_final.mp4` |
| 7 | QA: sync, levels, subtitle accuracy | Signed-off pipeline |

### Week 2: Batch Audio Production
| Day | Task | Deliverable |
|-----|------|-------------|
| 8-10 | Generate narration for Videos 1-12 | `audio/video_01-12_narration.wav + .json` |
| 11-12 | Generate SRT subtitles for all | `subs/video_01-12.srt` |
| 13 | Mux all 12 videos (parallel on GX10) | `output_phase2/video_01-12_final.mp4` |
| 14 | Full QA review | Approved Phase 2 videos |

### Week 3: Platform Optimization
| Day | Task | Deliverable |
|-----|------|-------------|
| 15 | Generate thumbnails (12 custom + playlist) | `thumbnails/` |
| 16 | Write YouTube metadata (titles, descriptions, tags, chapters) | `metadata/youtube_*.json` |
| 17 | Write LinkedIn metadata (professional tone, native captions) | `metadata/linkedin_*.json` |
| 18 | Create YouTube playlist, end screens, cards | Studio setup |
| 19 | Batch upload to YouTube (scheduled) | 12 videos scheduled |
| 20 | Cross-post to LinkedIn | 12 posts scheduled |
| 21 | GitHub Pages embed, analytics setup | Portfolio integration |

---

## Quality Gates

### Audio Quality
- [ ] Narration naturalness ≥4/5 (self-review + 1 peer)
- [ ] No audible artifacts, clipping, or background noise
- [ ] Consistent voice/profile across all 12 videos
- [ ] Audio levels: -16 LUFS (YouTube standard)

### Sync Accuracy
- [ ] Audio-video sync <100ms drift (measured at 5 points)
- [ ] Subtitle timing ±500ms accuracy
- [ ] Chapter markers align with slide transitions

### Platform Compliance
- [ ] YouTube: H.264, AAC, 1080p, chapters, cards, end screens
- [ ] LinkedIn: 1080p, native captions (SRT), professional description
- [ ] Thumbnails: 1280×720, <2MB, high contrast, readable at 10%

---

## File Structure Additions

```
videos/
├── (existing MASTER_PLAN files...)
├── audio/                          # NEW - Phase 2
│   ├── video_01_narration.wav
│   ├── video_01_timestamps.json
│   └── ...
├── subs/                           # NEW - Phase 2
│   ├── video_01.srt
│   └── ...
├── output_phase2/                  # NEW - Phase 2
│   ├── video_01_final.mp4
│   └── ...
├── thumbnails/                     # NEW - Phase 2
│   ├── video_01_thumb.jpg
│   └── ...
├── metadata/                       # NEW - Phase 2
│   ├── youtube_video_01.json
│   ├── linkedin_video_01.json
│   └── ...
├── scripts/                        # EXTENDED - Phase 2
│   ├── extract_narration.py
│   ├── generate_srt.py
│   ├── mux_audio_video.py
│   └── upload_youtube.py
└── voice_profile.json              # NEW - Phase 2
```

---

## Integration with Existing MASTER_PLAN

| MASTER_PLAN Phase 1 Output | Phase 2 Input |
|---------------------------|---------------|
| `output_phase1/video_01_silent.mp4` | Video source for mux |
| `content/video_01.yaml` | Narration text source (per-slide `narration` field) |
| `scripts/assemble_video.py` | Extended with `mux_audio_video.py` call |

**No changes to Phase 1 pipeline required** — Phase 2 consumes its outputs.

---

## Quick Start (After Phase 1 Complete)

```bash
cd /home/eaguiar2015/findtorontoevents_antigravity.ca/.kilo/worktrees/samvideos-v3/videos

# 1. Install TTS dependencies
pip install TTS edge-tts piper-tts ffmpeg-python

# 2. Test TTS engines
python -c "from TTS.api import TTS; tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', gpu=True); print('XTTS v2 OK')"
python -c "import edge_tts; print('Edge TTS OK')"

# 3. Create voice profile (record 30s sample → reference_voice.wav)
# 4. Run Phase 2 pipeline
python scripts/extract_narration.py
python scripts/generate_srt.py
python scripts/mux_audio_video.py

# 5. Verify output
ffplay output_phase2/video_01_final.mp4
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| XTTS v2 quality insufficient | Edge TTS fallback (unlimited, high quality) |
| TTS timestamps misaligned | Manual SRT correction pass; Whisper alignment as backup |
| FFmpeg NVENC fails | Software encoding fallback (`-c:v libx264 -preset slow`) |
| Subtitle burn-in reduces quality | Provide both burned + soft sub versions |
| Voice inconsistency across videos | Single voice profile; batch generate all narration in one session |

---

## Success Criteria

- [ ] 12 videos with natural narration uploaded to YouTube
- [ ] 12 videos cross-posted to LinkedIn with native captions
- [ ] Consistent voice across series
- [ ] Subtitles 100% accurate, burned + soft
- [ ] Chapter markers functional on YouTube
- [ ] Total Phase 2 time: ≤2 weeks after Phase 1 complete