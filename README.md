# Infrastructure Health Tool

![CI](https://img.shields.io/badge/CI-passing-brightgreen)

A lightweight Python CLI tool that performs system health checks, analyzes logs, and generates structured JSON reports.

Designed for monitoring, automation, and entry-level DevOps / Python engineering workflows.

This tool is built to integrate cleanly into CI/CD pipelines to automatically validate infrastructure health on every push or deployment.

---

## 🚀 Features

- CPU, memory, and disk usage collection
- Log file analysis (keyword matching)
- Structured JSON health report generation
- Configurable warning thresholds
- Machine-friendly exit codes (CI/CD ready)
- Safe handling of missing or partial data
- Quiet and JSON-only modes for automation

---

## 📁 Project Structure

```
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
```

---

## ⚙️ Installation

Install dependencies:

```
pip install -r requirements.txt
```

---

## ▶️ Usage

Run a full health check:

```
python3 -m src.cli
```

Run with custom warning thresholds:

```
python3 -m src.cli --cpu-warn 70 --mem-warn 75 --disk-warn 85
```

Analyze logs from a directory:

```
python3 -m src.cli --logs-dir logs
```

Specify output directory:

```
python3 -m src.cli --output-dir reports
```

JSON-only output (no console summary):

```
python3 -m src.cli --json-only
```

Quiet mode:

```
python3 -m src.cli --quiet
```

---

## 📊 Sample Output

```
=== Infrastructure Health Summary ===
CPU Usage: 81.8% [WARN]
Memory Usage: 62.1% [OK]
Disk Usage: 3.3% [OK]
Log Issues: 0 total matches

Health check complete.
JSON report saved to:
reports/health_report_2026-02-02_15-08-26.json
```

---

## 🚦 Exit Codes (CI/CD Friendly)

| Code | Meaning |
|-----:|--------|
| 0 | All checks OK |
| 1 | One or more warnings |
| 2 | Error (missing or invalid data) |

---

## 🤖 Continuous Integration

This project includes GitHub Actions CI that runs on every push and pull request.

The workflow installs dependencies and executes the CLI to ensure consistent behavior and prevent regressions.

---

## 🎯 Why This Project Matters

This project demonstrates:

- Clean Python CLI design
- Defensive programming
- Automation-friendly patterns
- CI/CD integration
- Structured, machine-readable output
- Maintainable, modular code organization

Built as a portfolio project for junior Python, automation, and DevOps-oriented roles.

---

## 🧩 Relevance to Internal Engineering & CAD Tooling

Although this project focuses on infrastructure health monitoring, it mirrors the structure and patterns of internal engineering tools commonly used in large organizations, including CAD/EDA support environments.

The tool demonstrates capabilities relevant to internal tooling teams:
- CLI-based tool design for engineers
- Log parsing and pattern detection
- Structured JSON report generation for downstream tooling
- Deterministic exit codes for automation and flow control
- CI/CD integration for continuous validation
- Modular, maintainable code organization

These same patterns are commonly applied to validating design flows, analyzing CAD tool outputs, and supporting engineering productivity at scale. The domain differs, but the tooling principles remain the same.

---

## 📄 License

MIT