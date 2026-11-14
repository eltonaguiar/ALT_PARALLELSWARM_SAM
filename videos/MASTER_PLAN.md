# SAM Video Series - Master Implementation Plan

**Project:** ServiceNow SAM Expert Video Series for Job Interviews
**Target:** Demonstrate seasoned SAM expertise for CIS-SAM level interviews
**Hardware:** ASUS ROG Zephyrus GX10 (i9, RTX 4090 16GB, 64GB RAM)
**Budget:** $0 (all local + free tier tools)

---

## SOURCE MATERIAL CONSOLIDATED

### Primary Sources
1. **Live SAM Guide** - https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/
   - Comprehensive guide with exam alignment, lab, quiz, mnemonics
   - CIS-SAM domain mapping (5 domains, weights)
   - 7 compliance positions, 6 normalization statuses
   - Publisher traps for Microsoft, Oracle, IBM, SAP, Adobe
   - Reusable code snippets (Business Rules, Script Includes, Client Scripts)

2. **alt_parallelswarm_SAM Repo** - https://github.com/eltonaguiar/alt_parallelswarm_SAM
   - Multi-agent compiled reference (DeepSeek, Grok, Beam)
   - Cheat sheet with V/C/U/P verification marks
   - 13 key tables, 12 key properties, 11 key jobs
   - Rights algebra, IRE rule families, insert/update gates
   - Round 2 gap analysis with numeric test cases T1-T10
   - Bidirectional delta with live guide (18 corrections identified)

### Key Concepts Extracted (17 Categories)
See `SAM_KEY_CONCEPTS.md` for full detail:
1. One-sentence definition + SAM vs HAM vs ITAM
2. The Chain (I-D-S-E-R mnemonic)
3. Three Record Types Never to Confuse
4. SUMN Normalization (6 statuses)
5. Entitlements & Hygiene Rules
6. Reconciliation Engine (3 tiers)
7. Compliance Positions (6 states)
8. Publisher Traps (6 vendors)
9. SaaS License Management
10. Optimization & Reclamation
11. Key Tables/Properties/Jobs
12. Top 8 Traps
13. Rights Algebra
14. CIS-SAM Exam Domains
15. Interview Soundbites
16. Lab Walkthrough
17. Mnemonics (10+ memory aids)

---

## VIDEO SERIES STRUCTURE (12 Videos)

| # | Title | Phase 1 Target | Phase 2 Target | Source Sections |
|---|-------|----------------|----------------|-----------------|
| 1 | SAM in 60 Seconds | 65s | +30s narration | Purpose, SAM vs HAM |
| 2 | The Chain: Install → Discovery → Model → Entitlement → Result | 3min | +2min | Three Record Types, Chain |
| 3 | Normalization (SUMN) Deep Dive | 4min | +2min | SUMN, 6 Statuses, Content Library |
| 4 | Entitlements: Contracts, Metrics, Hygiene | 4min | +2min | Entitlements, License Metrics, Traps |
| 5 | Reconciliation Engine Explained | 4min | +2min | 3 Tiers, Step-by-step, What Breaks It |
| 6 | Compliance Positions & What They Mean | 3min | +1.5min | 6 Positions, Unknown ≠ Compliant |
| 7 | Publisher Traps: Microsoft, Oracle, IBM, SAP, Adobe | 5min | +3min | Publisher-Specific Traps |
| 8 | SaaS License Management | 3min | +1.5min | SaaS vs On-prem, Reclamation Pattern |
| 9 | Optimization & Reclamation Workflow | 3min | +1.5min | Priority Order, 60-90 Day Rule |
| 10 | Top 8 SAM Traps (Exam & Real World) | 3min | +1.5min | Top Traps, Common Mistakes |
| 11 | CIS-SAM Exam Map & Study Strategy | 3min | +1.5min | 5 Domains, Weights, What to Memorize |
| 12 | Lab Walkthrough: Entitlement → Compliance | 4min | +2min | 7-Step Lab, Teach Back |

**Total Phase 1:** ~42 minutes | **Total Phase 2:** ~62 minutes with narration

---

## TECHNICAL ARCHITECTURE

