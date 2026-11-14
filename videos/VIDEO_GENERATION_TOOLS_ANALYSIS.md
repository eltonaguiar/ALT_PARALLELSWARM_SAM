# Video Generation Tools Analysis for SAM Video Series

**Target Hardware:** ASUS ROG Zephyrus GX10 (Intel i9, RTX 4090 16GB VRAM, 64GB RAM)
**Goal:** Phase 1 = Visual slides/animations only; Phase 2 = Add natural voice narration

---

## PHASE 1: VIDEO GENERATION (Visual Only)

### LOCAL TOOLS (Run on ASUS GX10)

| Tool | Type | Pros | Cons | Best For |
|------|------|------|------|----------|
| **MoviePy** | Python library | Full programmatic control, Python ecosystem, free, mature | Manual animation coding, no built-in templates | Custom slide decks, code-driven videos |
| **Manim** | Python (math animations) | Beautiful math/technical animations, programmatic, community editions (ManimCE) | Steep learning curve, render time | Concept diagrams, flowcharts, math |
| **Stable Video Diffusion** | AI video (local) | Generates video from images, runs on 4090 | Needs ComfyUI/Automatic1111, inconsistent quality, short clips | B-roll, transitions, abstract visuals |
| **AnimateDiff** | AI animation (local) | Animates static images, ControlNet support | Complex setup, flickering issues | Slide-to-video animation |
| **Deforum** | AI video (local) | Zoom/pan animations, prompt-based | Inconsistent, needs tuning | Artistic transitions |
| **FFmpeg** | CLI/Scripting | Universal, fast, scriptable, hardware encoding (NVENC) | No GUI, manual composition | Final encoding, concatenation, optimization |
| **OBS Studio** | Screen recording | Free, records anything, NVENC support | Manual, not automated | Live coding demos, walkthroughs |
| **Python-pptx + LibreOffice** | Slides → Video | Professional slides, programmatic | Two-step (PPTX → PDF → images → video) | Clean slide decks |

### CLOUD FREE TIER TOOLS

| Tool | Free Tier | Pros | Cons | Best For |
|------|-----------|------|------|----------|
| **HeyGen** | 1 min/month | Avatar + TTS, templates, easy | Very limited free minutes | Intro/outro avatar segments |
| **D-ID** | 5 min trial | Talking head from photo, TTS | Watermark, limited trial | Presenter segments |
| **Runway Gen-2** | 125 credits (one-time) | Text-to-video, high quality | One-time credits only | B-roll generation |
| **Pika Labs** | Free tier (Discord) | Text-to-video, good motion | Discord only, queue times | Quick B-roll clips |
| **Kaiber** | 30 credits trial | Audio-reactive, artistic | Trial only, watermark | Artistic transitions |
| **Canva** | Free plan | Templates, animations, easy export | Limited Pro features | Quick slide animations |
| **Kapwing** | Free (watermark) | Browser-based, subtitles, TTS | Watermark on free | Quick edits, subtitles |
| **Lumen5** | Limited free | Blog-to-video, templates | Watermark, 720p max | Content repurposing |

### RECOMMENDED PHASE 1 STACK (Local-First)

**Option A: Programmatic Slides → Video (Highest Quality Control)**
```
Python Script → python-pptx → Professional Slides
     ↓
LibreOffice headless → PNG frames
     ↓
MoviePy/FFmpeg + NVENC → MP4 (H.264/H.265)
```

**Option B: Manim for Technical Diagrams + MoviePy for Assembly**
```
Manim scenes → Animated diagrams (MP4)
     ↓
MoviePy → Compose with slide images, transitions
     ↓
FFmpeg NVENC → Final render
```

**Option C: OBS + Scripted Recording (Fastest Production)**
```
Python script drives browser/app → OBS records (NVENC)
     ↓
FFmpeg trim/encode → Final MP4
```

---

## PHASE 2: NATURAL VOICE NARRATION (TTS)

### LOCAL TTS (ASUS GX10 - RTX 4090 Excellent for This)

| Model | Quality | Speed (RTX 4090) | VRAM | Setup | License |
|-------|---------|------------------|------|-------|---------|
| **XTTS v2 (Coqui)** | ⭐⭐⭐⭐⭐ | ~2x real-time | 4-6GB | `pip install TTS` | Coqui Public Model License |
| **Piper** | ⭐⭐⭐⭐ | ~50x real-time | <1GB | Binary/ONNX | MIT |
| **MeloTTS** | ⭐⭐⭐⭐ | ~10x real-time | 2GB | `pip install melo-tts` | MIT |
| **StyleTTS2** | ⭐⭐⭐⭐⭐ | ~3x real-time | 4GB | Complex install | Non-commercial |
| **Bark (Suno)** | ⭐⭐⭐⭐ | ~1x real-time | 8GB+ | `pip install bark` | MIT |
| **VALL-E X** | ⭐⭐⭐⭐⭐ | Slow | 12GB+ | Research code | Microsoft Research |
| **RVC (Retrieval-based)** | ⭐⭐⭐⭐⭐ | Real-time | 4GB | Training needed | Various |
| **Fish Speech** | ⭐⭐⭐⭐⭐ | Fast | 4GB | New, active dev | BSD-3 |

