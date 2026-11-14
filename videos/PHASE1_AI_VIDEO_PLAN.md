# Phase 1 Implementation Plan: SAM Video Generation (Visuals Only)

## Overview
Create 10 educational videos covering core SAM concepts for job interview mastery, using visual animations/diagrams without audio narration.

## Video Series Structure (10 Videos)

| # | Title | Duration | Source Section |
|---|-------|----------|----------------|
| 1 | SAM Overview: What, Why, How | 3 min | Purpose, SAM vs HAM vs ITAM |
| 2 | The Three Record Types You Must Know | 4 min | Three Record Types |
| 3 | Normalization Deep Dive: SUMN & Content Library | 5 min | Software Models & Normalization |
| 4 | Entitlements & License Metrics | 4 min | Entitlements, Key Fields |
| 5 | Reconciliation Engine: How Compliance Is Calculated | 5 min | Reconciliation, Flow Diagrams |
| 6 | Compliance Positions Explained | 4 min | Compliance Positions |
| 7 | Publisher-Specific Traps (Microsoft, Oracle, IBM, SAP, Adobe) | 5 min | Publisher-Specific Traps |
| 8 | SaaS License Management & Seat Reclamation | 4 min | SaaS License Management |
| 9 | Optimization & Reclamation Strategies | 4 min | Optimization & Reclamation |
| 10 | CIS-SAM Exam Prep: Domains, Quiz, Mnemonics | 4 min | Exam Alignment, Quiz, Memory Aids |

## Technical Stack (Local-First on ASUS GX10)

```
┌────────────────────────────────────────────────────────────┐
│  ASUS GX10 (RTX 3070/3080 class, 8-16GB VRAM)             │
├────────────────────────────────────────────────────────────┤
│  ComfyUI (Port 8188)          ← Node-based workflows      │
│  ├── Wan 2.1 1.3B (T2V/I2V)   ← Primary video model       │
│  ├── LTX-Video 2.x            ← Fast iteration            │
│  ├── ControlNet (Canny/Depth) ← Structure control         │
│  └── AnimateDiff-Evolved      ← Animation modules         │
├────────────────────────────────────────────────────────────┤
│  Remotion (React/TypeScript)  ← Programmatic video assembly│
│  ├── Video templates          ← Consistent branding       │
│  ├── Text overlays            ← Key concepts, definitions │
│  ├── Diagram rendering        ← Mermaid → SVG → Video     │
│  └── Transitions/Effects      ← Professional polish       │
├────────────────────────────────────────────────────────────┤
│  FFmpeg                       ← Final encoding, concat     │
│  Python scripts               ← Batch processing, metadata │
└────────────────────────────────────────────────────────────┘
```

## Step-by-Step Implementation

### Step 1: Environment Setup (Day 1)

```bash
# 1. Install ComfyUI
cd /home/eaguiar2015
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt

# 2. Install ComfyUI Manager (for easy model/node management)
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager

# 3. Install key custom nodes
git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved
git clone https://github.com/Fannovel16/comfyui_controlnet_aux

# 4. Download models via ComfyUI Manager or manually:
#    - Wan 2.1 1.3B (T2V/I2V)
#    - LTX-Video 2.x
#    - ControlNet models (Canny, Depth)
#    - AnimateDiff motion modules

# 5. Start ComfyUI
python main.py --listen 0.0.0.0 --port 8188
```

### Step 2: Create SAM Visual Style Workflows (Day 2-3)

**Workflow 1: Concept Diagram Generation**
- Input: Mermaid diagram text → SVG → Video frames
- Style: ServiceNow blue theme, consistent node shapes
- Output: 5-10 second animated diagram build

**Workflow 2: Text Overlay / Definition Cards**
- Input: Key term + definition
- Style: Clean card with icon, term, definition
- Output: 3-5 second reveal animation

**Workflow 3: Process Flow Animation**
- Input: Step-by-step process (e.g., normalization flow)
- Style: Animated flow with highlights
- Output: 10-15 second process walkthrough

**Workflow 4: Comparison Table Animation**
- Input: Markdown table (e.g., compliance positions)
- Style: Row-by-row reveal with color coding
- Output: 8-12 second table build

### Step 3: Remotion Project Setup (Day 3-4)

```bash
# Create Remotion project
cd /home/eaguiar2015/findtorontoevents_antigravity.ca/.kilo/worktrees/samvideos-v3/videos
npx create video@latest sam-video-series
cd sam-video-series
npm install

# Project structure:
# src/
#   components/
#     Intro.tsx           # Series intro with SAM logo
#     Outro.tsx           # Series outro with CTA
#     ConceptCard.tsx     # Term + definition card
#     DiagramPlayer.tsx   # Plays ComfyUI-generated video clips
#     TableBuilder.tsx    # Animated table from JSON
#     FlowDiagram.tsx     # Animated flowchart
#     LowerThird.tsx      # "SAM Concept: [Title]"
#   compositions/
#     Video1_SAMOverview.tsx
#     Video2_ThreeRecords.tsx
#     ... (one per video)
#   assets/
#     styles/             # Colors, fonts, constants
#     clips/              # ComfyUI-generated clips (symlinked)
#     audio/              # (Phase 2)
```

### Step 4: Content Scripts from SAM_KEY_CONCEPTS_SUMMARY.md (Day 4-5)

For each video, create a JSON script:

