# Video Generation Tools Research for SAM Educational Videos

## Executive Summary

This research covers free/open-source video generation tools with natural voices, suitable for:
- **Local compute**: ASUS GX10 (assumed RTX 3070/3080 class GPU, 8-16GB VRAM)
- **Cloud compute**: Free tiers + paid models via our API keys

**Phase 1 Focus**: Video generation (visuals/animations) to summarize SAM concepts
**Phase 2 Focus**: Videos with natural voice audio

---

## Part 1: Text-to-Video Generation (Visuals)

### Top Open-Source Models for Local Compute (ASUS GX10)

| Model | Repo | VRAM Req | Quality | Best For | License |
|-------|------|----------|---------|----------|---------|
| **Wan 2.1 (1.3B)** | Wan-Video/Wan2.1 | 8GB | SOTA 2025, best prompt adherence | General T2V, I2V | Apache 2.0 |
| **Wan 2.1 (14B)** | Wan-Video/Wan2.1 | 14GB+ | Highest quality | Production quality | Apache 2.0 |
| **CogVideoX-5B** | zai-org/CogVideo | 8-12GB | 10s videos, good quality | Balanced quality/speed | Apache 2.0 |
| **HunyuanVideo** | Tencent-Hunyuan/HunyuanVideo | 8GB (1.5) | Cinematic, strong I2V | Cinematic content | Apache 2.0 |
| **LTX-Video / LTX-2** | Lightricks/LTX-Video | 6-8GB | Real-time, 4K@50fps, native audio | Fast iteration | Apache 2.0 |
| **Mochi-1** | genmoai/models | 12GB+ | 30fps, physical realism | High-fidelity motion | Apache 2.0 |
| **SVD (Stable Video Diffusion)** | Stability-AI/generative-models | 8GB+ | I2V standard | Image-to-video | Stability NC |
| **FramePack** | lllyasviel/FramePack | 6GB | 60s@30fps, length-independent | Long-form content | Apache 2.0 |

### Recommended Local Stack for ASUS GX10 (8-16GB VRAM)

```
Option A (Best Balance): Wan 2.1 1.3B + ComfyUI
- Runs on 8GB VRAM
- Best prompt adherence
- Apache 2.0 license
- ComfyUI for workflow control

Option B (Speed): LTX-Video 2.x + ComfyUI
- Runs on 6GB VRAM
- Real-time generation
- Native audio sync
- Apache 2.0 license

Option C (Quality): CogVideoX-5B
- Runs on 8-12GB VRAM
- 10 second clips
- Z.ai backing
```

### Cloud/Hosted Free Tiers (No Local GPU Needed)

| Service | Free Tier | Models | API Access |
|---------|-----------|--------|------------|
| **fal.ai** | $1 credit (≈50-100 gens) | Wan, Kling, Veo, LTX, Luma, Runway | Python/Node SDK |
| **Replicate** | $10 credit/mo | 100+ video models | Python/Node SDK |
| **Hugging Face Spaces** | Free CPU/GPU (queue) | Many open models | Web UI / API |
| **Google Colab** | Free T4 GPU | Any model via diffusers | Notebook |
| **Kling AI** | Daily free credits | Kling 1.5/1.6 | REST API |
| **MiniMax/Hailuo** | Free tier | Hailuo 2.3 | REST API |
| **Seedance (ByteDance)** | Dreamina free tier | Seedance 2.0/2.5 | Web/Dreamina |

---

## Part 2: Text-to-Speech (Natural Voices)

### Top Local TTS Engines (Run on CPU/GPU)

| Engine | Repo | Voices | Quality | Languages | License | VRAM |
|--------|------|--------|---------|-----------|---------|------|
| **Kokoro TTS** | hexgrad/kokoro | 50+ | Excellent | 8+ | Apache 2.0 | 1-2GB |
| **Piper TTS** | rhasspy/piper | 1000+ | Very Good | 100+ | MIT | <1GB (CPU) |
| **XTTS v2** | coqui-ai/TTS | 16 languages | Excellent | 16 | CC BY-NC 4.0 | 2-4GB |
| **F5-TTS** | SWivid/F5-TTS | Few | Excellent | EN/ZH | MIT | 4-6GB |
| **CosyVoice** | FunAudioLLM/CosyVoice | Many | Excellent | EN/ZH | Apache 2.0 | 4-6GB |
| **GPT-SoVITS** | X-T-E-R/GPT-SoVITS | Voice clone | Excellent | EN/ZH/JP | MIT | 6-8GB |
| **Kitten TTS** | rsxdalv/kitten_tts | Few | Good | EN | MIT | 1-2GB |
| **Bark** | suno-ai/bark | 100+ | Good | Many | MIT | 4-8GB |
| **DIA** | nari-labs/dia | Few | Excellent | EN | Apache 2.0 | 4-6GB |
| **Index-TTS2** | rsxdalv/index_tts | Voice clone | Excellent | EN/ZH | MIT | 2-4GB |
| **Chatterbox** | rsxdalv/chatterbox | Few | Excellent | EN | MIT | 2-4GB |

