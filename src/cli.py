"""
cli.py

Entry point for the Infrastructure Health Tool.

Runs:
- System metrics collection (CPU, memory, disk, OS info)
- Log parsing (keyword matches)
- JSON report generation (saved to reports/)

Usage examples:
  python3 cli.py
  python3 cli.py --json-only
  python3 cli.py --cpu-warn 70 --mem-warn 75 --disk-warn 85
  python3 cli.py --logs-dir ../logs --output-dir reports
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from monitor import collect_system_metrics
from log_parser import analyze_logs
from reporter import generate_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="infra-health-tool",
        description="A simple CLI tool that checks basic system health and scans logs for issues.",
    )

    # Output behavior
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Only generate the JSON report (do not print the summary).",
    )

    # Thresholds (ints: percent 0..100)
    parser.add_argument(
        "--cpu-warn",
        type=int,
        default=80,
        help="CPU warning threshold (percent). Default: 80",
    )
    parser.add_argument(
        "--mem-warn",
        type=int,
        default=80,
        help="Memory warning threshold (percent). Default: 80",
    )
    parser.add_argument(
        "--disk-warn",
        type=int,
        default=90,
        help="Disk warning threshold (percent). Default: 90",
    )

    # Paths
    parser.add_argument(
        "--logs-dir",
        type=str,
        default=str(Path("..") / "logs"),
        help="Directory containing log files to scan. Default: ../logs",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(Path("reports")),
        help="Directory to save generated reports. Default: reports",
    )

    return parser


def clamp_percent(name: str, value: int) -> int:
    if not (0 <= value <= 100):
        raise ValueError(f"{name} must be between 0 and 100. You gave: {value}")
    return value


def status_from_threshold(value: float, warn_threshold: int) -> str:
    return "WARN" if value >= warn_threshold else "OK"


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # Validate thresholds
    try:
        cpu_warn = clamp_percent("cpu-warn", args.cpu_warn)
        mem_warn = clamp_percent("mem-warn", args.mem_warn)
        disk_warn = clamp_percent("disk-warn", args.disk_warn)
    except ValueError as e:
        print(f"ERROR: {e}")
        return 2

    logs_dir = Path(args.logs_dir).expanduser()
    output_dir = Path(args.output_dir).expanduser()

    print("Starting infrastructure health check...")

    # 1) Collect metrics
    system_metrics = collect_system_metrics()

    cpu_percent = float(system_metrics["cpu"]["usage_percent"])
    mem_percent = float(system_metrics["memory"]["usage_percent"])
    disk_percent = float(system_metrics["disk"]["usage_percent"])

    # 2) Analyze logs
    log_analysis = analyze_logs(logs_dir)

    # Compute total matches safely (supports dict like {"ERROR": 3, "WARN": 2, ...})
    problem_counts = log_analysis.get("problem_counts", {})
    if isinstance(problem_counts, dict):
        total_problems_found = sum(int(v) for v in problem_counts.values())
    else:
        total_problems_found = 0

    # 3) Build thresholds + evaluations (these go into the JSON report)
    thresholds = {
        "cpu_warn_percent": cpu_warn,
        "memory_warn_percent": mem_warn,
        "disk_warn_percent": disk_warn,
    }

    evaluations = {
        "cpu_status": status_from_threshold(cpu_percent, cpu_warn),
        "memory_status": status_from_threshold(mem_percent, mem_warn),
        "disk_status": status_from_threshold(disk_percent, disk_warn),
        "total_log_matches": total_problems_found,
    }

    # 4) Generate report (JSON file)
    report_path = generate_report(
        system_metrics=system_metrics,
        log_analysis=log_analysis,
        output_dir=output_dir,
        thresholds=thresholds,
        evaluations=evaluations,
    )

    # 5) Print summary unless json-only
    if not args.json_only:
        print("\n=== Infrastructure Health Summary ===")
        print(f"CPU Usage: {cpu_percent:.1f}% [{evaluations['cpu_status']}]")
        print(f"Memory Usage: {mem_percent:.1f}% [{evaluations['memory_status']}]")
        print(f"Disk Usage: {disk_percent:.1f}% [{evaluations['disk_status']}]")
        print(f"Log Issues: {total_problems_found} total matches")
        print("====================================\n")

    print("Health check complete.")
    print(f"JSON report saved to: {report_path}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())