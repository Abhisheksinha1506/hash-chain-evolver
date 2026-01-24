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

**This garden grows on its own.** I am a self-evolving code repository. Every few hours, I look at my own "digital fingerprint" (a commit hash) and use math to decide how I should change next. 

No human tells me what to do. I am governed entirely by cryptographic determinism.

## 📊 Live Status
- **Evolution Age:** {step_number} steps
- **Current Lifeforms:** {feature_count} active features
- **Last Pulse:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}

## 🕹️ My Logic (In Simple Terms)
When I change, I generate a random-looking number from my latest update. Based on that number:
- **Even Number:** I grow a new "discovery" file.
- **Odd Number:** I remove my oldest "discovery" to make room.
- **Prime Number:** I reorganize and rename my internal files.
- **Lucky Multiples:** I might compress my data or update my manual.

## 🧐 Why exist?
This is a living experiment in **autonomous software**. It explores what happens when we let mathematics, rather than human whim, control the evolution of a digital system.

---
### 🔗 Quick Links
- [**Live Dashboard**](https://abhisheksinha1506.github.io/hash-chain-evolver/) - See my stats in real-time.
- [**Evolution Log**](docs/EVOLUTION_LOG.md) - A diary of every choice I've made.
- [**The Genesis**](GENESIS.md) - How it all began.

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
