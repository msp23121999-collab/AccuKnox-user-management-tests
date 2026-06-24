"""
Application Health Checker (Problem Statement 2 - Objective 4)

Checks the uptime and health of one or more web applications by sending
HTTP requests and evaluating the response status codes.

Status Logic:
  - 2xx → Application is UP (functioning correctly)
  - 3xx → Application is UP (redirect, but reachable)
  - 4xx → Application is DOWN (client error — e.g., 404 Not Found)
  - 5xx → Application is DOWN (server error — e.g., 500 Internal Server Error)
  - Timeout / Connection Error → Application is DOWN (unreachable)

Usage:
    python app_health_checker.py

    You can also pass URLs as command-line arguments:
    python app_health_checker.py https://example.com https://httpstat.us/500

Configuration:
    Edit the DEFAULT_URLS list below to check different applications.
"""

import requests
import logging
import os
import sys
from datetime import datetime


# ── Configuration ───────────────────────────────────────────────────────

# Default list of URLs to check (used when no command-line args are given)
DEFAULT_URLS = [
    "https://opensource-demo.orangehrmlive.com",
    "https://www.google.com",
    "https://www.github.com",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://thiswebsitedoesnotexist12345.com",
]

# Timeout for each request (in seconds)
REQUEST_TIMEOUT = 10

# Log file path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app_health.log")


# ── Logging Setup ──────────────────────────────────────────────────────

def setup_logging():
    """Configure logging to write to both console and a log file."""
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("AppHealthChecker")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# ── Health Check Function ──────────────────────────────────────────────

def check_application_health(url, logger):
    """
    Send an HTTP GET request to the given URL and determine if the
    application is UP or DOWN based on the status code.

    Returns:
        dict with keys: url, status, status_code, response_time_ms, details
    """
    result = {
        "url": url,
        "status": "DOWN",
        "status_code": None,
        "response_time_ms": None,
        "details": "",
    }

    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
            headers={"User-Agent": "AccuKnox-HealthChecker/1.0"}
        )

        status_code = response.status_code
        response_time = response.elapsed.total_seconds() * 1000  # Convert to ms
        result["status_code"] = status_code
        result["response_time_ms"] = round(response_time, 2)

        if 200 <= status_code < 400:
            result["status"] = "UP"
            result["details"] = f"HTTP {status_code} - Application is functioning correctly."
            logger.info(
                f"[UP]   | {url} | HTTP {status_code} | "
                f"Response: {result['response_time_ms']}ms"
            )
        else:
            result["status"] = "DOWN"
            result["details"] = f"HTTP {status_code} - Application returned an error."
            logger.warning(
                f"[DOWN] | {url} | HTTP {status_code} | "
                f"Response: {result['response_time_ms']}ms"
            )

    except requests.exceptions.ConnectionError:
        result["details"] = "Connection Error - Application is unreachable."
        logger.error(f"[DOWN] | {url} | Connection Error - unreachable")

    except requests.exceptions.Timeout:
        result["details"] = f"Timeout - No response within {REQUEST_TIMEOUT} seconds."
        logger.error(f"[DOWN] | {url} | Timeout after {REQUEST_TIMEOUT}s")

    except requests.exceptions.RequestException as e:
        result["details"] = f"Request Error - {str(e)}"
        logger.error(f"[DOWN] | {url} | Error: {e}")

    return result


# ── Report Generator ───────────────────────────────────────────────────

def generate_report(results, logger):
    """Print a formatted summary report of all health check results."""
    logger.info("")
    logger.info("=" * 80)
    logger.info("APPLICATION HEALTH CHECK REPORT")
    logger.info("=" * 80)
    logger.info(
        f"{'URL':<50} {'Status':<8} {'Code':<6} {'Response (ms)':<15}"
    )
    logger.info("-" * 80)

    up_count = 0
    down_count = 0

    for r in results:
        code = str(r["status_code"]) if r["status_code"] else "N/A"
        resp = str(r["response_time_ms"]) if r["response_time_ms"] else "N/A"
        url_display = r["url"][:48]
        logger.info(
            f"{url_display:<50} {r['status']:<8} {code:<6} {resp:<15}"
        )

        if r["status"] == "UP":
            up_count += 1
        else:
            down_count += 1

    logger.info("-" * 80)
    logger.info(f"Total: {len(results)} | UP: {up_count} | DOWN: {down_count}")
    logger.info("=" * 80)


# ── Main ────────────────────────────────────────────────────────────────

def main():
    """Run health checks on all configured URLs and generate a report."""
    logger = setup_logging()

    # Use command-line args if provided, otherwise use DEFAULT_URLS
    urls = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_URLS

    logger.info("=" * 80)
    logger.info(
        f"Application Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    logger.info(f"Checking {len(urls)} application(s)...")
    logger.info("=" * 80)

    results = []
    for url in urls:
        result = check_application_health(url, logger)
        results.append(result)

    generate_report(results, logger)

    logger.info(f"Log saved to: {LOG_FILE}")


if __name__ == "__main__":
    main()