### Best Free Cloud TTS APIs

| Service | Free Tier | Voices | Quality | Notes |
|---------|-----------|--------|---------|-------|
| **Microsoft Edge TTS** | Unlimited | 400+ | Excellent | Via edge-tts Python lib |
| **Google Cloud TTS** | 1M chars/mo | 380+ | Excellent | Neural2, WaveNet |
| **ElevenLabs** | 10k chars/mo | 29 | Best-in-class | Voice cloning |
| **OpenAI TTS** | Pay per use | 6 | Excellent | tts-1, tts-1-hd |
| **Coqui Studio** | Free trial | Many | Good | XTTS access |
| **PlayHT** | Free tier | 800+ | Good | Low latency |

---

## Part 3: Integrated Video + Audio Pipelines

### Complete Open-Source Solutions

| Project | Repo | Description | Key Features |
|---------|------|-------------|--------------|
| **Pixelle-Video** | AIDC-AI/Pixelle-Video | Full auto short video engine | Script→Images→Voice→Video, WebUI, ComfyUI/RunningHub/API, Edge-TTS/Index-TTS |
| **AI-VIDEO-SERVICE** | AniketRangari1998/AI-VIDEO-SERVICE | Talking avatar backend | Edge TTS + SadTalker + FFmpeg, REST API |
| **TTS-WebUI** | rsxdalv/TTS-WebUI | All-in-one TTS WebUI | 30+ TTS models, extensions, API, Silly Tavern integration |
| **LocalText2Voice** | estebanstifli/LocalText2Voice | Desktop app for audiobooks/videos | Local models + cloud APIs, editable storyboards |
| **MoneyPrinterTurbo** | harry0703/MoneyPrinterTurbo | Auto short video generator | GPT script + images + TTS + video |
| **NarratoAI** | linyqh/NarratoAI | Film commentary automation | Script + clips + voice + subtitles |
| **OpenMontage** | calesthio/OpenMontage | Agentic video production | 12 pipelines, 50+ tools, Piper TTS local mode |
| **ViMax** | HKUDS/ViMax | Multi-agent video gen | Director/Screenwriter/Producer agents |

### Talking Head / Avatar Generation

| Tool | Repo | Type | Input | Output |
|------|------|------|-------|--------|
| **SadTalker** | vinthony/SadTalker | Audio-driven face | Image + Audio | Talking head video |
| **LivePortrait** | KwaiVGI/LivePortrait | Efficient portrait | Image + Video/Audio | Animated portrait |
| **MuseTalk** | TMElyralab/MuseTalk | Real-time lip-sync | Image + Audio | Lip-synced video |
| **EchoMimicV2** | antgroup/echomimic_v2 | Semi-body animation | Image + Audio | Upper body animation |
| **OmniAvatar** | Omni-Avatar/OmniAvatar | Full-body avatar | Image + Audio | Full-body talking |
| **DA-Vinci-MagiHuman** | GAIR-NLP/daVinci-MagiHuman | Audio-video gen | Text/Image/Audio | Lip-synced talking head |
| **Duix Avatar** | duixcom/Duix-Avatar | Offline avatar toolkit | Text/Audio | Digital human video |

---

## Part 4: Recommended Architecture for SAM Videos

### Phase 1: Video-Only (Visual Summaries)

```
┌─────────────────────────────────────────────────────────────┐
│                    SAM Content Pipeline                      │
├─────────────────────────────────────────────────────────────┤
│  1. Script Generation (LLM)                                 │
│     - Input: SAM_KEY_CONCEPTS_SUMMARY.md                    │
│     - Output: Structured scripts per video topic            │
│                                                             │
│  2. Visual Asset Generation                                 │
│     Option A (Local): ComfyUI + Wan 2.1 / LTX-Video        │
│     - Workflows for: diagrams, animations, text overlays   │
│     - Consistent style via LoRA / prompt templates         │
│                                                             │
│     Option B (Cloud): fal.ai / Replicate API               │
│     - Batch generation via Python SDK                      │
│     - Models: Wan 2.1, Kling, Seedance                     │
│                                                             │
│  3. Video Assembly                                          │
│     - Remotion (React) for programmatic video composition  │
│     - Or: FFmpeg concat + overlays for simple assembly     │
│     - Or: Pixelle-Video pipeline (if using their templates)│
└─────────────────────────────────────────────────────────────┘
```

