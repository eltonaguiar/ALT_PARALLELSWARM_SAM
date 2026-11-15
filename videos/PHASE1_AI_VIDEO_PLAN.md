# Phase 1 Implementation Plan: SAM Video Generation (Visuals Only)

## Overview
Create 12 educational videos covering core SAM concepts for job interview mastery, using visual animations/diagrams without audio narration. **Integrates best practices from peer MASTER_PLAN pipeline** (python-pptx/Manim) with AI video generation (ComfyUI/Remotion).

## Video Series Structure (12 Videos) — Aligned with Peer Content

| # | Title | Duration | Peer Video Ref | Key Integrations |
|---|-------|----------|----------------|------------------|
| 1 | SAM in 60 Seconds | 65s | video_01 | I-D-S-E-R mnemonic, 3-record rule, value prop |
| 2 | The Chain: Install → Discovery → Model → Entitlement → Result | 3 min | video_02 | Full chain visual, mnemonic animation |
| 3 | Normalization (SUMN) Deep Dive | 4 min | video_03 | 6 statuses table, suite roll-up critical |
| 4 | Entitlements: Contracts, Metrics, Hygiene | 4 min | video_04 | 7 must-have attrs, metric mismatch trap |
| 5 | Reconciliation Engine Explained | 4 min | video_05 | 3 tiers, IRE rule, what breaks it |
| 6 | Compliance Positions & What They Mean | 3 min | video_06 | CUOUU mnemonic, Unknown ≠ Compliant |
| 7 | Publisher Traps: Microsoft, Oracle, IBM, SAP, Adobe | 5 min | video_07 | Core factor, PVU, indirect access, exam guidance |
| 8 | SaaS License Management | 3 min | video_08 | 26% waste pattern, reclamation workflow |
| 9 | Optimization & Reclamation Workflow | 3 min | video_09 | Priority order, 60-90 day rule |
| 10 | Top 8 SAM Traps (Exam & Real World) | 3 min | video_10 | Metric mismatch, duplicate installs, dead connectors |
| 11 | CIS-SAM Exam Map & Study Strategy | 3 min | video_11 | 5 domains, weights, what to memorize |
| 12 | Lab Walkthrough: Entitlement → Compliance | 4 min | video_12 | 7-step lab, interview talking points |

---

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
│  ├── Mnemonic animations      ← Letter-by-letter reveals  │
│  ├── Exam Alert badges        ← Animated callout boxes    │
│  ├── Interview Soundbites     ← Quote cards with icons    │
│  └── Transitions/Effects      ← Professional polish       │
├────────────────────────────────────────────────────────────┤
│  FFmpeg                       ← Final encoding, concat     │
│  Python scripts               ← Batch processing, metadata │
└────────────────────────────────────────────────────────────┘
```

---

## Unified Content Source (Drives BOTH Pipelines)

**Adopt peer YAML structure** at `videos/content/video_XX.yaml` — single source for:
- Peer pipeline: `generate_slides.py` → PPTX → PNG → MP4
- My pipeline: `scripts/generate_ai_prompts.py` → ComfyUI prompts → Remotion composition

### Content YAML Schema (from peer `video_01_sam_60s.yaml`)

```yaml
meta:
  title: "SAM in 60 Seconds"
  number: 1
  target_duration_sec: 65
  phase: 1
  description: "One-sentence SAM definition, SAM vs HAM vs ITAM, value proposition"