**Top Local Picks for GX10:**
1. **XTTS v2** - Best quality/speed balance, voice cloning, multilingual
2. **Piper** - Fastest, lowest resource, good enough for narration
3. **MeloTTS** - Good middle ground, fast, multi-speaker
4. **Fish Speech** - Newest SOTA, very natural

### CLOUD FREE TIER TTS

| Service | Free Tier | Quality | Voices | API | Best For |
|---------|-----------|---------|--------|-----|----------|
| **ElevenLabs** | 10k chars/mo | ⭐⭐⭐⭐⭐ | 300+ | Yes | Premium narration |
| **Microsoft Edge TTS** | Unlimited* | ⭐⭐⭐⭐ | 400+ | Unofficial | Free high-quality |
| **Google Cloud TTS** | 1M chars/mo | ⭐⭐⭐⭐ | 220+ | Yes | Production |
| **AWS Polly** | 5M chars/mo (12mo) | ⭐⭐⭐⭐ | 60+ | Yes | AWS integration |
| **PlayHT** | 12.5k chars/mo | ⭐⭐⭐⭐ | 142+ | Yes | Cloning |
| **Speechify** | Limited | ⭐⭐⭐⭐ | 30+ | No API | Personal use |
| **Coqui Studio** | Free tier | ⭐⭐⭐⭐ | Custom | Yes | Open source cloud |
| **Replicate** | $10 credit | ⭐⭐⭐⭐⭐ | Many | Yes | Model variety |

*Edge TTS via unofficial Python library `edge-tts`

### OUR AI TOOLS / MODEL ACCESS

**Available via our infrastructure:**
- **LiteLLM Proxy** (localhost:4000) → Can route to TTS-capable endpoints
- **Free tier models:** Groq, Cerebras (text only, not TTS)
- **NVIDIA NIM** - Has Parakeet ASR, not TTS
- **Local vLLM/Ollama** - Text models only

**Need dedicated TTS endpoints** - not covered by current LLM proxy.

---

## RECOMMENDED ARCHITECTURE

### Phase 1: Visual Generation (Week 1-2)

```python
# Core stack: python-pptx → LibreOffice → MoviePy → FFmpeg
# All local, deterministic, version-controlled

1. Create slide content as JSON/YAML (version controlled)
2. Python script generates .pptx with python-pptx
3. LibreOffice headless converts to PNG frames
4. MoviePy adds transitions, timing, exports video
5. FFmpeg with NVENC hardware encoding for final MP4
```

**Slide Template Structure per Video:**
- Title slide (3s)
- Concept overview (5-10s per bullet)
- Diagram/visual (8-15s)
- Key takeaway (3s)
- Next video teaser (2s)

### Phase 2: Audio Integration (Week 3-4)

**Option A: Local TTS (Recommended - Full Control)**
```bash
# Using XTTS v2 on GX10
python -m TTS.bin.tts --text "SAM reconciles entitlements against installs" \
  --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
  --speaker_wav reference_voice.wav \
  --out_path narration.wav
```

**Option B: Cloud TTS (ElevenLabs Free Tier)**
```python
# 10k chars/month ≈ 10-15 minutes of narration
# High quality, consistent, no local compute
```

**Option C: Hybrid - Edge TTS (Free, Unlimited, Good Quality)**
```python
import edge_tts
communicate = edge_tts.Communicate(text, voice="en-US-AriaNeural")
await communicate.save("narration.mp3")
```

### Final Assembly Pipeline

```
Video (no audio) + Narration (WAV/MP3) → FFmpeg → Final MP4 with audio
     ↓
Subtitles (SRT from narration timestamps) → Burned in or soft subs
     ↓
YouTube/LinkedIn optimized encode (H.264, AAC, 1080p/4K)
```

---

## IMPLEMENTATION PLAN

### Week 1: Foundation
- [ ] Set up Python environment with: `python-pptx`, `moviepy`, `ffmpeg-python`, `edge-tts`, `TTS` (Coqui)
- [ ] Create slide template system (JSON → PPTX)
- [ ] Build Manim scenes for key diagrams (chain, reconciliation flow, compliance states)
- [ ] Test LibreOffice headless conversion
- [ ] Benchmark FFmpeg NVENC encoding on GX10

