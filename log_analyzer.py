import re
import csv
import json
from collections import Counter
import os

LOG_FILE = "logs/access.log"
REPORT_CSV = "reports/summary.csv"
REPORT_JSON = "reports/summary.json"

def parse_logs():
    if not os.path.exists(LOG_FILE):
        print("❌ Log file not found!")
        return

    with open(LOG_FILE, "r") as f:
        logs = f.readlines()

    ip_counter = Counter()
    status_counter = Counter()
    skipped_lines = []

    # Enhanced regex: IPv4 or hostname + status code
    log_pattern = re.compile(r'([\w\.\-]+).*" (\d{3}) ')

    for line in logs:
        match = log_pattern.search(line)
        if match:
            ip_or_host = match.group(1)
            status = match.group(2)
            ip_counter[ip_or_host] += 1
            status_counter[status] += 1
        else:
            skipped_lines.append(line.strip())

    os.makedirs("reports", exist_ok=True)

    # Write CSV report
    with open(REPORT_CSV, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Top IPs / Hosts"])
        for ip, count in ip_counter.most_common(10):
            writer.writerow([ip, count])
        writer.writerow([])
        writer.writerow(["Status Code", "Count"])
        for status, count in status_counter.items():
            writer.writerow([status, count])

    # Write JSON report
    summary_data = {
        "top_ips_or_hosts": ip_counter.most_common(10),
        "status_counts": dict(status_counter),
        "skipped_lines": skipped_lines
    }
    with open(REPORT_JSON, "w") as jsonfile:
        json.dump(summary_data, jsonfile, indent=4)

    print(f"✅ Reports generated: {REPORT_CSV} & {REPORT_JSON}")

    if skipped_lines:
        print(f"⚠️ {len(skipped_lines)} lines skipped. Check JSON report for details.")

if __name__ == "__main__":
    parse_logs()