slides:
  - id: title
    type: title
    duration: 3
    text: "ServiceNow SAM in 60 Seconds"
    subtitle: "Software Asset Management Essentials for CIS-SAM"
    show_number: true

  - id: hook
    type: statement
    duration: 5
    text: |
      SAM is the ONLY IT practice that directly prevents
      seven-figure audit penalties while finding 5-15%
      waste in software spend — in year one.
    emphasis: "audit penalties, waste, year one"

  - id: definition
    type: definition
    duration: 8
    title: "What is SAM? (One Sentence)"
    text: |
      SAM reconciles what you OWN (entitlements)
      against what EXISTS and is USED (installs + usage)
      per software model and license metric,
      producing a compliance position.
    highlight: "reconciles, entitlements, installs, usage, compliance position"

  - id: sam_vs_ham
    type: comparison_table
    duration: 12
    title: "SAM vs HAM vs ITAM"
    headers: ["Aspect", "HAM (Hardware)", "SAM (Software)", "ITAM (Both)"]
    rows:
      - ["Tracks", "Physical assets", "Entitlements, installs, usage", "Full portfolio"]
      - ["Core Question", "What do we own, where, who?", "Are we compliant?", "Cost & risk"]
      - ["Key Engine", "Asset lifecycle", "RECONCILIATION", "Both engines"]
      - ["Primary Risk", "Lost/stolen assets", "Publisher audit fines", "Both"]
      - ["Exam Focus", "Hardware normalization", "Metric + publisher rules", "Integration"]
    highlight_row: 2
    highlight_text: "Reconciliation = SAM's unique engine"

  - id: chain
    type: diagram_placeholder
    duration: 10
    title: "The SAM Chain (Memorize: I-D-S-E-R)"
    text: |
      Install → Discovery Model → Software Model → Entitlement → Reconciliation → Compliance Position
      
      I - Install (cmdb_sam_sw_install)
      D - Discovery Model (cmdb_sam_sw_discovery_model)
      S - Software Model (cmdb_software_product_model)
      E - Entitlement (alm_license)
      R - Reconciliation (samp_*_result)
    mnemonic: "I-D-S-E-R = Install, Discovery, Software, Entitlement, Reconciliation"

  - id: three_records
    type: key_concept
    duration: 10
    title: "Three Records Never to Confuse"
    bullets:
      - "Software Model = What it IS (canonical definition from Content Library)"
      - "Entitlement = What you MAY USE (contract rights, quantity, metric)"
      - "Installation = What EXISTS (one install on one device)"
      - "Reconciliation = THE DIFFERENCE (computed nightly/weekly)"
    rule: "Model ≠ Entitlement ≠ Install. Confusing them = wrong compliance."

  - id: value_prop
    type: statement
    duration: 7
    text: |
      Business case in one line:
      SAM returns 5-15% of software spend in year one
      through reclamation and right-sizing,
      and removes catastrophic audit exposure
      on Microsoft, Oracle, IBM — the top three publishers.

  - id: exam_alert
    type: exam_alert
    duration: 5
    text: "EXAM: SAM vs HAM distinction is Domain 1 (15%). Know the 'Reconciliation = SAM's unique engine' talking point."

  - id: interview_soundbite
    type: interview_soundbite
    duration: 5
    text: "\"SAM is the only IT practice that directly prevents seven-figure audit penalties while simultaneously finding 5-15% waste in software spend.\""

  - id: cta
    type: next_video
    duration: 3
    text: "Next: The Chain — Install → Discovery Model → Software Model → Entitlement → Result"
    next_video: 2
```

### Slide Types → My AI Pipeline Mapping

| Peer Slide Type | My AI Prompt Template | Remotion Component |
|----------------|----------------------|-------------------|
| `title` | Title card animation with logo | `TitleCard.tsx` |
| `statement` | Centered text reveal with emphasis highlights | `StatementCard.tsx` |
| `definition` | Definition card with keyword highlighting | `DefinitionCard.tsx` |
| `comparison_table` | Animated table build (row-by-row) | `TableBuilder.tsx` |
| `diagram_placeholder` | ComfyUI + ControlNet (Canny) from Mermaid SVG | `DiagramPlayer.tsx` |
| `key_concept` | Bullet reveal with icons | `BulletReveal.tsx` |
| `exam_alert` | Animated "⚠ EXAM ALERT" badge | `ExamAlert.tsx` |
| `interview_soundbite` | Quote card with speaker icon | `InterviewQuote.tsx` |
| `next_video` | Next video teaser with number | `NextVideoTeaser.tsx` |

---

## Visual Design System (from Peer `generate_slides.py`)

### Color Palette
```typescript
// src/assets/styles/theme.ts
export const COLORS = {
  sn_green: '#006B3F',        // ServiceNow green (primary)
  sn_green_light: '#009B5A',  // Accent
  dark_slate: '#1E2A3A',      // Background
  medium_slate: '#2D3E50',    // Card background
  light_slate: '#3D4E60',     // Borders
  white: '#FFFFFF',
  off_white: '#F8F9FA',
  accent_orange: '#E67E22',   // Exam alerts
  accent_red: '#E74C3C',      // Errors/under-licensed
  accent_blue: '#3498DB',     // Info/compliant
  accent_yellow: '#F39C12',   // Highlights/mnemonics
  text_primary: '#1E2A3A',
  text_secondary: '#5D6D7E',
  code_bg: '#2C3E50',
};
```

### Typography
```typescript
export const FONTS = {
  title: 'Inter, sans-serif',
  subtitle: 'Inter, sans-serif',
  body: 'Source Sans Pro, sans-serif',
  bullet: 'Source Sans Pro, sans-serif',
  code: 'JetBrains Mono, monospace',
  mnemonic: 'JetBrains Mono, monospace',
  caption: 'Source Sans Pro, sans-serif',
};
```

### Layout Constants
```typescript
export const LAYOUT = {
  slideWidth: 1920,
  slideHeight: 1080,
  margin: 120,           // 0.6 inches at 1080p
  contentWidth: 1680,
  accentBarHeight: 6,    // Thin top/bottom bars
  videoNumberBadge: { width: 80, height: 50, right: 50, top: 30 },
};
```

### Required Visual Elements (Every Slide)
1. **Top accent bar** (6px, `sn_green`) — full width
2. **Bottom accent bar** (6px, `sn_green`) — full width
3. **Video number badge** (top-right, `sn_green` background, white text, `#{number}`)
4. **Consistent font sizes** per hierarchy

