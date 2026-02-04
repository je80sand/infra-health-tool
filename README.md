![CI](https://github.com/je80sand/infra-health-tool/actions/workflows/ci.yml/badge.svg)


# Infrastructure Health Tool

A lightweight Python CLI tool that performs system health checks, analyzes logs, and generates structured JSON reports.

Designed for monitoring, automation, and entry-level DevOps / Python engineering workflows.

---

## 🚀 Features

- CPU, memory, and disk usage collection
- Log file analysis (keyword matching)
- JSON health report generation
- Configurable warning thresholds
- Machine-friendly exit codes (CI/CD ready)
- Safe handling of missing or partial data

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
│ └── __init__.py
├── .gitignore
├── requirements.txt
└── README.md

---

## ⚙️ Installation

pip install -r requirements.txt

---

## ▶️ Usage

Run a full health check:

python3 -m src.cli

Run with custom warning thresholds:

python3 -m src.cli --cpu-warn 70 --mem-warn 75 --disk-warn 85

Analyze logs from a directory:

python3 -m src.cli --logs-dir logs

Specify output directory:

python3 -m src.cli --output-dir reports

JSON-only output (no console summary):

python3 -m src.cli --json-only

Quiet mode:

python3 -m src.cli --quiet

---

## 📊 Sample Output

=== Infrastructure Health Summary ===
CPU Usage: 81.8% [WARN]
Memory Usage: 62.1% [OK]
Disk Usage: 3.3% [OK]
Log Issues: 0 total matches
====================================

Health check complete.
JSON report saved to: reports/health_report_2026-02-02_15-08-26.json

---

## 🧾 Exit Codes (CI/CD Friendly)

0 = All checks OK  
1 = One or more warnings  
2 = Error (missing or invalid data)

---

## 🤖 Continuous Integration

This project includes GitHub Actions CI that runs on every push and pull request, installs dependencies, and executes the CLI.

---

## 🎯 Why This Project Matters

This project demonstrates clean Python CLI design, defensive programming, automation patterns, CI/CD integration, and DevOps-friendly exit codes.

Built as a portfolio project for junior Python, automation, and DevOps roles.

---

## 📜 License

MIT