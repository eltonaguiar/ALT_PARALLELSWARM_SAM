#!/bin/bash
# SAM Videos - Environment Setup Script
# Run on ASUS GX10 (Ubuntu/WSL2) to set up Phase 1 video generation environment

set -e

echo "========================================="
echo "SAM Videos - Phase 1 Environment Setup"
echo "========================================="

# Configuration
WORKSPACE="/home/eaguiar2015/findtorontoevents_antigravity.ca/.kilo/worktrees/samvideos-v3/videos"
COMFYUI_DIR="$HOME/ComfyUI"
NODE_VERSION="22"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${GREEN}[SETUP]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check prerequisites
check_prereqs() {
    log "Checking prerequisites..."
    
    # Python 3.10+
    if ! command -v python3.10 &> /dev/null && ! command -v python3.11 &> /dev/null; then
        error "Python 3.10+ required. Install via: sudo apt install python3.11 python3.11-venv"
        exit 1
    fi
    
    # Git
    if ! command -v git &> /dev/null; then
        error "Git not found. Install via: sudo apt install git"
        exit 1
    fi
    
    # NVIDIA GPU check
    if command -v nvidia-smi &> /dev/null; then
        log "NVIDIA GPU detected:"
        nvidia-smi --query-gpu=name,memory.total --format=csv
    else
        warn "No NVIDIA GPU detected. CPU-only mode will be very slow."
    fi
    
    # FFmpeg
    if ! command -v ffmpeg &> /dev/null; then
        warn "FFmpeg not found. Will install via package manager."
    fi
}

# Install system dependencies
install_system_deps() {
    log "Installing system dependencies..."
    
    sudo apt update
    sudo apt install -y \
        python3.11 python3.11-venv python3.11-dev \
        git ffmpeg \
        build-essential cmake \
        libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1-mesa-glx \
        wget curl
}

# Setup ComfyUI
setup_comfyui() {
    log "Setting up ComfyUI..."
    
    if [ ! -d "$COMFYUI_DIR" ]; then
        git clone https://github.com/comfyanonymous/ComfyUI "$COMFYUI_DIR"
    else
        log "ComfyUI already exists, updating..."
        cd "$COMFYUI_DIR" && git pull
    fi
    
    cd "$COMFYUI_DIR"
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        python3.11 -m venv venv
    fi
    
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Install ComfyUI Manager
    cd custom_nodes
    if [ ! -d "ComfyUI-Manager" ]; then
        git clone https://github.com/ltdrdata/ComfyUI-Manager
    fi
    
    # Essential custom nodes for video
    declare -a nodes=(
        "https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite"
        "https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved"
        "https://github.com/Fannovel16/comfyui_controlnet_aux"
        "https://github.com/cubiq/ComfyUI_essentials"
        "https://github.com/ltdrdata/ComfyUI-Impact-Pack"
    )
    
    for node in "${nodes[@]}"; do
        name=$(basename "$node" .git)
        if [ ! -d "$name" ]; then
            log "Installing $name..."
            git clone "$node"
        fi
    done
    
    # Install node dependencies
    for node in "${nodes[@]}"; do
        name=$(basename "$node" .git)
        if [ -f "$name/requirements.txt" ]; then
            pip install -r "$name/requirements.txt"
        fi
    done
}

# Download models
download_models() {
    log "Downloading models (this will take a while)..."
    
    cd "$COMFYUI_DIR"
    source venv/bin/activate
    
    # Use ComfyUI Manager CLI to download models
    # Wan 2.1 1.3B (T2V/I2V)
    python -c "
from comfyui_manager import model_manager
model_manager.download_model('wan2.1_t2v_1.3b')
model_manager.download_model('wan2.1_i2v_1.3b')
model_manager.download_model('ltx_video_2b')
" 2>/dev/null || warn "ComfyUI Manager model download not available via CLI. Download manually via UI."
    
    log "Models can also be downloaded via ComfyUI Manager UI at http://localhost:8188"
    log "Search for: wan2.1, ltx_video, animate_diff"
}

# Setup Remotion project
setup_remotion() {
    log "Setting up Remotion project..."
    
    cd "$WORKSPACE"
    
    if [ ! -d "sam-video-series" ]; then
        npx create video@latest sam-video-series --yes
        cd sam-video-series
        npm install
    else
        log "Remotion project exists, updating dependencies..."
        cd sam-video-series && npm install
    fi
}

# Create project structure
create_structure() {
    log "Creating project directory structure..."
    
    cd "$WORKSPACE"
    
    mkdir -p \
        scripts \
        workflows \
        assets/clips \
        final \
        thumbnails \
        sam-video-series/src/assets/clips
    
    # Symlink clips directory for Remotion access
    ln -sf "$WORKSPACE/assets/clips" "$WORKSPACE/sam-video-series/src/assets/clips"
}

