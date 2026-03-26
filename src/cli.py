"""
cli.py

Entry point for the Infrastructure Health Tool.

Runs:
- system metrics collection
- log parsing
- JSON / Markdown report generation
- simple terminal summary

Run with:
    python3 -m src.cli
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, Optional

from .log_parser import analyze_logs
from .monitor import collect_system_metrics
from .reporter import save_all_reports


def safe_float(value: Any) -> Optional[float]:
    """Try to convert a value to float. Return None if it fails."""
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def get_usage_percent(system_metrics: Dict[str, Any], section: str) -> Optional[float]:
    """
    Get usage percent from nested metric sections like:
    system_metrics["cpu"]["usage_percent"]
    """
    block = system_metrics.get(section)

    if not isinstance(block, dict):
        return None

    return safe_float(block.get("usage_percent"))


def format_percent(percent: Optional[float]) -> str:
    """Format a percentage nicely."""
    if percent is None:
        return "N/A"
    return f"{percent:.1f}%"


def get_status(percent: Optional[float], warn_threshold: float) -> str:
    """Return OK, WARN, or N/A based on the value."""
    if percent is None:
        return "N/A"

    if percent >= warn_threshold:
        return "WARN"

    return "OK"


def get_total_matches(log_analysis: Dict[str, Any]) -> int:
    """Safely get total matches from log analysis."""
    if not isinstance(log_analysis, dict):
        return 0

    if isinstance(log_analysis.get("total_matches"), int):
        return int(log_analysis["total_matches"])

    if isinstance(log_analysis.get("total_problems_found"), int):
        return int(log_analysis["total_problems_found"])

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="infra-health-tool",
        description="Infrastructure Health Tool: metrics + log scan + report generation",
    )

    parser.add_argument("--json-only", action="store_true", help="Only print JSON report location")
    parser.add_argument("--quiet", action="store_true", help="Reduce terminal output")

    parser.add_argument("--cpu-warn", type=float, default=80.0, help="CPU warning threshold")
    parser.add_argument("--mem-warn", type=float, default=80.0, help="Memory warning threshold")
    parser.add_argument("--disk-warn", type=float, default=90.0, help="Disk warning threshold")

    parser.add_argument("--logs-dir", type=str, default="logs", help="Directory containing logs")
    parser.add_argument("--output-dir", type=str, default="reports", help="Output directory")

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logs_dir = Path(args.logs_dir)
    output_dir = Path(args.output_dir)

    if not args.quiet:
        print("Starting infrastructure health check...")

    # 1) Collect system metrics
    system_metrics = collect_system_metrics()

    # 2) Parse logs safely
    try:
        log_analysis = analyze_logs(logs_dir)
    except Exception:
        log_analysis = {"total_matches": 0}

    # 3) Pull out nested usage percentages
    cpu_percent = get_usage_percent(system_metrics, "cpu")
    mem_percent = get_usage_percent(system_metrics, "memory")
    disk_percent = get_usage_percent(system_metrics, "disk")

    evaluations = {
        "cpu_status": get_status(cpu_percent, float(args.cpu_warn)),
        "memory_status": get_status(mem_percent, float(args.mem_warn)),
        "disk_status": get_status(disk_percent, float(args.disk_warn)),
    }

    total_matches = get_total_matches(log_analysis)

    # 4) Build simple network-style values for the current reporter
    packets_sent = 10
    packets_received = max(0, packets_sent - min(total_matches, packets_sent))
    packet_loss_percent = ((packets_sent - packets_received) / packets_sent) * 100

    if cpu_percent is None and mem_percent is None and disk_percent is None:
        average_latency_ms = 0
    else:
        numbers = [value for value in [cpu_percent, mem_percent, disk_percent] if value is not None]
        average_latency_ms = round(sum(numbers) / len(numbers), 2)

    target = system_metrics.get("system", {}).get("hostname", "localhost")

    # 5) Save reports
    save_all_reports(
        target=target,
        packets_sent=packets_sent,
        packets_received=packets_received,
        packet_loss_percent=packet_loss_percent,
        average_latency_ms=average_latency_ms,
    )

    json_report_path = output_dir / "health_report.json"

    # 6) Output
    if args.json_only:
        if not args.quiet:
            print(f"JSON report saved to: {json_report_path}")
        return 0

    if not args.quiet:
        print("\n=== Infrastructure Health Summary ===")
        print(f"CPU Usage: {format_percent(cpu_percent)} [{evaluations['cpu_status']}]")
        print(f"Memory Usage: {format_percent(mem_percent)} [{evaluations['memory_status']}]")
        print(f"Disk Usage: {format_percent(disk_percent)} [{evaluations['disk_status']}]")
        print(f"Log Issues: {total_matches} total matches")
        print("Health check complete.")
        print(f"JSON report saved to: {json_report_path}")

    # 7) Exit code rules
    # 0 = OK
    # 1 = warning
    # 2 = error / missing metrics
    if cpu_percent is None and mem_percent is None and disk_percent is None:
        return 2

    if (
        evaluations["cpu_status"] == "WARN"
        or evaluations["memory_status"] == "WARN"
        or evaluations["disk_status"] == "WARN"
    ):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())