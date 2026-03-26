"""
reporter.py

Saves infrastructure health reports to disk.

Supports:
- JSON report
- Markdown report
"""

import json
import os
from datetime import datetime

from ai_analyzer import generate_ai_analysis


def ensure_reports_folder():
    os.makedirs("reports", exist_ok=True)


def build_report_data(target, packets_sent, packets_received, packet_loss_percent, average_latency_ms):
    report_data = {
        "target": target,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "packets_sent": packets_sent,
        "packets_received": packets_received,
        "packet_loss_percent": packet_loss_percent,
        "average_latency_ms": average_latency_ms,
    }

    report_data["ai_analysis"] = generate_ai_analysis(report_data)

    return report_data


def save_json_report(report_data, filename="reports/health_report.json"):
    ensure_reports_folder()

    with open(filename, "w") as file:
        json.dump(report_data, file, indent=4)

    print(f"JSON report saved to {filename}")


def save_markdown_report(report_data, filename="reports/health_report.md"):
    ensure_reports_folder()

    ai_analysis = report_data.get("ai_analysis", {})
    findings = ai_analysis.get("findings", [])
    causes = ai_analysis.get("possible_causes", [])
    recommendations = ai_analysis.get("recommendations", [])

    with open(filename, "w") as file:
        file.write("# Infrastructure Health Report\n\n")
        file.write(f"**Target:** {report_data['target']}\n\n")
        file.write(f"**Timestamp:** {report_data['timestamp']}\n\n")
        file.write(f"**Packets Sent:** {report_data['packets_sent']}\n\n")
        file.write(f"**Packets Received:** {report_data['packets_received']}\n\n")
        file.write(f"**Packet Loss:** {report_data['packet_loss_percent']}%\n\n")
        file.write(f"**Average Latency:** {report_data['average_latency_ms']} ms\n\n")

        file.write("## AI Summary\n\n")
        file.write(f"{ai_analysis.get('summary', 'No AI summary available.')}\n\n")

        file.write("## Findings\n\n")
        for item in findings:
            file.write(f"- {item}\n")
        file.write("\n")

        file.write("## Possible Causes\n\n")
        for item in causes:
            file.write(f"- {item}\n")
        file.write("\n")

        file.write("## Recommendations\n\n")
        for item in recommendations:
            file.write(f"- {item}\n")
        file.write("\n")

    print(f"Markdown report saved to {filename}")


def save_all_reports(target, packets_sent, packets_received, packet_loss_percent, average_latency_ms):
    report_data = build_report_data(
        target,
        packets_sent,
        packets_received,
        packet_loss_percent,
        average_latency_ms,
    )

    save_json_report(report_data)
    save_markdown_report(report_data)

    return report_data