### Phase 2: Video + Natural Voice Audio

```
┌─────────────────────────────────────────────────────────────┐
│                  SAM Video + Audio Pipeline                  │
├─────────────────────────────────────────────────────────────┤
│  Phase 1 Pipeline +                                         │
│                                                             │
│  4. Voice Generation                                        │
│     Option A (Local): TTS-WebUI / Kokoro / Piper           │
│     - Consistent voice across all videos                   │
│     - Voice cloning for "expert narrator" persona          │
│                                                             │
│     Option B (Cloud): Edge TTS (free) / ElevenLabs        │
│     - edge-tts: unlimited, 400+ voices, Python native      │
│     - ElevenLabs: best quality, voice cloning, 10k free   │
│                                                             │
│  5. Lip-Sync / Talking Head (Optional)                     │
│     - SadTalker / LivePortrait for avatar presenter        │
│     - Or: Simple audio overlay on visual content           │
│                                                             │
│  6. Final Composition                                       │
│     - FFmpeg: video + audio sync                           │
│     - Add: subtitles, lower thirds, transitions            │
│     - Output: MP4 (H.264/HEVC) for YouTube/LinkedIn        │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 5: Specific Tool Recommendations for Our Stack

### For ASUS GX10 Local Compute (Recommended Priority)

| Priority | Tool | Purpose | Install |
|----------|------|---------|---------|
| **1** | **ComfyUI** | Node-based video workflow | `pip install comfyui` |
| **2** | **Wan 2.1 (1.3B)** | Primary T2V/I2V model | Via ComfyUI manager |
| **3** | **LTX-Video** | Fast iteration, real-time | Via ComfyUI manager |
| **4** | **TTS-WebUI** | All-in-one TTS server | `git clone + installer` |
| **5** | **Kokoro TTS** | Best local natural voice | Via TTS-WebUI extension |
| **6** | **Piper TTS** | Lightweight, 1000+ voices | Via TTS-WebUI extension |
| **7** | **SadTalker** | Talking head avatar | Manual setup required |
| **8** | **FFmpeg** | Video/audio processing | `winget install ffmpeg` |
| **9** | **Remotion** | Programmatic video (React) | `npm create video` |
| **10** | **Pixelle-Video** | Full pipeline alternative | Windows package or uv |

### For Cloud Compute (Our Free/Paid API Keys)

| Priority | Service | Models/Features | Our Access |
|----------|---------|-----------------|------------|
| **1** | **fal.ai** | Wan, Kling, Veo, LTX, Luma, Runway | API key in dbpasses |
| **2** | **Replicate** | 100+ video + TTS models | API key in dbpasses |
| **3** | **Microsoft Edge TTS** | Unlimited, 400+ voices | Free, no key needed |
| **4** | **Kling AI** | Daily free credits, 1080p | Web/API |
| **5** | **MiniMax/Hailuo** | Free tier, good quality | Web/API |
| **6** | **ElevenLabs** | Best TTS, voice cloning | If we have key |
| **7** | **OpenAI TTS** | High quality, 6 voices | If we have key |

---

## Part 6: Implementation Roadmap

### Week 1: Foundation (Phase 1 - Video Only)
- [ ] Set up ComfyUI on ASUS GX10
- [ ] Install Wan 2.1 1.3B and LTX-Video models
- [ ] Create SAM visual style prompt templates
- [ ] Build ComfyUI workflows for: concept diagrams, process flows, text overlays
- [ ] Test batch generation of 10 SAM concept visuals
- [ ] Set up Remotion project for programmatic video assembly
- [ ] Create video template: intro → concept → diagram → summary → outro

### Week 2: Content Production (Phase 1)
- [ ] Write scripts for 10 SAM videos from SAM_KEY_CONCEPTS_SUMMARY.md
- [ ] Generate visual assets for each video via ComfyUI
- [ ] Assemble videos in Remotion with transitions, text overlays
- [ ] Export MP4s, review quality
- [ ] Create thumbnails and metadata

### Week 3: Audio Integration (Phase 2)
- [ ] Set up TTS-WebUI locally (or use edge-tts cloud)
- [ ] Select/clone consistent narrator voice (Kokoro or Edge TTS)
- [ ] Generate audio for all 10 scripts
- [ ] Optional: Set up SadTalker for talking head intros
- [ ] Sync audio with video in FFmpeg/Remotion
- [ ] Add subtitles (Whisper for alignment)

### Week 4: Polish & Deploy
- [ ] Quality review all videos
- [ ] Create YouTube/LinkedIn optimized versions
- [ ] Build video index/playlist page
- [ ] Document pipeline for future topics

---

## Part 7: Cost Analysis

### Local Compute (ASUS GX10) - One-time Setup
- **Hardware**: Already owned
- **Electricity**: ~$0.50-1.00 per hour of GPU use
- **Storage**: 50-100GB for models
- **Time**: 1-2 days setup

### Cloud Compute (Per Video Estimates)
| Service | Cost per 10-sec clip | Cost per 3-min video |
|---------|---------------------|---------------------|
| fal.ai (Wan 2.1) | ~$0.05 | ~$0.90 |
| fal.ai (Kling) | ~$0.10 | ~$1.80 |
| Replicate (Wan) | ~$0.08 | ~$1.44 |
| Edge TTS | **FREE** | **FREE** |
| ElevenLabs | ~$0.01/1k chars | ~$0.03 |

**Estimated 10-video series (3 min each)**:
- Local video gen: $0 (electricity only)
- Cloud video gen: $9-18 (fal.ai/Replicate)
- Local TTS: $0
- Cloud TTS (Edge): $0
- **Total: $0-18** for complete series

---

## Part 8: Key GitHub Repos to Clone/Reference

```bash
# Core video generation
git clone https://github.com/comfyanonymous/ComfyUI
git clone https://github.com/Wan-Video/Wan2.1
git clone https://github.com/Lightricks/LTX-Video

