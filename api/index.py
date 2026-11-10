from flask import Flask, request, jsonify
import random
import string
import time
import requests
import os

app = Flask(__name__)

# Pre-load HTML at startup - try embedded file first, then filesystem
HTML_CONTENT = None
try:
    from api.html_content import HTML_CONTENT as _EMBEDDED_HTML
    HTML_CONTENT = _EMBEDDED_HTML
except:
    try:
        from html_content import HTML_CONTENT as _EMBEDDED_HTML2
        HTML_CONTENT = _EMBEDDED_HTML2
    except:
        pass
if not HTML_CONTENT:
    try:
        _candidates = [
            os.path.join(os.path.dirname(__file__), '..', 'index.html'),
            os.path.join(os.getcwd(), 'index.html'),
            '/var/task/index.html',
            os.path.join('/var/task', 'public', 'index.html'),
            'index.html',
            os.path.join(os.path.dirname(__file__), '../public/index.html'),
        ]
        for _p in _candidates:
            if os.path.exists(_p):
                with open(_p, 'r', encoding='utf-8') as _f:
                    HTML_CONTENT = _f.read()
                break
    except Exception:
        pass
if not HTML_CONTENT:
    HTML_CONTENT = "<html><body><h1>NGL Spammer</h1><p>API is online at /api/send</p></body></html>"

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
    try:
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
    """ REAL - one HTTP POST to https://ngl.link/api/submit per call
        Every single message does this exact request with fresh deviceId + UA.
        Returns (success_bool, status_code, msg, device_id) - success only if NGL confirms 200
    """
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
        if resp.status_code == 200:
            try:
                j = resp.json()
                # NGL sometimes returns JSON with error even on 200
                if isinstance(j, dict) and j.get("status") == "error":
                    return False, resp.status_code, str(j), device_id
                if isinstance(j, dict) and "error" in j and j.get("error"):
                    return False, resp.status_code, str(j.get("error")), device_id
            except:
                pass
            # 200 with no error = REAL delivered to NGL inbox
            return True, resp.status_code, "Delivered", device_id
        elif resp.status_code == 429:
            return False, resp.status_code, "Rate limited by NGL - too fast", device_id
        elif resp.status_code == 404:
            return False, resp.status_code, "User not found", device_id
        else:
            return False, resp.status_code, f"NGL {resp.status_code}: {resp.text[:200]}", device_id
    except requests.exceptions.Timeout:
        return False, 0, "Timeout to NGL", device_id
    except Exception as e:
        return False, 0, f"Error: {str(e)[:200]}", device_id

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route('/', methods=['GET'])
def serve_index():
    if HTML_CONTENT:
        return HTML_CONTENT, 200, {'Content-Type': 'text/html; charset=utf-8'}
    return "index.html not found", 404

@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({"status": "ok", "service": "NGL Spammer", "python": True, "vercel": True, "flask": True})

