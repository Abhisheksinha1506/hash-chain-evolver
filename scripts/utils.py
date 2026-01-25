#!/usr/bin/env python3
"""Utility functions for hash chain evolution."""

import hashlib
import os
import json
from datetime import datetime
from pathlib import Path

# Project root directory (one level up from scripts/)
ROOT_DIR = Path(__file__).parent.parent.absolute()


def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def get_hash_value(commit_hash):
    """Extract numeric value from last byte of hash."""
    last_byte = commit_hash[-2:]  # Last 2 hex chars = 1 byte
    return int(last_byte, 16)  # Convert hex to decimal (0-255)


def log_evolution(action, hash_value, commit_hash, details):
    """Log evolution step to EVOLUTION_LOG.md and docs/EVOLUTION_LOG.md."""
    log_files = [ROOT_DIR / "EVOLUTION_LOG.md", ROOT_DIR / "docs" / "EVOLUTION_LOG.md"]
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    entry = f"""
## Evolution Step {get_step_number()}

- **Timestamp:** {timestamp}
- **Commit Hash:** `{commit_hash[:8]}`
- **Hash Value:** {hash_value} (0x{hash_value:02X})
- **Action:** {action}
- **Details:** {details}

---
"""
    
    for log_file in log_files:
        if log_file.exists():
            with open(log_file, "a") as f:
                f.write(entry)
        else:
            # Ensure directory exists for docs/
            log_file.parent.mkdir(exist_ok=True)
            with open(log_file, "w") as f:
                f.write("# Hash Chain Evolution Log\n\n")
                f.write(entry)


def get_step_number():
    """Get current evolution step number."""
    # Use root log as source of truth
    log_file = ROOT_DIR / "EVOLUTION_LOG.md"
    if not log_file.exists():
        # Fallback to docs log
        log_file = ROOT_DIR / "docs" / "EVOLUTION_LOG.md"
    
    if not log_file.exists():
        return 1
    
    with open(log_file, "r") as f:
        content = f.read()
        return content.count("## Evolution Step") + 1


def update_readme_stats():
    """Update README.md with current statistics."""
    features_dir = ROOT_DIR / "features"
    feature_count = len(list(features_dir.glob("*.txt"))) if features_dir.exists() else 0
    
    step_number = get_step_number()
    
    readme_content = f"""# 🧬 Hash Chain Evolver

### "A digital garden that grows by its own mathematical pulse."

**Hash Chain Evolver** is an autonomous code repository. Unlike normal software that humans write and update, this project changes itself automatically using its own "digital DNA" (commit hashes).

## 🏮 The Simple Analogy
Imagine a **self-playing piano**. Instead of a musician choosing the notes, the piano looks at the pattern of its last performance to decide what to play next. 

In this project:
1. Every hour, the system wakes up.
2. It looks at its latest "fingerprint" (the commit hash).
3. It uses that code to decide whether to **birth** a new file, **decay** an old one, or **evolve** its internal structure.

## 📊 Live Status
- **Evolution Age:** {step_number} steps
- **Current Lifeforms:** {feature_count} active features
- **Last Pulse:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}

## 🕹️ The Rules of Growth
Every hour, a "mathematical pulse" (a number from 0-255) is extracted from the latest commit:
- **Even Number (BIRTH):** A new "discovery" file is created.
- **Odd Number (DECAY):** The oldest file is recycled to make room.
- **Prime Number (METAMORPHOSIS):** Internal files are renamed and reorganized.
- **Lucky Multiples (PURIFICATION):** Data is cleaned and optimized.
- **Pulse % 13 (INGESTION):** The system "hears" an Issue and weaves it into the chain.
- **Pulse % 17 (MUTATION):** The system "absorbs" a Pull Request as a genetic mutation.

## 🧐 Why exist?
This is an experiment in **deterministic chaos**. It's built to see how a system can evolve into a complex structure without a single human decision. It's half-code, half-art, and entirely math.

---
### 🔗 Watch the Growth
- [**Live Dashboard**](https://abhisheksinha1506.github.io/hash-chain-evolver/) - See the statistics in real-time.
- [**Evolution Log**](docs/EVOLUTION_LOG.md) - Read the diary of every pulse.
- [**Chain Visualization**](docs/CHAIN_VISUALIZATION.md) - See the mathematical connections.

---
*Observe, don't interfere. The chain evolves regardless.*
"""
    
    with open(ROOT_DIR / "README.md", "w") as f:
        f.write(readme_content)


def save_state(state_data):
    """Save current state to JSON in root and docs/."""
    state_files = [ROOT_DIR / "state.json", ROOT_DIR / "docs" / "state.json"]
    for state_file in state_files:
        state_file.parent.mkdir(exist_ok=True)
        with open(state_file, "w") as f:
            json.dump(state_data, indent=2, fp=f)


def load_state():
    """Load state from JSON."""
    # Try root first, then docs
    state_files = [ROOT_DIR / "state.json", ROOT_DIR / "docs" / "state.json"]
    for state_file in state_files:
        if state_file.exists():
            with open(state_file, "r") as f:
                return json.load(f)
    return {"features_created": 0, "features_deleted": 0, "refactors": 0, "last_processed_hash": ""}