# TTS
git clone https://github.com/rsxdalv/TTS-WebUI
git clone https://github.com/hexgrad/kokoro
git clone https://github.com/rhasspy/piper

# Talking head
git clone https://github.com/vinthony/SadTalker
git clone https://github.com/KwaiVGI/LivePortrait

# Full pipelines
git clone https://github.com/AIDC-AI/Pixelle-Video
git clone https://github.com/AniketRangari1998/AI-VIDEO-SERVICE
git clone https://github.com/harry0703/MoneyPrinterTurbo

# Programmatic video
npx create video@latest sam-videos  # Remotion

# Awesome lists for reference
git clone https://github.com/backblaze-labs/awesome-video-generation
git clone https://github.com/ishandutta2007/Video-Generation-Landscape
git clone https://github.com/augstai/awesome-ai-video-generation
```

---

## Part 9: SAM-Specific Visual Style Guidelines

### Consistent Visual Language for All SAM Videos

| Element | Specification |
|---------|---------------|
| **Color Palette** | ServiceNow blue (#0066CC), white, dark gray (#1E1E1E), accent green (#00B33C) for compliant, red (#E53935) for under-licensed, yellow (#FFB300) for over-licensed |
| **Typography** | Inter/Roboto for UI, JetBrains Mono for code/tables |
| **Diagrams** | Mermaid-style flowcharts, consistent node shapes |
| **Icons** | Lucide/Phosphor icon set |
| **Transitions** | Smooth fade/slide, 0.3s duration |
| **Lower Thirds** | "SAM Concept: [Title]" format |
| **Watermark** | Subtle "ServiceNow SAM Expert Series" |

### Video Structure Template (3-5 minutes each)

```
0:00-0:15  Hook + Topic Title + Why It Matters
0:15-0:45  Core Concept (ELI5 analogy)
0:45-2:00  Deep Dive (diagrams, tables, examples)
2:00-2:30  Common Mistakes / Interview Traps
2:30-3:00  Key Takeaways + Mnemonics
3:00-3:15  Preview Next Video + CTA
```

---

## Conclusion

**For Phase 1 (Video Only)**: Start with **ComfyUI + Wan 2.1 1.3B** on ASUS GX10 for local control, or **fal.ai API** for faster iteration. Use **Remotion** for programmatic assembly.

**For Phase 2 (Video + Audio)**: Add **edge-tts (Microsoft Edge TTS)** for free unlimited natural voices, or **TTS-WebUI with Kokoro** locally. Optional **SadTalker** for talking head presenter.

**Total Investment**: $0-20 for complete 10-video SAM mastery series using mostly free/local tools.

The SAM_KEY_CONCEPTS_SUMMARY.md provides all content needed — now it's a production pipeline task.