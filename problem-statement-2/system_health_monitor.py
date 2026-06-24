"""
System Health Monitoring Script (Problem Statement 2 - Objective 1)

Monitors the health of a system by checking:
  - CPU usage
  - Memory usage
  - Disk space usage
  - Top running processes

If any metric exceeds a predefined threshold, the script logs an ALERT
to both the console and a log file.

Usage:
    python system_health_monitor.py

Configuration:
    Edit the THRESHOLDS dictionary below to adjust alert levels.
"""

import psutil
import logging
import os
import sys
from datetime import datetime


# ── Configuration ───────────────────────────────────────────────────────

THRESHOLDS = {
    "cpu_percent": 80.0,       # Alert if CPU usage > 80%
    "memory_percent": 80.0,    # Alert if memory usage > 80%
    "disk_percent": 80.0,      # Alert if disk usage > 80%
}

# Log file path (inside the project logs/ folder)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
LOG_FILE = os.path.join(LOG_DIR, "system_health.log")


# ── Logging Setup ──────────────────────────────────────────────────────

def setup_logging():
    """Configure logging to write to both console and a log file."""
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("SystemHealthMonitor")
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# ── Health Check Functions ──────────────────────────────────────────────

def check_cpu(logger):
    """Check CPU usage and log an alert if it exceeds the threshold."""
    cpu_usage = psutil.cpu_percent(interval=1)
    threshold = THRESHOLDS["cpu_percent"]

    logger.info(f"CPU Usage: {cpu_usage}% (Threshold: {threshold}%)")

    if cpu_usage > threshold:
        logger.warning(
            f"[ALERT] CPU usage is {cpu_usage}% - exceeds threshold of {threshold}%!"
        )
    return cpu_usage


def check_memory(logger):
    """Check memory usage and log an alert if it exceeds the threshold."""
    memory = psutil.virtual_memory()
    mem_usage = memory.percent
    threshold = THRESHOLDS["memory_percent"]

    logger.info(
        f"Memory Usage: {mem_usage}% "
        f"(Used: {memory.used / (1024**3):.2f} GB / "
        f"Total: {memory.total / (1024**3):.2f} GB)"
    )

    if mem_usage > threshold:
        logger.warning(
            f"[ALERT] Memory usage is {mem_usage}% - exceeds threshold of {threshold}%!"
        )
    return mem_usage


def check_disk(logger):
    """Check disk usage for all partitions and alert if any exceed the threshold."""
    threshold = THRESHOLDS["disk_percent"]
    results = []

    partitions = psutil.disk_partitions(all=False)
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_pct = usage.percent

            logger.info(
                f"Disk [{partition.device}] Usage: {disk_pct}% "
                f"(Used: {usage.used / (1024**3):.2f} GB / "
                f"Total: {usage.total / (1024**3):.2f} GB)"
            )

            if disk_pct > threshold:
                logger.warning(
                    f"[ALERT] Disk [{partition.device}] usage is {disk_pct}% "
                    f"- exceeds threshold of {threshold}%!"
                )
            results.append((partition.device, disk_pct))
        except PermissionError:
            logger.error(f"Permission denied for partition: {partition.device}")
        except Exception as e:
            logger.error(f"Error checking partition {partition.device}: {e}")

    return results


def check_running_processes(logger, top_n=5):
    """Log the top N processes by CPU usage."""
    logger.info(f"Top {top_n} Processes by CPU Usage:")
    logger.info(f"{'PID':<10} {'Name':<30} {'CPU%':<10} {'Memory%':<10}")
    logger.info("-" * 60)

    processes = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Sort by CPU usage descending
    processes.sort(key=lambda p: p.get("cpu_percent", 0) or 0, reverse=True)

    for proc in processes[:top_n]:
        pid = proc.get("pid", "N/A")
        name = proc.get("name", "Unknown")[:28]
        cpu = proc.get("cpu_percent", 0) or 0
        mem = proc.get("memory_percent", 0) or 0
        logger.info(f"{pid:<10} {name:<30} {cpu:<10.1f} {mem:<10.1f}")

    return processes[:top_n]


# ── Main ────────────────────────────────────────────────────────────────

def main():
    """Run all system health checks and log results."""
    logger = setup_logging()

    logger.info("=" * 60)
    logger.info(f"System Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    check_cpu(logger)
    logger.info("-" * 60)

    check_memory(logger)
    logger.info("-" * 60)

    check_disk(logger)
    logger.info("-" * 60)

    check_running_processes(logger)

    logger.info("=" * 60)
    logger.info("Health check complete.")
    logger.info(f"Log saved to: {LOG_FILE}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
