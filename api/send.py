from http.server import BaseHTTPRequestHandler
import json
import random
import string
import time
import requests

# Curated modern User-Agents (fallback if file not available)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.115 Mobile/15E148 Safari/604.1",
]

def generate_device_id():
    chars = string.ascii_lowercase + string.digits
    part1 = ''.join(random.choices(chars, k=8))
    part2 = ''.join(random.choices(chars, k=4))
    part3 = ''.join(random.choices(chars, k=4))
    part4 = ''.join(random.choices(chars, k=4))
    part5 = ''.join(random.choices(chars, k=12))
    return f"{part1}-{part2}-{part3}-{part4}-{part5}"

def get_random_ua():
    # Try to read from bundled file if exists (Vercel includes it if we bundle)
    try:
        import os
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "user-agents.txt"),
            os.path.join(os.path.dirname(__file__), "..", "user-agents.txt"),
            "user-agents.txt",
            "/var/task/user-agents.txt",
            "/var/task/api/user-agents.txt"
        ]
        for p in possible_paths:
            if os.path.exists(p):
                with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = [l.strip() for l in f.readlines() if l.strip()]
                    if lines:
                        return random.choice(lines)
    except:
        pass
    return random.choice(USER_AGENTS)

def send_single_ngl(username, message):
    device_id = generate_device_id()
    ua = get_random_ua()

    headers = {
        'Host': 'ngl.link',
        'sec-ch-ua': '"Google Chrome";v="121", "Chromium";v="121", "Not-A.Brand";v="24"',
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': ua,
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://ngl.link',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://ngl.link/{username}',
        'accept-language': 'en-US,en;q=0.9',
    }

    data = {
        'username': username,
        'question': message,
        'deviceId': device_id,
        'gameSlug': '',
        'referrer': '',
    }

    try:
        resp = requests.post('https://ngl.link/api/submit', headers=headers, data=data, timeout=10)
        # NGL returns 200 even on success, but check body
        if resp.status_code == 200:
            # Sometimes returns JSON with success
            try:
                j = resp.json()
                # If API returns error field, treat as failure
                if isinstance(j, dict) and j.get("status") == "error":
                    return False, resp.status_code, str(j), device_id
            except:
                pass
            return True, resp.status_code, "Sent successfully", device_id
        elif resp.status_code == 429:
            return False, resp.status_code, "Rate limited by NGL - try slower delay", device_id
        elif resp.status_code == 404:
            return False, resp.status_code, "User not found - check username", device_id
        else:
            return False, resp.status_code, f"NGL responded with {resp.status_code}: {resp.text[:200]}", device_id
    except requests.exceptions.Timeout:
        return False, 0, "Timeout connecting to NGL - try again", device_id
    except requests.exceptions.ProxyError:
        return False, 0, "Proxy error (not used in web version)", device_id
    except Exception as e:
        return False, 0, f"Error: {str(e)[:200]}", device_id


class handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default logging
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {
            "status": "online",
            "service": "NGL Spammer API",
            "version": "2.0",
            "endpoints": {
                "POST /api/send": "Send NGL messages - body: {username, message, count, delay}"
            },
            "limits": {
                "maxCountPerRequest": 20,
                "maxDelay": 5,
                "timeoutSeconds": 10
            },
            "usage": "POST with JSON: {\"username\": \"ngluser\", \"message\": \"hello\", \"count\": 5, \"delay\": 0.5}"
        }
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        # CORS headers
        content_length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b'{}'

        try:
            body = json.loads(raw_body.decode('utf-8') if raw_body else '{}')
        except:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": "Invalid JSON body"}).encode())
            return

        username = str(body.get('username', '')).strip().lstrip('@').lstrip('/')
        message = str(body.get('message', '')).strip()
        # Support both "count" and "amount"
        try:
            count = int(body.get('count', body.get('amount', 1)))
        except:
            count = 1
        try:
            delay = float(body.get('delay', 0))
        except:
            delay = 0

        # Validation
        if not username:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": "Username is required"}).encode())
            return

        if not message:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": "Message is required"}).encode())
            return

        if len(message) > 300:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": "Message too long (max 300 chars)"}).encode())
            return

        # Clamp values for Vercel timeout safety
        # Max 20 per request to stay within 10s execution (hobby plan)
        original_count = count
        count = max(1, min(count, 20))
        delay = max(0, min(delay, 3))

        # Username sanity
        if len(username) < 2 or len(username) > 30:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": "Invalid username length (2-30)"}).encode())
            return

        results = []
        success_count = 0
        fail_count = 0
        consecutive_fails = 0

        start_time = time.time()
        # Vercel hobby has ~10s timeout, we enforce 9s max loop
        MAX_EXEC_SECONDS = 9

        for i in range(count):
            # Check timeout guard
            if time.time() - start_time > MAX_EXEC_SECONDS:
                results.append({
                    "index": i+1,
                    "success": False,
                    "error": "Server timeout guard - remaining messages not sent. Try smaller count or use client-side batch mode.",
                    "statusCode": 0
                })
                fail_count += 1
                # Mark remaining as not attempted
                for j in range(i+1, count):
                    results.append({
                        "index": j+1,
                        "success": False,
                        "error": "Skipped due to timeout guard",
                        "statusCode": 0
                    })
                    fail_count += 1
                break

            ok, status, msg, device_id = send_single_ngl(username, message)

            entry = {
                "index": i+1,
                "success": ok,
                "statusCode": status,
                "message": msg,
                "deviceId": device_id
            }
            results.append(entry)

            if ok:
                success_count += 1
                consecutive_fails = 0
            else:
                fail_count += 1
                consecutive_fails += 1
                # If 4 consecutive fails, we already rotate deviceId/UA each request, so just log
                if consecutive_fails >= 4:
                    entry["note"] = "Multiple failures - NGL may be rate limiting. Try increasing delay."

            # Delay between requests (except last)
            if delay > 0 and i < count - 1:
                # Also respect timeout guard
                remaining = MAX_EXEC_SECONDS - (time.time() - start_time)
                # if delay would exceed remaining, break
                if remaining < delay:
                    results.append({
                        "index": i+2,
                        "success": False,
                        "error": f"Stopped early to avoid timeout - {count - (i+1)} remaining not sent",
                        "statusCode": 0
                    })
                    break
                time.sleep(delay)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        response_payload = {
            "success": True,
            "username": username,
            "requested": original_count,
            "processed": len(results),
            "sent": success_count,
            "failed": fail_count,
            "clamped": original_count != count,
            "clampNote": f"Count clamped to {count} per request for server stability. For larger counts, frontend will batch automatically." if original_count != count else None,
            "results": results,
            "meta": {
                "delay": delay,
                "executionTime": round(time.time() - start_time, 2)
            }
        }
        self.wfile.write(json.dumps(response_payload).encode())