@app.route('/api/send', methods=['GET', 'POST', 'OPTIONS'])
def send():
    if request.method == 'OPTIONS':
        return '', 200
    if request.method == 'GET':
        return jsonify({
            "status": "online",
            "service": "NGL Spammer API",
            "version": "2.0",
            "usage": "POST with JSON: {\"username\": \"ngluser\", \"message\": \"hello\", \"count\": 5, \"delay\": 0.5}",
            "limits": {"maxCountPerRequest": 20, "maxDelay": 3}
        })
    try:
        body = request.get_json(force=True) or {}
    except:
        return jsonify({"success": False, "error": "Invalid JSON body"}), 400

    username = str(body.get('username', '')).strip().lstrip('@').lstrip('/')
    if 'ngl.link/' in username:
        username = username.split('ngl.link/')[-1].split('/')[0].split('?')[0]
    username = username.strip()
    message = str(body.get('message', '')).strip()
    try:
        count = int(body.get('count', body.get('amount', 1)))
    except:
        count = 1
    try:
        delay = float(body.get('delay', 0))
    except:
        delay = 0

    if not username:
        return jsonify({"success": False, "error": "Username is required"}), 400
    if not message:
        return jsonify({"success": False, "error": "Message is required"}), 400
    if len(message) > 300:
        return jsonify({"success": False, "error": "Message too long (max 300 chars)"}), 400
    if len(username) < 2 or len(username) > 30:
        return jsonify({"success": False, "error": "Invalid username length (2-30)"}), 400

    original_count = count
    # Vercel timeout is 10s - clamp per request to 20 so it finishes fast and reliably
    # Frontend automatically batches 1000 into 50x20 real requests - ALL are real HTTP POSTs to NGL
    count = max(1, min(count, 20))
    delay = max(0, min(delay, 3))

    results = []
    success_count = 0
    fail_count = 0
    start_time = time.time()
    MAX_EXEC_SECONDS = 9

    # REAL LOOP - each iteration = 1 real requests.post to ngl.link/api/submit
    for i in range(count):
        if time.time() - start_time > MAX_EXEC_SECONDS:
            results.append({"index": i+1, "success": False, "error": "Timeout guard", "statusCode": 0})
            fail_count += 1
            for j in range(i+1, count):
                results.append({"index": j+1, "success": False, "error": "Skipped timeout", "statusCode": 0})
                fail_count += 1
            break
        ok, status, msg, device_id = send_single_ngl(username, message)
        entry = {"index": i+1, "success": ok, "statusCode": status, "message": msg, "deviceId": device_id}
        results.append(entry)
        if ok:
            success_count += 1
        else:
            fail_count += 1
        # Real delay between each NGL hit - helps avoid 429 while staying fast
        if delay > 0 and i < count - 1:
            remaining = MAX_EXEC_SECONDS - (time.time() - start_time)
            if remaining < delay:
                break
            time.sleep(delay)

    return jsonify({
        "success": True,
        "username": username,
        "requested": original_count,
        "processed": len(results),
        "sent": success_count,
        "failed": fail_count,
        "clamped": original_count != count,
        "clampNote": f"Count clamped to {count} per request. Frontend batches automatically so 100 = 5x20 real sends." if original_count != count else None,
        "results": results,
        "meta": {"delay": delay, "executionTime": round(time.time() - start_time, 2), "real": "Each 'sent' = 1 verified HTTP 200 from https://ngl.link/api/submit"}
    })

@app.route('/api/index.py', methods=['GET', 'POST', 'OPTIONS'])
def index_py_fallback():
    original = request.headers.get('x-matched-path') or request.headers.get('x-vercel-matched-path') or request.headers.get('x-vercel-rewrite') or request.headers.get('x-forwarded-url') or ''
    if request.method == 'POST':
        try:
            body = request.get_json(force=True, silent=True) or {}
            if body.get('username') or body.get('message'):
                return send()
        except:
            pass
        endpoint = request.args.get('original_path') or request.args.get('endpoint') or request.args.get('path') or original or ''
        if 'health' in endpoint or 'health' in original:
            return health()
        if 'send' in endpoint or 'send' in original:
            return send()
        return send()
    endpoint = request.args.get('original_path') or request.args.get('endpoint') or request.args.get('path') or original or ''
    if 'health' in endpoint.lower():
        return health()
    if 'send' in endpoint.lower():
        return send()
    if HTML_CONTENT:
        return HTML_CONTENT, 200, {'Content-Type': 'text/html; charset=utf-8'}
    return jsonify({
        "status": "online",
        "service": "NGL Spammer API",
        "version": "2.0",
        "note": "Frontend not found, but API is online",
        "endpoints": {"GET /api/health": "Health check", "POST /api/send": "Send NGL messages"},
        "path_seen": request.path,
        "method": request.method
    })

@app.route('/api/<path:path>', methods=['GET','POST','OPTIONS'])
def catch_all(path):
    if path in ['send', 'send.py', 'health', 'health.py', 'index.py']:
        if 'send' in path:
            return send()
        elif 'health' in path:
            return health()
        else:
            return index_py_fallback()
    return jsonify({"error": "Not found", "path": path, "seen_path": request.path}), 404
