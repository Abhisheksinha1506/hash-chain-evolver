#!/usr/bin/env python3
"""Visualize the hash chain as a graph."""

import subprocess
import json
from pathlib import Path


def get_commit_chain():
    """Get all commits with their hashes."""
    try:
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H|%s|%ci", "--all"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError:
        return []
    
    commits = []
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split('|')
            if len(parts) >= 3:
                hash_val, message, date = parts[0], parts[1], parts[2]
                commits.append({
                    "hash": hash_val,
                    "hash_value": int(hash_val[-2:], 16),
                    "message": message,
                    "date": date
                })
    
    return commits


def generate_mermaid_diagram():
    """Generate Mermaid diagram of hash chain."""
    commits = get_commit_chain()[:20]  # Last 20 commits
    
    if not commits:
        return "No commits found to visualize."
    
    diagram = ["```mermaid", "graph TD"]
    
    for i, commit in enumerate(commits):
        hash_short = commit["hash"][:8]
        hash_val = commit["hash_value"]
        
        node_id = f"C{i}"
        label = f"{hash_short}<br/>Value: {hash_val}"
        
        diagram.append(f'    {node_id}["{label}"]')
        
        if i > 0:
            diagram.append(f'    {node_id} --> C{i-1}')
    
    diagram.append("```")
    
    return "\n".join(diagram)


if __name__ == "__main__":
    mermaid = generate_mermaid_diagram()
    
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    output_file = docs_dir / "CHAIN_VISUALIZATION.md"
    with open(output_file, "w") as f:
        f.write("# Hash Chain Visualization\n\n")
        f.write(mermaid)
    
    print(f"✅ Visualization saved to {output_file}")
