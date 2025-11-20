import subprocess
import re

def run_ab(url, n=100, c=1):
    # Force HTTP/1.1
    cmd = [
        "ab",
        "-n", str(n),
        "-c", str(c),
        "-H", "Connection: close",
        url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr

    # Extract avg time
    avg_match = re.search(r"Time per request:\s+([\d\.]+)\s+\[ms\]", output)
    avg = float(avg_match.group(1)) if avg_match else None

    # Extract failed requests
    failed_match = re.search(r"Failed requests:\s+(\d+)", output)
    failed = int(failed_match.group(1)) if failed_match else None

    return {
        "avg_ms": avg,
        "failed": failed,
        "raw_output": output
    }

if __name__ == "__main__":
    URL = "https://projetmassivedata.appspot.com/api/timeline?user=user1&limit=20"
    result = run_ab(URL, n=200, c=10)
    print(result)
