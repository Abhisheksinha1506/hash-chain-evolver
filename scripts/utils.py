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

### 🤖 The "Robot Gardener" Analogy
Imagine a garden that is tended by a robot. Every few hours, the robot looks at its own **digital fingerprint** (a long string of numbers). 
- If the fingerprint ends in an **even number**, the robot plants a new "discovery" file. 
- If it's **odd**, it prunes the oldest file to make room. 
- If it's a **prime number**, it reorganizes the entire garden layout.

This repository is that garden—completely autonomous, growing and changing forever based on its own mathematical pulse.

## 📊 Live Garden Stats
- **Total Growth Steps:** {step_number}
- **Active Digital Lifeforms:** {feature_count}
- **Last Pulse Detected:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}

## 🕹️ The Game Rules
Each evolution is determined by the "DNA" of the last update:
- **🌱 BIRTH (Even):** A new feature is born.
- **🍂 PRUNE (Odd):** Space is cleared for new growth.
- **🔧 EVOLVE (Prime):** The codebase reorganizes itself.
- **⚡ TIGHTEN (÷10):** Code is cleaned and optimized.
- **📝 ARCHIVE (÷7):** Documentation is refreshed.

## 🧐 Why?
To explore how software can evolve without human hands, using nothing but the pure, deterministic chaos of cryptographic hashes.

---
### 🔗 Explore
- [**Live Dashboard**](https://abhisheksinha1506.github.io/hash-chain-evolver/) - Visual status monitor.
- [**Evolution Log**](docs/EVOLUTION_LOG.md) - The complete history of every change.
- [**Genesis**](GENESIS.md) - The first heartbeat of the system.

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
