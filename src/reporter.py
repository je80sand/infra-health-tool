"""
reporter.py

Responsible for saving reports to disk.

We support:
- JSON report (main report)
- Markdown report (human-friendly)
"""

import json
import os
from datetime import datetime


def ensure_reports_folder():
    """Make sure reports/ exists."""
    os.makedirs("reports", exist_ok=True)


def save_json_report(full_report):
    """
    Save the full report to reports/ as JSON.
    Returns the path to the saved file.
    """
    ensure_reports_folder()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"health_report_{timestamp}.json"
    path = os.path.join("reports", filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=2)

    return path


def save_markdown_report(full_report):
    """
    Save a human-readable Markdown report to reports/.
    Returns the path to the saved file.
    """
    ensure_reports_folder()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"health_report_{timestamp}.md"
    path = os.path.join("reports", filename)

    system = full_report["system_metrics"]
    logs = full_report["log_analysis"]

    cpu = system["cpu"]["usage_percent"]
    mem = system["memory"]["usage_percent"]
    disk = system["disk"]["usage_percent"]

    lines = []
    lines.append(f"# Infrastructure Health Report\n\n")
    lines.append(f"**Generated:** {system['timestamp']}\n\n")

    lines.append("## System\n")
    lines.append(f"- OS: **{system['system']['os']}**\n")
    lines.append(f"- Hostname: **{system['system']['hostname']}**\n\n")

    lines.append("## Metrics\n")
    lines.append(f"- CPU Usage: **{cpu}%**\n")
    lines.append(f"- Memory Usage: **{mem}%**\n")
    lines.append(f"- Disk Usage: **{disk}%**\n\n")

    lines.append("## Log Analysis\n")
    lines.append(f"- Logs folder: **{logs['logs_dir']}**\n")
    lines.append(f"- Files scanned: **{logs['files_scanned']}**\n\n")

    lines.append("### Problem Counts\n")
    for key, value in logs["problem_counts"].items():
        lines.append(f"- {key}: **{value}**\n")
    lines.append("\n")

    lines.append("### Example Matches (first few)\n")
    for key, examples in logs.get("examples", {}).items():
        if examples:
            lines.append(f"**{key}**\n")
            for ex in examples:
                lines.append(f"- `{ex}`\n")
            lines.append("\n")

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return path