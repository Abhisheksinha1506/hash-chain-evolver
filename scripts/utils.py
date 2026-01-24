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
    
    readme_content = f"""# Hash Chain Evolver

A self-evolving repository driven by cryptographic determinism.

## Current State

- **Evolution Steps:** {step_number}
- **Active Features:** {feature_count}
- **Last Updated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}

## How It Works

Each commit's SHA-256 hash deterministically controls the next evolution step:

| Hash Condition | Action |
|----------------|--------|
| Even number | Create new feature |
| Odd number | Delete oldest feature |
| Prime number | Refactor codebase |
| Divisible by 10 | Optimize files |
| Divisible by 7 | Update documentation |
| Ends in 0 | Create version tag |

## Evolution Rules

The last byte of each commit hash (0-255) determines the transformation:
- **Even:** Generates `feature_<N>.txt`
- **Odd:** Removes oldest feature file
- **Prime:** Renames files with `refactored_` prefix
- **÷10:** Compresses content
- **÷7:** Updates this README
- **Ends in 0:** Creates git tag `v<step>`

## Watch the Evolution

Check the [commit history](../../commits/main) to see the deterministic chain unfold.

See [EVOLUTION_LOG.md](EVOLUTION_LOG.md) for detailed step-by-step log.

---

*This repository evolves autonomously. No human intervention required.*
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
    return {"features_created": 0, "features_deleted": 0, "refactors": 0}
