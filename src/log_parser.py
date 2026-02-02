"""
log_parser.py

Scans log files for common problem patterns and counts occurrences.

Designed to be easy to understand:
- Look in a folder
- Read text files
- Count matches for each keyword

No hidden magic.
"""

import os


DEFAULT_PATTERNS = [
    "ERROR",
    "WARNING",
    "WARN",
    "FAILED",
    "TIMEOUT",
    "EXCEPTION",
]


def analyze_logs(logs_dir="logs", patterns=None):
    """
    Analyze log files in `logs_dir` and count pattern occurrences.

    Returns:
    {
      "logs_dir": "logs",
      "files_scanned": 2,
      "problem_counts": {"ERROR": 1, "WARNING": 3, ...},
      "examples": {
          "ERROR": ["...first matching line...", "..."],
          ...
      }
    }
    """
    if patterns is None:
        patterns = DEFAULT_PATTERNS

    result = {
        "logs_dir": logs_dir,
        "files_scanned": 0,
        "problem_counts": {p: 0 for p in patterns},
        "examples": {p: [] for p in patterns},
    }

    # If the folder doesn't exist, just return zeros (not an error).
    if not os.path.isdir(logs_dir):
        return result

    for filename in os.listdir(logs_dir):
        path = os.path.join(logs_dir, filename)

        # Only scan regular files
        if not os.path.isfile(path):
            continue

        result["files_scanned"] += 1

        # Read file safely
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line_stripped = line.strip()

                    for p in patterns:
                        if p in line_stripped:
                            result["problem_counts"][p] += 1

                            # Store a few example lines (so report feels real)
                            if len(result["examples"][p]) < 3:
                                result["examples"][p].append(line_stripped)

        except Exception:
            # If a file can't be read for some reason, skip it.
            continue

    return result