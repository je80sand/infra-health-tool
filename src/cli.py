"""
cli.py

Entry point for the Infra Health Tool.

Features included:
- CLI flags (json-only, summary-only, no-save)
- Markdown export (--export-md)
- Simulation mode (--simulate ok|warn|critical)
- Threshold controls (--cpu-warn, etc.)
"""

import argparse

from monitor import collect_system_metrics
from log_parser import analyze_logs
from reporter import save_json_report, save_markdown_report


def evaluate_usage(value, warn_threshold, critical_threshold):
    """
    Convert a numeric percentage into a human label: OK / WARN / CRITICAL
    """
    if value >= critical_threshold:
        return "CRITICAL"
    if value >= warn_threshold:
        return "WARN"
    return "OK"


def apply_simulation(system_metrics, mode):
    """
    Override real metrics with demo values.
    This keeps the rest of the program identical (clean design).
    """
    if mode == "ok":
        system_metrics["cpu"]["usage_percent"] = 10.0
        system_metrics["memory"]["usage_percent"] = 45.0
        system_metrics["disk"]["usage_percent"] = 30.0

    elif mode == "warn":
        system_metrics["cpu"]["usage_percent"] = 75.0
        system_metrics["memory"]["usage_percent"] = 78.0
        system_metrics["disk"]["usage_percent"] = 85.0

    elif mode == "critical":
        system_metrics["cpu"]["usage_percent"] = 95.0
        system_metrics["memory"]["usage_percent"] = 94.0
        system_metrics["disk"]["usage_percent"] = 98.0

    return system_metrics


def build_parser():
    parser = argparse.ArgumentParser(
        description="Infra Health Tool - collect system metrics + scan logs + output report."
    )

    # --- OUTPUT OPTIONS ---
    parser.add_argument("--summary-only", action="store_true",
                        help="Print the summary and exit (still saves unless --no-save).")

    parser.add_argument("--json-only", action="store_true",
                        help="Do not print the summary (only save report and print paths).")

    parser.add_argument("--export-md", action="store_true",
                        help="Also export a Markdown report into the reports/ folder.")

    parser.add_argument("--no-save", action="store_true",
                        help="Do not save a report file (quick check).")

    # --- THRESHOLDS ---
    parser.add_argument("--cpu-warn", type=float, default=70, help="CPU WARN threshold percent.")
    parser.add_argument("--cpu-critical", type=float, default=90, help="CPU CRITICAL threshold percent.")

    parser.add_argument("--mem-warn", type=float, default=70, help="Memory WARN threshold percent.")
    parser.add_argument("--mem-critical", type=float, default=90, help="Memory CRITICAL threshold percent.")

    parser.add_argument("--disk-warn", type=float, default=80, help="Disk WARN threshold percent.")
    parser.add_argument("--disk-critical", type=float, default=95, help="Disk CRITICAL threshold percent.")

    # --- LOGS ---
    parser.add_argument("--logs-dir", default="logs", help="Folder to scan for logs (default: logs).")

    # --- SIMULATION ---
    parser.add_argument("--simulate", choices=["ok", "warn", "critical"],
                        help="Simulate system metrics for demo purposes.")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # 1) Collect real metrics
    system_metrics = collect_system_metrics()

    # 2) Optional simulation override
    if args.simulate:
        system_metrics = apply_simulation(system_metrics, args.simulate)

    # 3) Analyze logs
    log_analysis = analyze_logs(logs_dir=args.logs_dir)

    # 4) Build full report
    full_report = {
        "system_metrics": system_metrics,
        "log_analysis": log_analysis,
    }

    # 5) Pull values we need for summary
    cpu_percent = system_metrics["cpu"]["usage_percent"]
    memory_percent = system_metrics["memory"]["usage_percent"]
    disk_percent = system_metrics["disk"]["usage_percent"]

    # 6) Calculate log totals BEFORE printing (fixes your error)
    problem_counts = log_analysis["problem_counts"]
    total_problems_found = sum(problem_counts.values())

    # 7) Evaluate health status using CLI thresholds
    cpu_status = evaluate_usage(cpu_percent, args.cpu_warn, args.cpu_critical)
    memory_status = evaluate_usage(memory_percent, args.mem_warn, args.mem_critical)
    disk_status = evaluate_usage(disk_percent, args.disk_warn, args.disk_critical)

    # 8) Print summary (unless json-only)
    if not args.json_only:
        print("\n--- Infrastructure Health Summary ---")
        print(f"CPU Usage: {cpu_percent}% [{cpu_status}]")
        print(f"Memory Usage: {memory_percent}% [{memory_status}]")
        print(f"Disk Usage: {disk_percent}% [{disk_status}]")
        print(f"Log Issues: {total_problems_found} total matches")
        print("------------------------------------\n")

    # If user wants summary-only, we still continue to save unless no-save is set.
    # (You can change this behavior later; this is a good default.)

    # 9) Save JSON + optional Markdown
    json_path = None
    md_path = None

    if not args.no_save:
        json_path = save_json_report(full_report)

        if args.export_md:
            md_path = save_markdown_report(full_report)

    # 10) Output final info (even for json-only)
    print("Health check complete.")

    if args.no_save:
        print("No files saved (--no-save).")
    else:
        if json_path:
            print(f"JSON report saved to: {json_path}")
        if md_path:
            print(f"Markdown report saved to: {md_path}")


if __name__ == "__main__":
    main()