### Week 2: Video Production (Phase 1)
- [ ] Generate all 12 videos as silent MP4s
- [ ] Create consistent branding (intro/outro, lower thirds, color scheme)
- [ ] Add animated diagrams from Manim
- [ ] Export at 4K for future-proofing, 1080p for delivery

### Week 3: Audio (Phase 2)
- [ ] Test XTTS v2, Piper, Edge TTS for quality comparison
- [ ] Select voice/profile for series consistency
- [ ] Generate narration for all 12 videos
- [ ] Create SRT subtitles with timestamps

### Week 4: Assembly & Polish
- [ ] Combine video + audio with FFmpeg
- [ ] Add subtitles (burned + soft)
- [ ] Generate thumbnails
- [ ] Create YouTube/LinkedIn metadata (titles, descriptions, tags, chapters)
- [ ] Batch upload preparation

---

## HARDWARE REQUIREMENTS CHECK (ASUS GX10)

| Component | Spec | Adequate? |
|-----------|------|-----------|
| GPU | RTX 4090 16GB VRAM | ✅ Excellent for XTTS v2, Stable Video Diffusion |
| CPU | Intel i9 (24 cores) | ✅ Excellent for parallel rendering |
| RAM | 64GB | ✅ Plenty for all local models |
| Storage | NVMe SSD | ✅ Fast I/O for video processing |
| NVENC | Dual NVENC on 4090 | ✅ Hardware H.264/HEVC encoding |

---

## COST ANALYSIS

| Approach | Phase 1 Cost | Phase 2 Cost | Ongoing |
|----------|-------------|-------------|---------|
| **All Local** | $0 | $0 | $0 |
| **Local Video + Edge TTS** | $0 | $0 | $0 |
| **Local Video + ElevenLabs** | $0 | Free tier (10k/mo) | $0-22/mo |
| **Cloud Video (HeyGen/D-ID)** | Limited free | Limited free | $29-59/mo |

**Recommendation: All Local + Edge TTS = $0 total cost, full control, no limits.**

---

## SAMPLE SCRIPT STRUCTURE (Video 1: "SAM in 60 Seconds")

```yaml
# slides/video_01_sam_in_60_seconds.yaml
title: "SAM in 60 Seconds"
duration_target: 65
slides:
  - type: title
    text: "ServiceNow SAM in 60 Seconds"
    subtitle: "Software Asset Management Essentials"
    duration: 3
  
  - type: definition
    text: |
      SAM reconciles what you OWN (entitlements)
      against what EXISTS and is USED (installs + usage)
      per software model and license metric.
    duration: 8
  
  - type: comparison
    title: "SAM vs HAM vs ITAM"
    rows:
      - ["", "HAM", "SAM", "ITAM"]
      - ["Tracks", "Physical hardware", "Software licenses", "Both"]
      - ["Key Engine", "Asset Lifecycle", "Reconciliation", "Both"]
      - ["Risk", "Lost assets", "Audit fines", "Both"]
    duration: 12
  
  - type: diagram
    title: "The SAM Chain"
    concept: "Install → Discovery Model → Software Model → Entitlement → Reconciliation → Compliance Position"
    duration: 15
  
  - type: key_points
    title: "Three Records Never to Confuse"
    bullets:
      - "Software Model = What it IS (canonical definition)"
      - "Entitlement = What you MAY USE (contract rights)"
      - "Installation = What EXISTS (on a device)"
      - "Reconciliation = THE DIFFERENCE"
    duration: 12
  
  - type: cta
    text: "Next: The Chain — Install → Discovery → Model → Entitlement → Result"
    duration: 3
```

---

## QUICK START COMMANDS

```bash
# Install dependencies
pip install python-pptx moviepy ffmpeg-python edge-tts TTS manim

# Install LibreOffice (for PPTX → PNG)
sudo apt-get install libreoffice

# Install FFmpeg with NVENC support
sudo apt-get install ffmpeg

# Test NVENC
ffmpeg -encoders | grep nvenc

# Test XTTS v2
python -c "from TTS.api import TTS; tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2'); print('XTTS v2 loaded')"

# Test Edge TTS
python -c "import edge_tts; print('Edge TTS available')"
```

---

## NEXT STEPS

1. **Create slide content YAML files** for all 12 videos (use SAM_KEY_CONCEPTS.md as source)
2. **Build PPTX generator script** that reads YAML → creates styled slides
3. **Create Manim scenes** for 4-5 key technical diagrams
4. **Build video assembly pipeline** (PPTX → PNG → MoviePy → FFmpeg)
5. **Test TTS options** and select voice
6. **Produce Video 1 as pilot** to validate full pipeline
7. **Batch produce remaining 11 videos**
8. **Add audio + subtitles** for Phase 2