---

## Mnemonic Animation System (New — Peer Integration)

### Mnemonics to Animate (Letter-by-Letter Reveal)

| Mnemonic | Expansion | Video | Animation Style |
|----------|-----------|-------|-----------------|
| **I-D-S-E-R** | Install, Discovery, Software, Entitlement, Reconciliation | 1, 2 | Sequential letter pop with icon |
| **CUOUU** | Compliant, Under, Over, Unlicensed, Unknown | 6 | Color-coded boxes (green/red/amber/blue/gray) |
| **BAA** | Before, After, Async (Business Rules) | Cross-cutting | Three-panel flip |
| **LOCS** | onLoad, onChange, onSubmit, onCellEdit (Client Scripts) | Cross-cutting | Four-icon grid |
| **IRE** | Identification Before Reconciliation | 5 | Arrow flow: Identify → Reconcile |

### Implementation (ComfyUI + Remotion)
```python
# ComfyUI: ControlNet (Canny) on text mask → letter reveal frames
# Remotion: MnemonicAnimator.tsx — sequences frames with timing
```

---

## Exam Alert & Interview Soundbite System (New — Peer Integration)

### Exam Alert Badge (Per Video)
```typescript
// ExamAlert.tsx — Animated callout
// Trigger: Slide with type: "exam_alert"
// Visual: Orange accent bar, pulsing ⚠ icon, "EXAM:" prefix
// Content: Domain %, question style, key talking point
```

### Interview Soundbite Card (Per Video)
```typescript
// InterviewQuote.tsx — Quote card with speaker icon
// Trigger: Slide with type: "interview_soundbite"
// Visual: Large quote marks, speaker icon, attribution
// Content: One-liner for interview use
```

---

## Lab Demo Clips (New — Peer Integration)

**Record via OBS on PDI instance** (Step 1-7 from `video_12_lab.yaml`):

| Lab Step | Clip Duration | Use In Video |
|----------|---------------|--------------|
| Step 1: Choose/verify software model | 15s | Video 2, 3 |
| Step 2: Create entitlement (qty=1) | 15s | Video 4, 5 |
| Step 3: Confirm installs exist | 12s | Video 5 |
| Step 4: Run reconciliation | 15s | Video 5 |
| Step 5: True-up fix (qty > installs) | 15s | Video 5, 6 |
| Step 6: Normalize discovery model | 15s | Video 3 |
| Step 7: Teach-back (5 sentences) | 15s | Video 12 |

**OBS Settings**: 1080p, 30fps, NVENC, ServiceNow PDI instance
**Post-process**: Crop to relevant UI, add zoom highlights, overlay step numbers

---

## Step-by-Step Implementation (Updated)

### Step 1: Environment Setup (Day 1)
```bash
# Same as before + OBS for lab clips
cd /home/eaguiar2015
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI && pip install -r requirements.txt
cd custom_nodes && git clone https://github.com/ltdrdata/ComfyUI-Manager
git clone https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite
git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved
git clone https://github.com/Fannovel16/comfyui_controlnet_aux
# Download models via Manager: wan2.1, ltx_video, animate_diff
python main.py --listen 0.0.0.0 --port 8188
```

