from apachelogs import LogParser, COMBINED

parser = LogParser(COMBINED)
resource_counts = {}
ip_counts = {}
status_codes = {}
total_bytes = 0
total_requests = 0

with open("real_apache_logs.log") as f:
    for line in f:
        entry = parser.parse(line)
        total_requests += 1

        # Count IP addresses
        ip = entry.remote_host
        ip_counts[ip] = ip_counts.get(ip, 0) + 1

        # Count resources
        resource = entry.request_line.split()[1]
        resource_counts[resource] = resource_counts.get(resource, 0) + 1

        # Sum bytes
        total_bytes += entry.bytes_sent or 0

        # Count status codes
        status_code = str(entry.final_status)[0]
        status_codes[status_code] = status_codes.get(status_code, 0) + 1

# Find most common resource
most_common_resource = max(resource_counts.items(), key=lambda x: x[1])
# Find most common IP
most_common_ip = max(ip_counts.items(), key=lambda x: x[1])

# Print statistics
print(f"Total Requests: {total_requests}")
print(f"Total Data transmitted: {total_bytes / (1024**3):.1f}GiB")
print(f"Most requested resource: {most_common_resource[0]}")
print(f"Total requests for {most_common_resource[0]}: {most_common_resource[1]}")
print(
    f"Percentage of requests for {most_common_resource[0]}: {(most_common_resource[1]/total_requests)*100:.10f}"
)
print(f"Remote host with the most requests: {most_common_ip[0]}")
print(f"Total requests from {most_common_ip[0]}: {most_common_ip[1]}")
print(
    f"Percentage of requests from {most_common_ip[0]}: {(most_common_ip[1]/total_requests)*100:.10f}"
)

# Print status code percentages
for code in "12345":
    count = status_codes.get(code, 0)
    percentage = (count / total_requests) * 100 if total_requests > 0 else 0
    print(f"Percentage of {code}xx requests: {percentage:.10f}")
