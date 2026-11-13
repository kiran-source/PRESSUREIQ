"""Capture high-resolution screenshots of PRESSUREIQ v5.0 Visual Intelligence views."""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "dashboard" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PORT = os.getenv("STREAMLIT_PORT", "8501")
BASE_URL = f"http://localhost:{PORT}"


async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop Profile View - Ruturaj Gaikwad
        page = await browser.new_page(viewport={"width": 1440, "height": 1050})
        await page.goto(f"{BASE_URL}?page=Player+Intelligence", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page.screenshot(path=str(OUT_DIR / "v5_batter_hero_desktop.png"))
        print("Captured v5_batter_hero_desktop.png")

        # 2. Desktop Bowler Profile View - Liam Dawson
        bowling_radio = page.locator("text=Bowling").first
        await bowling_radio.wait_for(state="visible", timeout=10000)
        await bowling_radio.click()
        await asyncio.sleep(2.0)
        await page.screenshot(path=str(OUT_DIR / "v5_bowler_hero_desktop.png"))
        print("Captured v5_bowler_hero_desktop.png")

        # 3. Mobile View - Batter Profile Hero
        page_mobile = await browser.new_page(viewport={"width": 375, "height": 812})
        await page_mobile.goto(f"{BASE_URL}?page=Player+Intelligence", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page_mobile.screenshot(path=str(OUT_DIR / "v5_batter_hero_mobile.png"))
        print("Captured v5_batter_hero_mobile.png")

        # 4. Desktop Leaderboards - Top 3 Podium Cards
        await page.goto(f"{BASE_URL}?page=Pressure+Leaderboards", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page.screenshot(path=str(OUT_DIR / "v5_leaderboard_podium_desktop.png"))
        print("Captured v5_leaderboard_podium_desktop.png")

        # 5. Desktop Player Comparison - Side by Side Portraits
        await page.goto(f"{BASE_URL}?page=Player+Comparison", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page.screenshot(path=str(OUT_DIR / "v5_player_comparison_desktop.png"))
        print("Captured v5_player_comparison_desktop.png")

        # 6. Desktop Emerging Talent - Visual Scouting Gallery
        await page.goto(f"{BASE_URL}?page=Emerging+Talent", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page.screenshot(path=str(OUT_DIR / "v5_emerging_gallery_desktop.png"))
        print("Captured v5_emerging_gallery_desktop.png")

        # 7. Desktop Player Directory - Searchable 227-Athlete Grid
        await page.goto(f"{BASE_URL}?page=Player+Directory", wait_until="networkidle")
        await asyncio.sleep(2.5)
        await page.screenshot(path=str(OUT_DIR / "v5_player_directory_desktop.png"))
        print("Captured v5_player_directory_desktop.png")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(capture())