### Step 2: Create Unified Content YAML (Day 1-2)
```bash
# Copy peer content files to local
mkdir -p videos/content
# Use peer YAMLs as base, add AI prompt fields
# Generate 12 YAML files from SAM_KEY_CONCEPTS_SUMMARY.md + peer content
```

### Step 3: Build Remotion Theme System (Day 2-3)
```bash
cd videos
npx create video@latest sam-video-series
cd sam-video-series && npm install

# Create theme components:
# src/components/
#   ThemeProvider.tsx       # COLORS, FONTS, LAYOUT context
#   AccentBars.tsx          # Top/bottom bars (every slide)
#   VideoNumberBadge.tsx    # Top-right badge
#   TitleCard.tsx
#   StatementCard.tsx
#   DefinitionCard.tsx
#   TableBuilder.tsx        # Animated row-by-row
#   DiagramPlayer.tsx       # ComfyUI clip playback
#   BulletReveal.tsx        # Icon + text reveal
#   ExamAlert.tsx           # Pulsing orange badge
#   InterviewQuote.tsx      # Speaker icon + quote
#   MnemonicAnimator.tsx    # Letter-by-letter
#   NextVideoTeaser.tsx
# compositions/
#   Video1_SAM60s.tsx ... Video12_Lab.tsx
```

### Step 4: Create ComfyUI Workflows for Each Slide Type (Day 3-4)

| Workflow | Input | Output | Key Nodes |
|----------|-------|--------|-----------|
| `title_card.json` | Title + subtitle | 3s MP4 | Text-to-image + AnimateDiff |
| `statement_reveal.json` | Text + emphasis words | 5-8s MP4 | ControlNet (text mask) + Wan 2.1 I2V |
| `definition_card.json` | Term + definition + highlights | 8s MP4 | Text layout + reveal animation |
| `table_build.json` | Headers + rows + highlight_row | 10-15s MP4 | Row-by-row via AnimateDiff |
| `diagram_from_mermaid.json` | Mermaid SVG | 10s MP4 | LoadImage (SVG) → ControlNet (Canny) → Wan 2.1 I2V |
| `bullet_reveal.json` | Bullets + icons | 8-12s MP4 | Sequential reveal |
| `mnemonic_reveal.json` | Mnemonic + expansion | 5s MP4 | Letter-by-letter |
| `exam_alert.json` | Alert text | 5s MP4 | Pulsing badge animation |
| `interview_quote.json` | Quote + attribution | 5s MP4 | Quote card animation |

### Step 5: Generate AI Prompts from YAML (Day 4-5)

```python
# scripts/generate_ai_prompts.py
# Reads content/*.yaml → outputs ComfyUI API calls per slide
# Maps slide.type → workflow template + fills prompt variables
```

### Step 6: Batch Generate Visual Assets (Day 5-8)

```bash
# For each video YAML:
# 1. Parse slides
# 2. Call ComfyUI API for each slide → MP4 clips
# 3. Save to sam-video-series/src/assets/clips/video_XX/
# 4. Record lab demo clips via OBS (parallel)
```

### Step 7: Assemble Videos in Remotion (Day 8-10)

```bash
cd sam-video-series
# Each composition imports clips in order, adds:
# - AccentBars (top/bottom)
# - VideoNumberBadge
# - Transitions between clips
# - Timing per YAML duration

npm run build -- --composition=Video1_SAM60s
npm run build -- --composition=Video2_Chain
# ... all 12
```

### Step 8: Post-Processing & QC (Day 10-12)

```bash
# FFmpeg final encoding
for video in out/*.mp4; do
    ffmpeg -i "$video" \
        -c:v h264_nvenc -preset p6 -cq 18 \
        -c:a aac -b:a 128k \
        -movflags +faststart \
        "final/$(basename "$video")"
done

# Thumbnails at 5s mark
for video in final/*.mp4; do
    ffmpeg -i "$video" -ss 00:00:05 -vframes 1 "thumbnails/$(basename "$video" .mp4).jpg"
done
```

---

## ComfyUI Workflow Templates (Detailed)

