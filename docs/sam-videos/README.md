# ServiceNow SAM Video Series

**CIS-SAM Interview Preparation & Technical Mastery**

This video series covers all 12 core modules of ServiceNow Software Asset Management (SAM), designed for CIS-SAM exam preparation and demonstrating expert-level technical knowledge in job interviews.

---

## 🎬 Full Video Curriculum (12 Videos)

| # | Title | Duration | Status | Link |
|---|-------|----------|--------|------|
| 1 | SAM in 60 Seconds | 58s | ✅ Complete | [Watch](./video_01_final.mp4) |
| 2 | The Chain — Install → Discovery → Model → Entitlement → Result | 95s | ✅ Complete | [Watch](./video_02_final.mp4) |
| 3 | Normalization (SUMN) Deep Dive | 4 min | 📋 Planned | — |
| 4 | Entitlements: Contracts, Metrics, and Hygiene | 4 min | 📋 Planned | — |
| 5 | Reconciliation Engine Explained | 4 min | 📋 Planned | — |
| 6 | Compliance Positions — 6 States, Unknown ≠ Compliant | 3 min | 📋 Planned | — |
| 7 | Publisher Traps — Microsoft, Oracle, IBM, SAP, Adobe | 5 min | 📋 Planned | — |
| 8 | SaaS License Management | 3 min | 📋 Planned | — |
| 9 | Optimization & Reclamation — Where SAM Pays for Itself | 3 min | 📋 Planned | — |
| 10 | Top 8 SAM Traps — Exam & Real World | 3 min | 📋 Planned | — |
| 11 | CIS-SAM Exam Map & Study Strategy | 3 min | 📋 Planned | — |
| 12 | Lab Walkthrough: Entitlement → Reconciliation → Compliance | 4 min | 📋 Planned | — |

---

## 📚 Summary: Long-Form Grouped Sections

### Section 1: SAM Foundations (Videos 1–2)
**Runtime:** ~2.5 minutes  
**Core Concepts:** One-sentence SAM definition, SAM vs HAM vs ITAM, The Chain (I-D-S-E-R), Three Record Types, Business Case

### Section 2: Data Integrity & Normalization (Videos 3–4)
**Runtime:** ~8 minutes  
**Core Concepts:** SUMN normalization pipeline, Content Library & Publisher Packs, 6 Normalization Statuses, Suite Roll-up, License Metrics, Entitlement Hygiene, Metric Mismatch Trap

### Section 3: Reconciliation & Compliance (Videos 5–6)
**Runtime:** ~7 minutes  
**Core Concepts:** Reconciliation Step-by-Step, Three Tiers (Product, Model, Metric), 6 Compliance Positions, Unknown ≠ Compliant, Financial Meaning

### Section 4: Publisher-Specific & SaaS (Videos 7–8)
**Runtime:** ~8 minutes  
**Core Concepts:** Microsoft (SQL Server core factor, M365 bundles), Oracle (server-level, core factor, LMS scripts), IBM (PVU, ILMT), SAP (indirect access), Adobe (suite roll-up), SaaS connectors, Seat utilization, Dead connector trap

### Section 5: Optimization, Exam & Lab (Videos 9–12)
**Runtime:** ~14 minutes  
**Core Concepts:** Reclamation priority, 60-90 day rule, Top 8 traps, CIS-SAM domain weights, Lab walkthrough (7 steps), Mnemonics (I-D-S-E-R, BAA, LOCS)

---

## 🔗 Key Resources

- **GitHub Repository:** [alt_parallelswarm_SAM](https://github.com/eltonaguiar/alt_parallelswarm_SAM)
- **ServiceNow SAM Guide:** [Live Documentation](https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/)
- **Source Content:** [SAM_KEY_CONCEPTS.md](../videos/SAM_KEY_CONCEPTS.md)

---

## 📋 Video Metadata

| Field | Value |
|-------|-------|
| Repository | alt_parallelswarm_SAM |
| Folder | videos/ |
| Worktree | samvideos-v4 |
| Generated | 2026-11-14 |
| Phase 1 | Visual only (YAML → PPTX → MP4) |
| Phase 2 | Audio + Subtitles (edge-tts + SRT + FFmpeg) |

---

## 📦 Video Files (Phase 2 Complete)

| File | Duration | Size | Description |
|------|----------|------|-------------|
| video_01_final.mp4 | 58s | 3.2 MB | SAM in 60 Seconds with narration |
| video_02_final.mp4 | 95s | 265 KB | The Chain with narration |
| video_01_silent.mp4 | 58s | 797 KB | Phase 1 silent version |
| video_02_silent.mp4 | 5s | 67 KB | Phase 1 silent version |

Subtitles: [video_01.srt](./subtitles/video_01.srt) | [video_02.srt](./subtitles/video_02.srt)

---

## 🚀 Build Pipeline

```yaml
# GitHub Actions: .github/workflows/render-sam-videos.yml
# Trigger: Push to videos/content/** or videos/scripts/**
# Output: videos/output/video_*.mp4 (committed to repo)
# Deploy: docs/sam-videos/ (GitHub Pages)
```

---

## 📝 Notes

- All videos use **edge-tts (en-US-AriaNeural)** for narration (free, unlimited, natural)
- Subtitles are **slide-aligned** to match YAML `duration` fields exactly
- **No overlapping captions** — each subtitle segment corresponds to its visual slide
- Format: 1920×1080, 30fps, H.264 (libx264), AAC 192kbps
- Target: CIS-SAM exam preparation & job interview demonstration