### Phase 1: Visual Generation Pipeline (Local-First)

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  Content YAML   │────▶│ python-pptx  │────▶│ LibreOffice │────▶│   MoviePy    │
│  (12 files)     │     │  Generator   │     │  Headless   │     │  Composer    │
└─────────────────┘     └──────────────┘     │ (PPTX→PNG)  │     └──────┬───────┘
                                              └─────────────┘            │
                                                      ┌──────────────┐   │
                                                      │   Manim      │───┤
                                                      │  (Diagrams)  │   │
                                                      └──────────────┘   │
                                                                         ▼
┌─────────────────┐     ┌──────────────┐     ┌─────────────────────────┐
│  YouTube/LinkedIn│◀───│   FFmpeg     │◀───│    Intermediate MP4     │
│   Metadata JSON  │     │  (NVENC)     │     │   (Silent, 4K/1080p)   │
└─────────────────┘     └──────────────┘     └─────────────────────────┘
```

**Core Dependencies:**
- `python-pptx` - Programmatic slide creation
- `manim` (ManimCE) - Technical animations
- `libreoffice` (headless) - PPTX → PNG conversion
- `moviepy` - Video composition, transitions, timing
- `ffmpeg-python` / FFmpeg CLI - Hardware encoding (NVENC), final output
- `edge-tts` - Free, unlimited, high-quality TTS (Phase 2)

### Phase 2: Audio Integration Pipeline

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│  Script Text    │────▶│   Edge TTS   │────▶│  Narration WAV   │
│  (per slide)    │     │  (or XTTS v2)│     │  + Timestamps    │
└─────────────────┘     └──────────────┘     └────────┬─────────┘
                                                      │
                                                      ▼
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│  Final MP4      │◀───│   FFmpeg     │◀───│  Silent Video +  │
│  (with audio,   │     │  (mux +      │     │  Narration +     │
│   subs, chap.)  │     │   subs)      │     │  SRT Subtitles   │
└─────────────────┘     └──────────────┘     └──────────────────┘
```

---

## IMPLEMENTATION TIMELINE

### Week 1: Foundation & Tooling (Days 1-7)

| Day | Task | Deliverable |
|-----|------|-------------|
| 1 | Environment setup, dependency install, NVENC test | Working dev environment |
| 2 | Create slide template system (master slide, layouts, theme) | `slide_template.py` |
| 3 | Build YAML → PPTX generator with styling | `generate_slides.py` |
| 4 | Create Manim scenes for 5 key diagrams | `diagrams/` (5 .py files) |
| 5 | Build video assembly pipeline (PNG → MoviePy → FFmpeg) | `assemble_video.py` |
| 6 | Test full pipeline with dummy content | `test_output.mp4` |
| 7 | Benchmark render times, optimize settings | Performance baseline |

### Week 2: Content Production (Days 8-14)

| Day | Task | Deliverable |
|-----|------|-------------|
| 8-9 | Write 12 YAML content files from SAM_KEY_CONCEPTS.md | `content/video_01-12.yaml` |
| 10 | Generate all 12 slide decks (PPTX) | `slides/video_01-12.pptx` |
| 11 | Convert to PNG frames via LibreOffice | `frames/video_01-12/` |
| 12 | Render Manim diagram animations | `diagrams/output/*.mp4` |
| 13 | Assemble all 12 silent videos | `output_phase1/video_01-12_silent.mp4` |
| 14 | Quality review, fix timing/transitions | Approved Phase 1 videos |

### Week 3: Audio Production (Days 15-21)

| Day | Task | Deliverable |
|-----|------|-------------|
| 15 | Extract narration scripts from YAML (per-slide text) | `scripts/video_01-12_narration.txt` |
| 16 | Test TTS options: Edge TTS vs XTTS v2 vs Piper (quality A/B) | TTS selection decision |
| 17-18 | Generate narration for all 12 videos + timestamps | `audio/video_01-12_narration.wav + .json` |
| 19 | Generate SRT subtitles from timestamps | `subs/video_01-12.srt` |
| 20 | Mux audio + video + subtitles with FFmpeg | `output_phase2/video_01-12_final.mp4` |
| 21 | Full QA: sync, levels, subtitle accuracy | Approved Phase 2 videos |

### Week 4: Publishing & Polish (Days 22-28)

| Day | Task | Deliverable |
|-----|------|-------------|
| 22 | Generate thumbnails (12 custom + 1 playlist) | `thumbnails/` |
| 23 | Write YouTube metadata (titles, descriptions, tags, chapters) | `metadata/youtube_*.json` |
| 24 | Write LinkedIn metadata (shorter, professional tone) | `metadata/linkedin_*.json` |
| 25 | Create playlist, end screens, cards | YouTube Studio setup |
| 26 | Batch upload to YouTube (unlisted → scheduled) | 12 videos scheduled |
| 27 | Cross-post to LinkedIn, GitHub Pages embed | Multi-platform presence |
| 28 | Analytics baseline, retrospective doc | `RETROSPECTIVE.md` |

