import re
import logging
from collections import defaultdict, Counter
from datetime import datetime

#setup logging
log_filename = f"analysis_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

#file to analyze
log_file = "access.log"
log_pattern = re.compile(r'(\S+) \S+ \S+ \[(.*?)] "(\S+) (\S+) \S+" (\d{3}) (\S+) "([^"]+)"')

#stats
total_requests = 0
unique_ips = set()
http_methods = Counter()
urls = Counter()
status_codes = Counter()
errors = []

#security monitoring
failed_logins = defaultdict(list)
security_incidents = []
forbidden_access = []

#known suspicious user agents
suspicious_agents = ["sqlmap", "nikto", "fuzzer", "acunetix"]

# read and process log file
try:
    with open(log_file, "r") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            match = log_pattern.match(line)
            if not match:
                logging.warning(f"line {line_num}: malformed entry skipped")
                continue

            ip, timestamp, method, url, status, size, user_agent = match.groups()
            status = int(status)

            # stats
            total_requests += 1
            unique_ips.add(ip)
            http_methods[method] += 1
            urls[url] += 1
            status_codes[status] += 1

            # error log
            if 400 <= status < 600:
                errors.append(f"[{timestamp}] {ip} {method} {url} status: {status}")

            # security analysis
            if url == "/login" and status == 401:
                failed_logins[ip].append(timestamp)
                if len(failed_logins[ip]) >= 3:
                    incident = f"possible brute force: {ip} - {len(failed_logins[ip])} failed logins"
                    if incident not in security_incidents:
                        security_incidents.append(incident)
                        logging.warning(incident)

            if status == 403:
                incident = f"forbidden access: {ip} -> {url}"
                forbidden_access.append(incident)
                security_incidents.append(incident)
                logging.warning(incident)

            if any(agent.lower() in user_agent.lower() for agent in suspicious_agents):
                incident = f"suspicious user agent: {ip} -> {user_agent}"
                security_incidents.append(incident)
                logging.warning(incident)

            if any(word in url.lower() for word in ["union", "select", "drop", "insert", "--", ";"]):
                incident = f"potential sql injection: {ip} -> {url}"
                security_incidents.append(incident)
                logging.warning(incident)

except FileNotFoundError:
    logging.error(f"log file '{log_file}' not found")
    print(f"error: {log_file} not found")
except PermissionError:
    logging.error(f"permission denied reading '{log_file}'")
    print(f"error: permission denied for {log_file}")

#write summary report
try:
    with open("summary_report.txt", "w") as f:
        f.write("SERVER LOG SUMMARY\n")
        f.write("=" * 50 + "\n")
        f.write(f"total requests: {total_requests}\n")
        f.write(f"unique visitors: {len(unique_ips)}\n\n")

        f.write("http methods:\n")
        for m, c in http_methods.items():
            f.write(f" {m}: {c}\n")

        f.write("\nmost requested urls:\n")
        for u, c in urls.most_common(5):
            f.write(f" {u}: {c}\n")

        f.write("\nstatus codes:\n")
        for code, c in sorted(status_codes.items()):
            f.write(f" {code}: {c}\n")

except PermissionError:
    logging.error("cannot write summary_report.txt")

# write security report
try:
    with open("security_incidents.txt", "w") as f:
        f.write("SECURITY INCIDENTS\n")
        f.write("=" * 50 + "\n")
        f.write(f"total incidents: {len(security_incidents)}\n\n")

        if failed_logins:
            f.write("brute force attempts:\n")
            for ip, attempts in failed_logins.items():
                if len(attempts) >= 3:
                    f.write(f"{ip}: {len(attempts)} failed logins\n")
            f.write("\n")

        if forbidden_access:
            f.write("forbidden access:\n")
            for incident in forbidden_access:
                f.write(f"{incident}\n")

        for incident in security_incidents:
            f.write(f"{incident}\n")

except PermissionError:
    logging.error("cannot write security_incidents.txt")

#write error log
try:
    with open("error_log.txt", "w") as f:
        f.write("HTTP ERRORS\n")
        f.write("=" * 50 + "\n")
        f.write(f"total errors: {len(errors)}\n\n")
        for e in errors:
            f.write(f"{e}\n")
except PermissionError:
    logging.error("cannot write error_log.txt")

# final console output
print("analysis complete")
print(f"total requests: {total_requests}")
print(f"security incidents: {len(security_incidents)}")
print(f"errors detected: {len(errors)}")
print("reports generated: summary_report.txt, security_incidents.txt, error_log.txt")