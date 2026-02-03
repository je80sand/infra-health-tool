🖥️ Infrastructure Health Tool
A lightweight Python CLI tool that performs system health checks, analyzes logs, and generates structured JSON reports.
Designed for monitoring, automation, and entry-level DevOps / Python engineering workflows.
🚀 Features
✅ CPU, memory, and disk usage collection
🔍 Log file analysis (keyword matching)
📄 JSON health report generation
⚠️ Configurable warning thresholds
🤖 Machine-friendly exit codes (CI/CD ready)
🧪 Safe handling of missing or partial data
📦 Project Structure
Copy code

infra-health-tool/
├── src/
│ ├── cli.py # CLI entry point
│ ├── monitor.py # System metrics collection
│ ├── log_parser.py # Log analysis
│ ├── reporter.py # JSON report generation
│ └── __init__.py
├── reports/ # Generated health reports
├── logs/ # Optional log input directory
├── requirements.txt
└── README.md
🛠️ Installation
Copy code
Bash
pip install -r requirements.txt
▶️ Usage
Run full health check
Copy code
Bash
python3 -m src.cli
JSON only (no console output)
Copy code
Bash
python3 -m src.cli --json-only
Custom warning thresholds
Copy code
Bash
python3 -m src.cli \
  --cpu-warn 70 \
  --mem-warn 75 \
  --disk-warn 85
Analyze logs from a directory
Copy code
Bash
python3 -m src.cli --logs-dir ./logs
Custom output directory
Copy code
Bash
python3 -m src.cli --output-dir reports
📊 Sample Output
Copy code

=== Infrastructure Health Summary ===
CPU Usage: 81.8% [WARN]
Memory Usage: 62.1% [OK]
Disk Usage: 3.3% [OK]
Log Issues: 0 total matches
===================================

Health check complete.
JSON report saved to: reports/health_report_2026-02-02_15-08-26.json
🔢 Exit Codes
Code
Meaning
0
All systems OK
1
One or more WARN conditions
2
Error or missing metric data
Example:
Copy code
Bash
python3 -m src.cli
echo $?
📄 JSON Report
Reports are saved to the reports/ directory and include:
Timestamp
System metadata
CPU, memory, disk usage
Log issue counts
Evaluation status