```json
{
  "videoId": 1,
  "title": "SAM Overview: What, Why, How",
  "duration": 180,
  "scenes": [
    {
      "id": "hook",
      "duration": 15,
      "type": "text_reveal",
      "content": "One question costs companies millions: Are we in control of the software we run?"
    },
    {
      "id": "definition",
      "duration": 30,
      "type": "concept_card",
      "content": {
        "term": "Software Asset Management (SAM)",
        "definition": "Reconciles what you own (entitlements) against what exists and is used (normalized installs + usage) per software model and license metric, producing a compliance position."
      }
    },
    {
      "id": "sam_vs_ham",
      "duration": 45,
      "type": "comparison_table",
      "content": "sam_vs_ham_table.json"
    },
    {
      "id": "eli5",
      "duration": 30,
      "type": "analogy_visual",
      "content": "1000 M365 E3 entitlements, 1180 installs, 1090 active users = 90 under-licensed"
    },
    {
      "id": "lifecycle",
      "duration": 45,
      "type": "flow_diagram",
      "content": "sam_lifecycle.mermaid"
    },
    {
      "id": "outro",
      "duration": 15,
      "type": "outro",
      "nextVideo": "The Three Record Types You Must Know"
    }
  ]
}
```

### Step 5: Batch Generate Visual Assets (Day 5-7)

```python
# scripts/generate_assets.py
import json
import subprocess
from pathlib import Path

# Load all video scripts
scripts_dir = Path("scripts/video_scripts")
clips_dir = Path("src/assets/clips")

for script_file in scripts_dir.glob("*.json"):
    with open(script_file) as f:
        script = json.load(f)
    
    for scene in script["scenes"]:
        if scene["type"] == "flow_diagram":
            # Generate diagram video via ComfyUI API
            generate_diagram_video(scene["content"], clips_dir)
        elif scene["type"] == "comparison_table":
            # Generate table animation
            generate_table_animation(scene["content"], clips_dir)
        # ... etc
```

### Step 6: Assemble Videos in Remotion (Day 7-10)

```bash
# Render each video
cd sam-video-series
npm run build -- --composition=Video1_SAMOverview
npm run build -- --composition=Video2_ThreeRecords
# ... etc

# Or render all
npm run render-all
```

### Step 7: Post-Processing & QC (Day 10-12)

```bash
# FFmpeg final encoding for YouTube/LinkedIn
for video in out/*.mp4; do
    ffmpeg -i "$video" \
        -c:v libx264 -preset slow -crf 18 \
        -c:a aac -b:a 128k \
        -movflags +faststart \
        "final/$(basename "$video")"
done

# Generate thumbnails
ffmpeg -i final/Video1_SAMOverview.mp4 -ss 00:00:05 -vframes 1 thumbnails/Video1.jpg
```

## ComfyUI Workflow Templates

### Template 1: Mermaid Diagram → Animated Video

```json
{
  "prompt": "Professional technical diagram animation, ServiceNow blue theme, clean lines, smooth transitions, 4K quality, educational style",
  "negative_prompt": "messy, cluttered, low quality, watermark, text artifacts, blurry",
  "workflow": {
    "1": "LoadImage (SVG rendered from Mermaid)",
    "2": "ControlNet (Canny) for structure preservation",
    "3": "Wan 2.1 I2V with motion bucket for diagram build animation",
    "4": "VideoHelperSuite: Save as MP4"
  }
}
```

### Template 2: Text Card Animation

```json
{
  "prompt": "Clean text reveal animation, minimal design, ServiceNow branding, professional typography, smooth easing",
  "workflow": {
    "1": "Text-to-image with ControlNet for text layout",
    "2": "AnimateDiff for reveal animation",
    "3": "LTX-Video for fast 3-5 sec clip"
  }
}
```

## Cloud Fallback (If Local Fails)

```python
# scripts/cloud_generate.py
import fal_client

# Use fal.ai for video generation
result = fal_client.subscribe(
    "fal-ai/wan-2-1-t2v",
    arguments={
        "prompt": "Professional SAM concept diagram...",
        "negative_prompt": "messy, low quality...",
        "num_frames": 81,
        "fps": 16,
        "width": 1280,
        "height": 720
    }
)
```

## Deliverables

| Output | Location | Format |
|--------|----------|--------|
| 10 Video MP4s | `videos/final/` | H.264, 1080p, 30fps |
| 10 Thumbnails | `videos/thumbnails/` | JPG, 1280x720 |
| Video Scripts JSON | `videos/scripts/` | JSON |
| ComfyUI Workflows | `videos/workflows/` | JSON |
| Remotion Project | `videos/sam-video-series/` | TypeScript/React |
| Metadata CSV | `videos/metadata.csv` | Title, duration, tags, description |

## Quality Gates

- [ ] All videos 1080p, 30fps, <50MB each
- [ ] Consistent branding across all 10 videos
- [ ] Accurate SAM content (reviewed against source)
- [ ] Smooth animations, no visual artifacts
- [ ] Proper timing (3-5 min each)
- [ ] Thumbnails with clear titles
- [ ] Metadata ready for YouTube/LinkedIn upload

## Next Steps After Phase 1

Phase 2 will add:
1. **Audio narration** via edge-tts (free) or TTS-WebUI (local)
2. **Subtitles** via Whisper alignment
3. **Talking head intros** via SadTalker (optional)
4. **YouTube/LinkedIn publishing** automation