# Generate video scripts from SAM summary
generate_scripts() {
    log "Generating video scripts from SAM_KEY_CONCEPTS_SUMMARY.md..."
    
    cat > "$WORKSPACE/scripts/generate_video_scripts.py" << 'PYEOF'
#!/usr/bin/env python3
"""Generate video scripts from SAM_KEY_CONCEPTS_SUMMARY.md"""

import json
import re
from pathlib import Path

SUMMARY_FILE = Path(__file__).parent.parent / "SAM_KEY_CONCEPTS_SUMMARY.md"
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts" / "video_scripts"
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

# Video definitions based on summary
VIDEOS = [
    {
        "id": 1,
        "title": "SAM Overview: What, Why, How",
        "source_sections": ["Purpose", "SAM vs HAM vs ITAM", "Where to Find It"],
        "duration": 180,
        "key_points": [
            "SAM reconciles entitlements vs installs/usage",
            "SAM vs HAM vs ITAM comparison table",
            "ELI5 analogy: 1000 entitlements, 1180 installs, 1090 users = 90 under",
            "SAM lifecycle diagram",
            "CIS-SAM domain 1 (15%)"
        ]
    },
    {
        "id": 2,
        "title": "The Three Record Types You Must Know",
        "source_sections": ["The Three Record Types You Must Never Confuse"],
        "duration": 240,
        "key_points": [
            "Software Model vs Discovery Model vs Installation vs Entitlement vs Reconciliation Result",
            "Table with tables, meanings, creators",
            "Rule of thumb: Model=what it is, Entitlement=what you may use, Install=what exists, Usage=what is used, Reconciliation=difference"
        ]
    },
    {
        "id": 3,
        "title": "Normalization Deep Dive: SUMN & Content Library",
        "source_sections": ["Software Models & Normalization (SUMN)"],
        "duration": 300,
        "key_points": [
            "Why normalization matters: 40 variants of 'Microsoft Office'",
            "6 normalization statuses",
            "Suite membership critical for Oracle, Microsoft, Adobe",
            "Normalization workflow steps 1-5",
            "Content Library publisher packs"
        ]
    },
    {
        "id": 4,
        "title": "Entitlements & License Metrics",
        "source_sections": ["Entitlements — The Contract Side", "Key Fields"],
        "duration": 240,
        "key_points": [
            "7 must-have entitlement attributes",
            "Metric mismatch = #1 silent reconciliation failure",
            "License types: perpetual vs subscription vs maintenance",
            "Entitlement hygiene rules",
            "Key fields table"
        ]
    },
    {
        "id": 5,
        "title": "Reconciliation Engine: How Compliance Is Calculated",
        "source_sections": ["Reconciliation — The Core Engine", "Reconciliation Flow Diagram", "Compliance Position States", "Publisher-Specific Rules Flow", "SaaS License Management Flow"],
        "duration": 300,
        "key_points": [
            "Step-by-step reconciliation process",
            "Formula: Compliance = f(entitlement, installs, usage, metric, rules)",
            "4 compliance states with financial meaning",
            "What breaks reconciliation table",
            "Publisher-specific rules flow",
            "SaaS flow differences"
        ]
    },
    {
        "id": 6,
        "title": "Compliance Positions Explained",
        "source_sections": ["Compliance Positions Explained"],
        "duration": 240,
        "key_points": [
            "6 positions: Compliant, Over-licensed, Under-licensed, Unlicensed, Not counted, Unknown",
            "Meaning, financial meaning, typical action for each",
            "Exam-critical: Unknown != Compliant",
            "State transition diagram"
        ]
    },
    {
        "id": 7,
        "title": "Publisher-Specific Traps",
        "source_sections": ["Publisher-Specific Traps"],
        "duration": 300,
        "key_points": [
            "Microsoft: SQL Server cores, virtualization, M365 overlap, downgrade rights",
            "Oracle: Core factors, server not VM licensing, LMS scripts, NUP minimums",
            "IBM: PVU tables, sub-capacity needs ILMT",
            "SAP: Named-user classification, indirect access",
            "Adobe: VIP/ETLA, shared-device, CC suite roll-up",
            "ServiceNow: Subscription by product/fulfilled user"
        ]
    },
    {
        "id": 8,
        "title": "SaaS License Management & Seat Reclamation",
        "source_sections": ["SaaS License Management", "Optimization & Reclamation"],
        "duration": 240,
        "key_points": [
            "On-premise vs SaaS comparison table",
            "Classic waste: 260/1000 M365 E5 never signed in 90 days = 26% savings",
            "Connector configuration essentials",
            "Reclamation workflow with 60-90 day inactivity window"
        ]
    },
    {
        "id": 9,
        "title": "Optimization & Reclamation Strategies",
        "source_sections": ["Optimization & Reclamation", "Common Mistakes"],
        "duration": 240,
        "key_points": [
            "Priority order: 1) Reclaim seats 2) Uninstall 3) Right-size 4) Consolidate 5) Align renewals 6) Enforce process",
            "Reclamation workflow steps",
            "Top 12 common mistakes table",
            "Key metrics for SAM program health"
        ]
    },
    {
        "id": 10,
        "title": "CIS-SAM Exam Prep: Domains, Quiz, Mnemonics",
        "source_sections": ["Official Exam Alignment — CIS-Software Asset Management", "Quiz", "Memory Aids & Mnemonics"],
        "duration": 240,
        "key_points": [
            "5 domains with weights: 15%, 25%, 30%, 20%, 10%",
            "Quiz questions 1-8 with answers",
            "Mnemonics: BAA, LOCS, IRE, ARM, etc.",
            "Lab walkthrough: Entitlement → Reconciliation → Compliance",
            "Official learning resources"
        ]
    }
]

def generate_script(video):
    """Generate detailed script JSON for a video."""
    scenes = []
    
    # Hook scene
    scenes.append({
        "id": "hook",
        "duration": 15,
        "type": "text_reveal",
        "content": f"Master {video['title']} — the concept that separates SAM novices from experts."
    })
    
    # Key points as scenes
    for i, point in enumerate(video['key_points']):
        if "table" in point.lower() or "comparison" in point.lower():
            scene_type = "comparison_table"
        elif "diagram" in point.lower() or "flow" in point.lower() or "workflow" in point.lower():
            scene_type = "flow_diagram"
        elif "mnemonic" in point.lower() or "memory" in point.lower():
            scene_type = "mnemonic_card"
        elif "analogy" in point.lower() or "eli5" in point.lower():
            scene_type = "analogy_visual"
        else:
            scene_type = "concept_card"
        
        scenes.append({
            "id": f"point_{i+1}",
            "duration": max(30, video['duration'] // len(video['key_points'])),
            "type": scene_type,
            "content": point
        })
    
    # Outro
    next_title = VIDEOS[video['id']]['title'] if video['id'] < len(VIDEOS) else None
    scenes.append({
        "id": "outro",
        "duration": 15,
        "type": "outro",
        "content": f"Next: {next_title}" if next_title else "Series complete! You're now SAM interview-ready."
    })
    
    return {
        "videoId": video['id'],
        "title": video['title'],
        "duration": video['duration'],
        "scenes": scenes
    }

if __name__ == "__main__":
    for video in VIDEOS:
        script = generate_script(video)
        out_file = SCRIPTS_DIR / f"video_{video['id']:02d}_{video['title'].lower().replace(' ', '_').replace(':', '').replace('&', 'and')}.json"
        with open(out_file, 'w') as f:
            json.dump(script, f, indent=2)
        print(f"Generated: {out_file}")
    
    print(f"\nAll {len(VIDEOS)} video scripts generated in {SCRIPTS_DIR}")
PYEOF

    python3 "$WORKSPACE/scripts/generate_video_scripts.py"
}

# Main execution
main() {
    echo "Starting SAM Videos Phase 1 setup..."
    
    check_prereqs
    install_system_deps
    setup_comfyui
    download_models
    setup_remotion
    create_structure
    generate_scripts
    
    echo ""
    echo "========================================="
    echo "Setup Complete!"
    echo "========================================="
    echo ""
    echo "Next steps:"
    echo "1. Start ComfyUI: cd ~/ComfyUI && source venv/bin/activate && python main.py --listen 0.0.0.0 --port 8188"
    echo "2. Open http://localhost:8188 and download models via Manager: wan2.1, ltx_video, animate_diff"
    echo "3. Review generated scripts in: $WORKSPACE/scripts/video_scripts/"
    echo "4. Create ComfyUI workflows for each scene type"
    echo "5. Build Remotion compositions in: $WORKSPACE/sam-video-series/"
    echo "6. Follow PHASE1_IMPLEMENTATION_PLAN.md for detailed steps"
    echo ""
    echo "Key files:"
    echo "  - Content: $WORKSPACE/SAM_KEY_CONCEPTS_SUMMARY.md"
    echo "  - Plan: $WORKSPACE/PHASE1_IMPLEMENTATION_PLAN.md"
    echo "  - Research: $WORKSPACE/research/VIDEO_GENERATION_TOOLS_RESEARCH.md"
}

main "$@"