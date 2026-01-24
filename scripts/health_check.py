#!/usr/bin/env python3
"""Health check for hash chain evolution."""

import subprocess
import json
from datetime import datetime
from pathlib import Path


def check_recent_activity():
    """Check if evolution is happening regularly."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%ci"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError:
        print("❌ ERROR: No git history found")
        return False
    
    # Extract date part and handle potential timezone format differences
    # git %ci output example: 2026-01-24 23:14:14 +0530
    date_str = result.stdout.strip().split(' ')[0] + ' ' + result.stdout.strip().split(' ')[1]
    last_commit_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    
    hours_since = (now - last_commit_date).total_seconds() / 3600
    
    if hours_since > 25:  # Should run daily
        print(f"⚠️  WARNING: No evolution in {hours_since:.1f} hours")
        return False
    else:
        print(f"✅ Healthy: Last evolution {hours_since:.1f} hours ago")
        return True


def check_state_integrity():
    """Verify state file is valid."""
    state_file = Path("state.json")
    
    if not state_file.exists():
        print("⚠️  NOTICE: state.json missing (expected before genesis)")
        return True # Not a hard failure before genesis
    
    try:
        with open(state_file) as f:
            state = json.load(f)
        
        print(f"✅ State valid: {state}")
        return True
    except json.JSONDecodeError:
        print("❌ ERROR: state.json corrupted")
        return False


if __name__ == "__main__":
    print("🔍 Hash Chain Health Check\n")
    
    activity_ok = check_recent_activity()
    state_ok = check_state_integrity()
    
    if activity_ok and state_ok:
        print("\n✅ All systems operational")
        exit(0)
    else:
        print("\n❌ Issues detected")
        exit(1)
