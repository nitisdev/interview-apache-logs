import re

total_requests = 0
total_bytes = 0
resource_counts = {}
ip_counts = {}
status_counts = {}

with open("real_apache_logs.log", "r") as f:
    for line in f:
        match = re.match(r'([\d.]+) .* "(.*?)" (\d+) (\d+|-)', line)
        if match:
            ip, request, status, bytes_sent = match.groups()
            total_requests += 1
            total_bytes += int(bytes_sent) if bytes_sent != '-' else 0

            resource = request.split()[1] if len(request.split()) > 1 else ''
            resource_counts[resource] = resource_counts.get(resource, 0) + 1
            ip_counts[ip] = ip_counts.get(ip, 0) + 1
            status_counts[status[0]] = status_counts.get(status[0], 0) + 1

most_requested = max(resource_counts.items(), key=lambda x: x[1])
most_active_ip = max(ip_counts.items(), key=lambda x: x[1])

print(f"Total Requests: {total_requests}")
print(f"Total Data transmitted: {total_bytes / (1024**3):.1f}GiB")
print(f"Most requested resource: {most_requested[0]}")
print(f"Total requests for {most_requested[0]}: {most_requested[1]}")
print(f"Percentage of requests for {most_requested[0]}: {(most_requested[1]/total_requests*100):.10f}")
print(f"Remote host with the most requests: {most_active_ip[0]}")
print(f"Total requests from  {most_active_ip[0]}: {most_active_ip[1]}")
print(f"Percentage of requests from {most_active_ip[0]}: {(most_active_ip[1]/total_requests*100):.10f}")
print(f"Percentage of 1xx requests: {(status_counts.get('1', 0)/total_requests*100):.10f}")
print(f"Percentage of 2xx requests: {(status_counts.get('2', 0)/total_requests*100):.10f}")
print(f"Percentage of 3xx requests: {(status_counts.get('3', 0)/total_requests*100):.10f}")
print(f"Percentage of 4xx requests: {(status_counts.get('4', 0)/total_requests*100):.10f}")
print(f"Percentage of 5xx requests: {(status_counts.get('5', 0)/total_requests*100):.10f}")
