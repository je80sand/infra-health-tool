# 🚀 Infrastructure Health Tool

![CI](https://github.com/je80sand/infra-health-tool/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tests](https://img.shields.io/badge/tests-pytest-green)
![License](https://img.shields.io/badge/license-MIT-green)

A lightweight Python CLI tool that performs system health checks, analyzes logs, and generates structured JSON reports.

Designed for monitoring, automation, and entry-level DevOps / QA / Python engineering workflows.

Built to integrate seamlessly into CI/CD pipelines to validate infrastructure health on every push or deployment.

---

## 🎥 Demo

Run:
python3 -m src.cli

Output:
=== Infrastructure Health Summary ===
CPU Usage: 81.8% [WARN]
Memory Usage: 62.1% [OK]
Disk Usage: 3.3% [OK]
Log Issues: 0 total matches

Health check complete.
JSON report saved to:
reports/health_report_2026-02-02_15-08-26.json

---

## 📸 Example JSON Output

{
  "cpu_percent": 81.8,
  "memory_percent": 62.1,
  "disk_percent": 3.3,
  "cpu_status": "WARN",
  "memory_status": "OK",
  "disk_status": "OK",
  "log_issues": 0,
  "timestamp": "2026-02-02T15:08:26"
}

---

## 🚀 Features

- CPU, memory, and disk usage collection
- Log file analysis (keyword matching)
- Structured JSON health report generation
- Configurable warning thresholds
- Machine-friendly exit codes (CI/CD ready)
- Safe handling of missing or partial data
- Quiet and JSON-only modes for automation---

## 🤖 AI-Powered Diagnostics

This tool includes a built-in AI-style analysis engine that converts raw system and network data into human-readable insights.

Instead of just showing metrics, the tool explains:

- System health status (excellent, good, unstable, critical)
- Network issues such as packet loss and high latency
- Likely causes (e.g., Wi-Fi instability, ISP issues, congestion)
- Actionable recommendations for troubleshooting

### Example AI Output

Connectivity to google.com is unstable with an 80.0% success rate.  
Moderate packet loss detected at 20%.  
Average latency is elevated at 85 ms.

Possible causes:
- Wi-Fi signal issues or interference  
- ISP instability  
- Network congestion  

Recommendations:
- Run the test at different times  
- Compare Wi-Fi vs Ethernet  
- Reboot router and retest  

---

This feature demonstrates how structured data can be transformed into meaningful insights, simulating real-world AI-assisted diagnostics used in production systems.


---

## 📁 Project Structure

infra-health-tool/
├── .github/
│ └── workflows/
│ └── ci.yml
├── logs/
│ └── sample.log
├── reports/
├── src/
│ ├── cli.py
│ ├── monitor.py
│ ├── log_parser.py
│ ├── reporter.py
│ ├── ai_analyzer.py
│ └── __init__.py
├── tests/
├── .gitignore
├── requirements.txt
└── README.md

---

## ⚙️ Installation

pip install -r requirements.txt

---

## ▶️ Usage

Run full health check:
python3 -m src.cli

Run with custom warning thresholds:
python3 -m src.cli --cpu-warn 70 --mem-warn 75 --disk-warn 85

Analyze logs from a directory:
python3 -m src.cli --logs-dir logs

Specify output directory:
python3 -m src.cli --output-dir reports

JSON-only output:
python3 -m src.cli --json-only

Quiet mode:
python3 -m src.cli --quiet

---

## 🧪 Testing

pytest tests/

---

## 📊 Exit Codes (CI/CD Friendly)

0 = All checks OK  
1 = One or more warnings  
2 = Error (missing or invalid data)

---

## 🔄 Continuous Integration

This project includes GitHub Actions CI that runs on every push and pull request.

The workflow:
- Installs dependencies
- Runs tests
- Executes the CLI

This ensures consistent behavior and prevents regressions.

---

## 🧠 AI Log Analysis (Optional Feature)

The ai_analyzer.py module is designed to extend log analysis capabilities.

Potential use cases:
- Detect anomaly patterns in logs
- Identify recurring system issues
- Enhance monitoring with intelligent insights

---

## 🎯 Why This Project Matters

- Clean Python CLI design
- Defensive programming
- Automation-friendly patterns
- CI/CD integration
- Structured, machine-readable output
- Maintainable, modular code organization

---

## 🏗️ Relevance to Internal Engineering & CAD Tooling

Although focused on infrastructure health monitoring, this project mirrors patterns used in internal engineering tools at large companies.

- CLI-based tooling for engineers
- Log parsing and pattern detection
- Structured JSON output for downstream systems
- Deterministic exit codes for automation workflows
- CI/CD validation pipelines
- Modular, scalable architecture

---

## 📄 License

MIT