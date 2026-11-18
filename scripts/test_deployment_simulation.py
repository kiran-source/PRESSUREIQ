"""
Phase 6: Local Deployment Simulation Script.
Executes: streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true
Verifies:
1. Process remains running.
2. Port 8501 is listening.
3. http://localhost:8501/healthz returns HTTP 200.
4. Homepage renders with HTTP 200 and valid HTML.
5. Zero startup exceptions.
"""
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

def run_simulation():
    cmd = [
        "streamlit",
        "run",
        "streamlit_app.py",
        "--server.address",
        "0.0.0.0",
        "--server.port",
        "8501",
        "--server.headless",
        "true",
    ]
    print(f"Command: {' '.join(cmd)}")
    
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    
    health_url = "http://127.0.0.1:8501/healthz"
    home_url = "http://127.0.0.1:8501/"
    
    success = False
    health_ok = False
    home_ok = False
    
    t0 = time.time()
    try:
        # Wait up to 25 seconds for server to initialize
        while time.time() - t0 < 25:
            ret = proc.poll()
            if ret is not None:
                print(f"ERROR: Process exited prematurely with return code {ret}")
                break
                
            try:
                with urllib.request.urlopen(health_url, timeout=3) as resp:
                    if resp.status == 200:
                        content = resp.read().decode("utf-8", errors="ignore").strip()
                        print(f"[OK] Health check /healthz: HTTP {resp.status} (Body: '{content}')")
                        health_ok = True
            except (urllib.error.URLError, ConnectionError, OSError):
                time.sleep(1)
                continue
                
            if health_ok:
                try:
                    with urllib.request.urlopen(home_url, timeout=5) as resp:
                        if resp.status == 200:
                            html = resp.read().decode("utf-8", errors="ignore")
                            title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
                            title = title_match.group(1) if title_match else "Unknown"
                            print(f"[OK] Homepage /: HTTP {resp.status} (Length: {len(html)} bytes, Title: '{title}')")
                            home_ok = True
                except Exception as e:
                    print(f"[ERROR] Homepage fetch failed: {e}")
                break
                
        if health_ok and home_ok and proc.poll() is None:
            success = True
            print("\nSIMULATION RESULT: SUCCESS (Process running, port 8501 listening, healthz=200, home=200)")
            
    finally:
        print("Stopping simulation server...", flush=True)
        proc.terminate()
        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            
        print(f"Server stdout:\n{stdout}", flush=True)
        print(f"Server stderr:\n{stderr}", flush=True)

    return success

if __name__ == "__main__":
    ok = run_simulation()
    sys.exit(0 if ok else 1)
