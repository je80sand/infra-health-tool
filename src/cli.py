"""
cli.py

Entry point for the Infrastructure Health Tool.

Runs:
- System metrics collection (CPU, memory, disk, OS info)
- Log parsing (keyword matches)
- JSON report generation (saved to reports/ by default)

Usage examples:
  python3 -m src.cli
  python3 -m src.cli --json-only
  python3 -m src.cli --cpu-warn 70 --mem-warn 75 --disk-warn 85
  python3 -m src.cli --logs-dir ./logs --output-dir reports
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, Optional

# IMPORTANT:
# Use relative imports so this works with: python3 -m src.cli
from .monitor import collect_system_metrics
from .log_parser import analyze_logs
from .reporter import generate_report


def _as_float(value: Any) -> Optional[float]:
    """Best-effort conversion to float; returns None if not possible."""
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _get_usage_percent(system_metrics: Dict[str, Any], section: str) -> Optional[float]:
    """
    Your monitor returns nested dicts like:
      { "cpu": {"usage_percent": 66.2, ...}, "memory": {"usage_percent": 62.6, ...}, ... }
    This safely extracts that usage_percent.
    """
    block = system_metrics.get(section)
    if not isinstance(block, dict):
        return None
    return _as_float(block.get("usage_percent"))


def _status(percent: Optional[float], warn_threshold: float) -> str:
    """
    If percent is missing, return N/A.
    Otherwise OK if percent < threshold, else WARN.
    """
    if percent is None:
        return "N/A"
    return "OK" if percent < warn_threshold else "WARN"


def _fmt_percent(percent: Optional[float]) -> str:
    """Format percent nicely, or N/A."""
    if percent is None:
        return "N/A"
    return f"{percent:.1f}%"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="infra-health-tool",
        description="Infrastructure Health Tool: metrics + log scan + JSON report",
    )

    parser.add_argument("--json-only", action="store_true", help="Only output JSON report path (no summary).")
    parser.add_argument("--quiet", action="store_true", help="Suppress non-essential output.")

    parser.add_argument("--cpu-warn", type=float, default=80.0, help="CPU usage warning threshold percent. Default: 80")
    parser.add_argument("--mem-warn", type=float, default=80.0, help="Memory usage warning threshold percent. Default: 80")
    parser.add_argument("--disk-warn", type=float, default=90.0, help="Disk usage warning threshold percent. Default: 90")

    parser.add_argument("--logs-dir", type=str, default="logs", help="Directory containing logs to scan. Default: logs")
    parser.add_argument("--output-dir", type=str, default="reports", help="Directory to save JSON reports. Default: reports")

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logs_dir = Path(args.logs_dir)
    output_dir = Path(args.output_dir)

    if not args.quiet:
        print("Starting infrastructure health check...")

    # 1) Collect metrics
    system_metrics: Dict[str, Any] = collect_system_metrics()

    # Extract the nested usage percents (THIS is the fix for your N/A)
    cpu_percent = _get_usage_percent(system_metrics, "cpu")
    mem_percent = _get_usage_percent(system_metrics, "memory")
    disk_percent = _get_usage_percent(system_metrics, "disk")

    # 2) Analyze logs
    log_analysis: Dict[str, Any] = analyze_logs(logs_dir)

    # total matches can be stored in different ways depending on your log_parser;
    # we handle common cases safely.
    total_matches = 0
    if isinstance(log_analysis, dict):
        if isinstance(log_analysis.get("total_matches"), int):
            total_matches = int(log_analysis["total_matches"])
        elif isinstance(log_analysis.get("total_problems_found"), int):
            total_matches = int(log_analysis["total_problems_found"])

    # 3) Evaluate statuses
    evaluations = {
        "cpu_status": _status(cpu_percent, args.cpu_warn),
        "memory_status": _status(mem_percent, args.mem_warn),
        "disk_status": _status(disk_percent, args.disk_warn),
    }

    thresholds = {
        "cpu_warn": float(args.cpu_warn),
        "mem_warn": float(args.mem_warn),
        "disk_warn": float(args.disk_warn),
    }

    # 4) Generate report JSON
    report_path = generate_report(
        system_metrics=system_metrics,
        log_analysis=log_analysis,
        thresholds=thresholds,
        evaluations=evaluations,
        output_dir=output_dir,
    )

    # 5) Output
    if args.json_only:
        # Machine-readable behavior
        if not args.quiet:
            print(f"JSON report saved to: {report_path}")
        return 0

    if not args.quiet:
        print("\n=== Infrastructure Health Summary ===")
        print(f"CPU Usage: {_fmt_percent(cpu_percent)} [{evaluations['cpu_status']}]")
        print(f"Memory Usage: {_fmt_percent(mem_percent)} [{evaluations['memory_status']}]")
        print(f"Disk Usage: {_fmt_percent(disk_percent)} [{evaluations['disk_status']}]")
        print(f"Log Issues: {total_matches} total matches")
        print("====================================\n")
        print("Health check complete.")
        print(f"JSON report saved to: {report_path}")

    # ----------------------------
    # Exit code rules:
    # 0 = all OK
    # 1 = any WARN
    # 2 = ERROR (missing data / exception)
    # ----------------------------

    exit_code = 0

    # If any metric is missing (None), treat as ERROR
    if cpu_percent is None or mem_percent is None or disk_percent is None:
        exit_code = 2
    else:
        # If any evaluation is WARN, exit 1
        if (
            evaluations.get("cpu_status") == "WARN"
            or evaluations.get("mem_status") == "WARN"
            or evaluations.get("disk_status") == "WARN"
        ):
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())