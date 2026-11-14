# SAM Videos Project

Educational video series for ServiceNow Software Asset Management (SAM) mastery — designed for job interview preparation and technical expertise demonstration.

## Project Structure

```
videos/
├── SAM_KEY_CONCEPTS_SUMMARY.md      # Source content (all key SAM concepts)
├── PHASE1_IMPLEMENTATION_PLAN.md    # Phase 1: Video-only generation plan
├── PHASE2_AUDIO_PLAN.md             # Phase 2: Audio integration plan (to be created)
├── research/
│   └── VIDEO_GENERATION_TOOLS_RESEARCH.md  # Comprehensive tool research
├── scripts/                          # Generation scripts (to be created)
├── workflows/                        # ComfyUI workflows (to be created)
├── sam-video-series/                 # Remotion project (to be created)
├── assets/                           # Generated visual assets
│   └── clips/                        # ComfyUI-generated video clips
├── final/                            # Final rendered videos
├── thumbnails/                       # Video thumbnails
└── metadata.csv                      # Video metadata for publishing
```

## Phase Status

| Phase | Focus | Status | Target |
|-------|-------|--------|--------|
| **Phase 1** | Video generation (visuals only) | 🟡 Planning | 10 videos, 3-5 min each |
| **Phase 2** | Audio narration + subtitles | ⏳ Pending | Natural voice, talking heads |

## Source Content

All SAM concepts consolidated from:
- **GitHub Pages Guide**: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/
- **alt_parallelswarm_SAM Repo**: https://github.com/eltonaguiar/alt_parallelswarm_SAM
- **CIS-SAM Exam Blueprint** domains mapped

Key concepts covered: SAM lifecycle, 3 record types, normalization (SUMN), entitlements, reconciliation, compliance positions, publisher traps, SaaS management, optimization, exam prep.

## Quick Start (Phase 1)

```bash
# 1. Set up ComfyUI on ASUS GX10
cd /home/eaguiar2015
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI && pip install -r requirements.txt
cd custom_nodes && git clone https://github.com/ltdrdata/ComfyUI-Manager
# ... install other custom nodes

# 2. Start ComfyUI
python main.py --listen 0.0.0.0 --port 8188

# 3. Create Remotion project
cd /home/eaguiar2015/findtorontoevents_antigravity.ca/.kilo/worktrees/samvideos-v3/videos
npx create video@latest sam-video-series

# 4. Follow PHASE1_IMPLEMENTATION_PLAN.md
```

## Key Tools Identified

| Category | Local (ASUS GX10) | Cloud (Free/Paid) |
|----------|-------------------|-------------------|
| **Video Gen** | ComfyUI + Wan 2.1 1.3B / LTX-Video | fal.ai, Replicate, Kling, MiniMax |
| **TTS** | TTS-WebUI (Kokoro, Piper, XTTS) | Edge TTS (free), ElevenLabs |
| **Talking Head** | SadTalker, LivePortrait | HeyGen, D-ID, Synthesia |
| **Assembly** | Remotion (React), FFmpeg | Creatomate, Shotstack |

## Video Series Outline (10 Videos)

1. **SAM Overview: What, Why, How** (3 min)
2. **The Three Record Types You Must Know** (4 min)
3. **Normalization Deep Dive: SUMN & Content Library** (5 min)
4. **Entitlements & License Metrics** (4 min)
5. **Reconciliation Engine: How Compliance Is Calculated** (5 min)
6. **Compliance Positions Explained** (4 min)
7. **Publisher-Specific Traps** (5 min)
8. **SaaS License Management & Seat Reclamation** (4 min)
9. **Optimization & Reclamation Strategies** (4 min)
10. **CIS-SAM Exam Prep: Domains, Quiz, Mnemonics** (4 min)

## Research Resources

- [Video Generation Tools Research](research/VIDEO_GENERATION_TOOLS_RESEARCH.md) — Comprehensive analysis of 50+ tools
- [Awesome Video Generation](https://github.com/backblaze-labs/awesome-video-generation) — Curated API/tool list
- [Video Generation Landscape](https://github.com/ishandutta2007/Video-Generation-Landscape) — Model comparisons
- [TTS-WebUI](https://github.com/rsxdalv/TTS-WebUI) — All-in-one local TTS
- [Pixelle-Video](https://github.com/AIDC-AI/Pixelle-Video) — Full auto video pipeline

## Notes

- **ASUS GX10**: Assumed RTX 3070/3080 class (8-16GB VRAM) — Wan 2.1 1.3B and LTX-Video run well
- **Cloud credits**: fal.ai ($1 free), Replicate ($10/mo free), Edge TTS (unlimited free)
- **License**: All recommended open-source tools are Apache 2.0 / MIT licensed
- **Phase 2**: Will add natural voice narration using edge-tts (Microsoft) or local Kokoro TTS