---

## CONTENT AUTHORING FORMAT

Each video defined as YAML:

```yaml
# content/video_03_normalization.yaml
meta:
  title: "Normalization (SUMN) Deep Dive"
  number: 3
  target_duration_sec: 240
  phase: 1

slides:
  - id: title
    type: title
    duration: 3
    text: "Software Model Normalization (SUMN)"
    subtitle: "From Raw Fingerprints to Canonical Models"
  
  - id: problem
    type: problem_statement
    duration: 8
    text: |
      Discovery finds 40 variants of "Microsoft Office":
      Office16, Office15, O365ProPlus, MSOffice2019...
      Without normalization: catastrophic under-licensing
  
  - id: workflow
    type: process_flow
    duration: 15
    title: "Normalization Workflow"
    steps:
      - "Discovery collects raw fingerprints → Discovery Model"
      - "SUMN matches to Content Library publisher packs"
      - "Unmatched → Normalization Queue (manual review)"
      - "Admin maps: Normalize action or Ignore"
      - "Normalized installs → Reconciliation"
  
  - id: statuses
    type: table
    duration: 12
    title: "Six Normalization Statuses"
    headers: ["Status", "Manual Normalize?", "Revert?"]
    rows:
      - ["New", "No", "No"]
      - ["Match Not Found", "Yes", "No"]
      - ["Publisher Normalized", "Yes", "Yes"]
      - ["Partially Normalized", "Yes", "Yes"]
      - ["Normalized", "No", "Yes"]
      - ["Manually Normalized", "No", "No"]
    highlight: "All reverts go to Match Not Found"
  
  - id: suites
    type: key_concept
    duration: 10
    title: "Suite Roll-Up Critical"
    text: |
      Oracle DB EE, Microsoft Office, Adobe CC are SUITES
      Components must roll up to suite for correct counting
      Without suite membership: 500 Word + 500 Excel + 500 PPT = 1,500 licenses!
  
  - id: takeaway
    type: key_takeaway
    duration: 5
    text: "Normalize FIRST, then entitle. Unnormalized = unlicensed = audit risk."
  
  - id: next
    type: next_video
    duration: 3
    text: "Next: Entitlements — Contracts, Metrics, and the Maintenance Trap"
```

---

## QUALITY STANDARDS

### Video Specs
- **Resolution:** 4K (3840×2160) master, 1080p delivery
- **Frame Rate:** 30 fps
- **Codec:** H.264 (NVENC) for compatibility, HEVC option
- **Bitrate:** 20 Mbps (4K), 8 Mbps (1080p)
- **Audio:** 48 kHz, 192 kbps AAC (Phase 2)
- **Subtitles:** Burned-in (MP4) + soft SRT (YouTube upload)

