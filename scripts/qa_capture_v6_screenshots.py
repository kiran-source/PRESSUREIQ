"""Capture high-resolution screenshots of PRESSUREIQ v6.0 RR Recruitment Intelligence views."""

import asyncio
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request
from playwright.async_api import async_playwright

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "docs" / "dashboard" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PORT = 8502
BASE_URL = f"http://127.0.0.1:{PORT}"


def wait_for_server(url: str, timeout: float = 30.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(f"{url}/_stcore/health", timeout=1.0) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False


async def capture_views():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # 1. Desktop - Recruitment Command Centre
        page = await browser.new_page(viewport={"width": 1440, "height": 1050})
        await page.goto(f"{BASE_URL}?page=Recruitment+Command+Centre", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page.screenshot(path=str(OUT_DIR / "v6_rr_command_centre_desktop.png"))
        print("Captured v6_rr_command_centre_desktop.png")

        # 2. Desktop - RR Target Batters
        await page.goto(f"{BASE_URL}?page=RR+Target+Batters", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page.screenshot(path=str(OUT_DIR / "v6_rr_target_batters_desktop.png"))
        print("Captured v6_rr_target_batters_desktop.png")

        # 3. Desktop - RR Target Bowlers
        await page.goto(f"{BASE_URL}?page=RR+Target+Bowlers", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page.screenshot(path=str(OUT_DIR / "v6_rr_target_bowlers_desktop.png"))
        print("Captured v6_rr_target_bowlers_desktop.png")

        # 4. Desktop - Squad Gap Analysis
        await page.goto(f"{BASE_URL}?page=Squad+Gap+Analysis", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page.screenshot(path=str(OUT_DIR / "v6_rr_squad_gap_desktop.png"))
        print("Captured v6_rr_squad_gap_desktop.png")

        # 5. Desktop - Alternative Target Finder
        await page.goto(f"{BASE_URL}?page=Alternative+Target+Finder", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page.screenshot(path=str(OUT_DIR / "v6_rr_alternatives_desktop.png"))
        print("Captured v6_rr_alternatives_desktop.png")

        # 6. Desktop - Eligibility & Auction Watchlist
        await page.goto(f"{BASE_URL}?page=Eligibility+%26+Auction+Watchlist", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page.screenshot(path=str(OUT_DIR / "v6_rr_watchlist_desktop.png"))
        print("Captured v6_rr_watchlist_desktop.png")

        # 7. Mobile View - Command Centre Mobile
        page_mob = await browser.new_page(viewport={"width": 375, "height": 812})
        await page_mob.goto(f"{BASE_URL}?page=Recruitment+Command+Centre", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page_mob.screenshot(path=str(OUT_DIR / "v6_rr_command_centre_mobile.png"))
        print("Captured v6_rr_command_centre_mobile.png")

        await browser.close()


def main():
    env = os.environ.copy()
    env["STREAMLIT_SERVER_PORT"] = str(PORT)
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    cmd = [
        sys.executable, "-m", "streamlit", "run", "src/dashboard/app.py",
        "--server.port", str(PORT),
        "--server.address", "127.0.0.1",
        "--server.headless", "true"
    ]
    proc = subprocess.Popen(cmd, cwd=str(REPO_ROOT), env=env)
    try:
        print(f"Waiting for Streamlit server on port {PORT}...")
        if not wait_for_server(BASE_URL, timeout=30.0):
            raise RuntimeError("Streamlit server failed to start within timeout.")
        print("Server ready. Starting Playwright capture...")
        asyncio.run(capture_views())
        print("All v6.0 screenshots captured successfully!")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    main()