### Template: Diagram from Mermaid (Core for Videos 2, 5, 6, 7)
```json
{
  "prompt": "Professional technical diagram animation, ServiceNow green (#006B3F) theme, clean lines, smooth transitions, 4K quality, educational style, dark slate background",
  "negative_prompt": "messy, cluttered, low quality, watermark, text artifacts, blurry, bright colors, cartoon style",
  "workflow": {
    "1": "LoadImage: mermaid_svg_rendered.png",
    "2": "ControlNetApply: canny_preprocessor, strength=0.8",
    "3": "Wan21I2V: motion_bucket=127, noise_aug_strength=0.02",
    "4": "VideoHelperSuite: save_video, fps=30, frames=150"
  }
}
```

### Template: Mnemonic Letter Reveal (Videos 1, 2, 6)
```json
{
  "prompt": "Clean letter-by-letter reveal animation, JetBrains Mono font, ServiceNow green color, each letter pops with subtle glow, dark slate background, educational",
  "workflow": {
    "1": "TextToImage: mnemonic_text_mask (black letters on white)",
    "2": "ControlNetApply: canny, strength=1.0",
    "3": "AnimateDiff: motion_module=v15, frames=20 per letter",
    "4": "LTXVideo: fast 5-sec composite"
  }
}
```

### Template: Exam Alert Badge (Every Video)
```json
{
  "prompt": "Animated exam alert badge, orange (#E67E22) pulsing background, white ⚠ icon, 'EXAM:' text, smooth pulsing, 5-second loop, dark slate",
  "workflow": {
    "1": "LoadImage: exam_badge_template.png",
    "2": "AnimateDiff: pulsing motion, 150 frames",
    "3": "VideoHelperSuite: save_video"
  }
}
```

---

## Cloud Fallback (If Local Fails)

```python
# scripts/cloud_generate.py
import fal_client

# Map slide types to fal.ai models
MODEL_MAP = {
    'diagram': 'fal-ai/wan-2-1-i2v',
    'text_reveal': 'fal-ai/ltx-video',
    'table': 'fal-ai/wan-2-1-t2v',
    'mnemonic': 'fal-ai/ltx-video',
}

async def generate_slide(slide_data, output_path):
    model = MODEL_MAP.get(slide_data['type'], 'fal-ai/wan-2-1-t2v')
    result = await fal_client.subscribe(model, arguments={...})
    download_video(result['video']['url'], output_path)
```

---

## Deliverables

| Output | Location | Format |
|--------|----------|--------|
| 12 Video MP4s | `videos/final/` | H.264, 1080p, 30fps, <50MB each |
| 12 Thumbnails | `videos/thumbnails/` | JPG, 1280x720 |
| Content YAMLs | `videos/content/` | 12 YAML files (unified source) |
| ComfyUI Workflows | `videos/workflows/` | 9 JSON workflows |
| Remotion Project | `videos/sam-video-series/` | TypeScript/React |
| Lab Demo Clips | `videos/lab_clips/` | 7 MP4 clips (OBS) |
| Metadata CSV | `videos/metadata.csv` | Title, duration, tags, description |

---

## Quality Gates (Enforced)

- [ ] All videos 1080p, 30fps, <50MB each
- [ ] Consistent branding: accent bars, video badge, colors, fonts on EVERY slide
- [ ] Mnemonics animated: I-D-S-E-R, CUOUU, BAA, LOCS, IRE
- [ ] Exam Alert badge in every video (domain %, question style)
- [ ] Interview Soundbite card in every video
- [ ] Three-record rule card appears in Videos 1, 2, 12
- [ ] Lab demo clips integrated in Videos 2, 3, 4, 5, 6, 12
- [ ] Accurate SAM content (reviewed against peer YAMLs + SAM_KEY_CONCEPTS_SUMMARY.md)
- [ ] No overlapping captions/content (subtitle timing ±500ms)
- [ ] Thumbnails with clear titles at 5s mark
- [ ] Metadata ready for YouTube/LinkedIn upload

---

## Next Steps After Phase 1

Phase 2 (`PHASE2_AUDIO_INTEGRATION_PLAN.md`) adds:
1. **Audio narration** via Edge TTS (free, unlimited) or XTTS v2 (local, voice cloning)
2. **Subtitles** via Whisper alignment → SRT (burned + soft)
3. **Talking head intros** via SadTalker (optional, using lab demo speaker)
4. **YouTube/LinkedIn publishing** automation with chapters, cards, end screens
5. **Analytics tracking** setup