### Branding Consistency
- **Color Scheme:** ServiceNow green (#006B3F) + dark slate (#1E2A3A) + white
- **Fonts:** Inter (titles), JetBrains Mono (code/tables), Source Sans (body)
- **Lower Third:** "ServiceNow SAM Expert Series" + video number
- **Intro:** 3s animated logo + title
- **Outro:** 3s "Subscribe for CIS-SAM prep" + next video link

### Accessibility
- High contrast ratios (WCAG AA)
- Subtitles on all videos
- Chapter markers in YouTube description
- Alt-text for thumbnails

---

## RISK MITIGATION

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| LibreOffice headless fails on complex PPTX | Medium | High | Test early; fallback to `unoconv` or `python-pptx` PDF export |
| Manim render too slow | Low | Medium | Pre-render diagrams; cache outputs |
| TTS quality insufficient | Medium | High | Test 3 options Week 3 Day 16; have cloud fallback |
| FFmpeg NVENC not available | Low | High | Verify Day 1; software encoding fallback (slower) |
| Content too dense for video format | Medium | High | Peer review scripts Week 2; enforce 1 concept/slide |
| Timeline slip | Medium | Medium | Buffer days built in; Phase 1 delivers value alone |

---

## SUCCESS METRICS

### Phase 1 (Visual Only)
- [ ] 12 videos rendered at 1080p/30fps, <5% render errors
- [ ] Consistent branding across all videos
- [ ] All key diagrams animated (Manim)
- [ ] Total runtime ~42 minutes

### Phase 2 (With Audio)
- [ ] Narration naturalness rated ≥4/5 in self-review
- [ ] Audio sync <100ms drift
- [ ] Subtitles 100% accurate
- [ ] Total runtime ~62 minutes

### Publishing
- [ ] All 12 videos uploaded to YouTube (unlisted → public schedule)
- [ ] LinkedIn posts for each video (12 posts)
- [ ] GitHub Pages embed on portfolio
-   [ ] Playlist created with proper ordering
- [ ] Analytics tracking enabled

---

## FILE STRUCTURE

```
videos/
├── SAM_KEY_CONCEPTS.md           # Source content (17 categories)
├── VIDEO_GENERATION_TOOLS_ANALYSIS.md  # Tool evaluation
├── MASTER_PLAN.md                # This file
├── content/                      # YAML slide definitions
│   ├── video_01_sam_60s.yaml
│   ├── video_02_chain.yaml
│   ├── ...
│   └── video_12_lab.yaml
├── scripts/                      # Python automation
│   ├── generate_slides.py
│   ├── assemble_video.py
│   ├── generate_narration.py
│   ├── mux_audio_video.py
│   └── upload_youtube.py
├── diagrams/                     # Manim scenes
│   ├── chain_diagram.py
│   ├── reconciliation_flow.py
│   ├── compliance_states.py
│   ├── publisher_traps.py
│   └── saas_vs_onprem.py
├── slide_template.pptx           # Master template
├── frames/                       # LibreOffice PNG output
│   ├── video_01/
│   └── ...
├── output_phase1/                # Silent videos
│   ├── video_01_silent.mp4
│   └── ...
├── output_phase2/                # Final videos with audio
│   ├── video_01_final.mp4
│   └── ...
├── audio/                        # Narration files
│   ├── video_01_narration.wav
│   ├── video_01_timestamps.json
│   └── ...
├── subs/                         # SRT subtitles
│   ├── video_01.srt
│   └── ...
├── thumbnails/                   # 1280x720 custom thumbs
│   ├── video_01_thumb.jpg
│   └── ...
├── metadata/                     # Platform metadata
│   ├── youtube_video_01.json
│   ├── linkedin_video_01.json
│   └── ...
└── RETROSPECTIVE.md              # Post-project review
```

---

## IMMEDIATE NEXT ACTIONS

1. **Run environment setup** (see `VIDEO_GENERATION_TOOLS_ANALYSIS.md` Quick Start)
2. **Create `slide_template.pptx`** with master slides/layouts
3. **Build `generate_slides.py`** prototype with 1 test YAML
4. **Test full pipeline** end-to-end with dummy content
5. **Author 12 YAML content files** from `SAM_KEY_CONCEPTS.md`
6. **Produce Video 1 as pilot** to validate everything

---

## COMMANDS TO START

```bash
cd /home/eaguiar2015/findtorontoevents_antigravity.ca/.kilo/worktrees/samvideos-v4/videos

# 1. Install dependencies
pip install python-pptx moviepy ffmpeg-python edge-tts TTS manim Pillow numpy

# 2. System dependencies
sudo apt-get update && sudo apt-get install -y libreoffice ffmpeg

# 3. Verify NVENC
ffmpeg -encoders | grep -E "nvenc|hevc_nvenc"

# 4. Test XTTS v2
python -c "from TTS.api import TTS; tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2', gpu=True); print('XTTS v2 OK')"

# 5. Test Edge TTS
python -c "import edge_tts; print('Edge TTS OK')"

# 6. Create project structure
mkdir -p content scripts diagrams frames output_phase1 output_phase2 audio subs thumbnails metadata

# 7. Start with slide template
# (Create slide_template.pptx manually or via script)
```

---

## NOTES FOR FUTURE SESSIONS

- All source content is in `SAM_KEY_CONCEPTS.md` - no need to re-fetch
- Tool analysis complete in `VIDEO_GENERATION_TOOLS_ANALYSIS.md`
- This plan is the single source of truth for execution
- Phase 1 delivers standalone value; Phase 2 enhances
- Zero budget constraint means all-local + Edge TTS preferred
- ASUS GX10 has ample compute for XTTS v2 if Edge TTS quality insufficient