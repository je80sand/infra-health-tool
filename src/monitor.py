"""
monitor.py

Collects basic system health metrics (CPU, memory, disk, OS info).
Think of this as your "system checkup" module.

Nothing fancy.
Just clear, readable Python.
"""

import platform
from datetime import datetime

import psutil


def collect_system_metrics():
    """
    Collect system metrics and return them in a clean dictionary.

    Returns a dict like:
    {
      "timestamp": "...",
      "system": {"os": "...", "hostname": "..."},
      "cpu": {"usage_percent": 12.3, "cores_logical": 8},
      "memory": {"usage_percent": 45.0, "total_gb": 16.0},
      "disk": {"usage_percent": 60.2, "total_gb": 512.0}
    }
    """

    timestamp = datetime.now().isoformat(timespec="seconds")

    # --- CPU ---
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_logical_cores = psutil.cpu_count(logical=True)

    # --- MEMORY ---
    mem = psutil.virtual_memory()
    mem_percent = mem.percent
    mem_total_gb = round(mem.total / (1024 ** 3), 2)

    # --- DISK (root) ---
    disk = psutil.disk_usage("/")
    disk_percent = disk.percent
    disk_total_gb = round(disk.total / (1024 ** 3), 2)

    # --- SYSTEM ---
    system_info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "hostname": platform.node(),
    }

    return {
        "timestamp": timestamp,
        "system": system_info,
        "cpu": {
            "usage_percent": cpu_percent,
            "cores_logical": cpu_logical_cores,
        },
        "memory": {
            "usage_percent": mem_percent,
            "total_gb": mem_total_gb,
        },
        "disk": {
            "usage_percent": disk_percent,
            "total_gb": disk_total_gb,
        },
    }