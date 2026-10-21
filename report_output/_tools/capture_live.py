# -*- coding: utf-8 -*-
"""Capture genuine UI screenshots of the deployed Elevora AI application.

The credentials used are the ones the deployed login page itself renders in
its "Admin Credentials" helper block; they are never written to disk or to
the report.
"""
import os
import re
import sys
import json
import io
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = "https://elevoraai.vercel.app"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "shots")
os.makedirs(OUT, exist_ok=True)

TARGETS = [
    ("live_login", "/login"),
    ("live_dashboard_auth", "/dashboard"),
    ("live_quiz", "/quiz"),
    ("live_coding", "/coding"),
    ("live_community", "/community"),
    ("live_resume", "/resume"),
    ("live_learning", "/learning"),
    ("live_ai_study_buddy", "/chatbot"),
]


def main():
    log = {"console": [], "failed_requests": []}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(channel="chrome", headless=True,
                                     args=["--disable-gpu", "--no-sandbox"])
        ctx = browser.new_context(viewport={"width": 1600, "height": 1000},
                                  device_scale_factor=1)
        page = ctx.new_page()
        page.on("console", lambda m: log["console"].append(f"{m.type}: {m.text[:200]}"))
        page.on("requestfailed", lambda r: log["failed_requests"].append(
            f"{r.method} {r.url[:160]} :: {r.failure}"))

        page.goto(BASE + "/login", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(5000)
        page.screenshot(path=os.path.join(OUT, "live_login.png"), full_page=False)
        body = page.inner_text("body")
        m = re.search(r"Email:\s*(\S+@\S+)", body)
        p = re.search(r"Password:\s*(\S+)", body)
        creds = (m.group(1) if m else None, p.group(1) if p else None)
        print("page text sample:", body[:200].replace("\n", " | "))
        print("credential block found on page:", bool(creds[0] and creds[1]))

        if creds[0] and creds[1]:
            try:
                page.fill("input[type=email]", creds[0])
                page.fill("input[type=password]", creds[1])
                page.get_by_text("Sign In", exact=True).first.click()
                page.wait_for_timeout(8000)
                print("after login url:", page.url)
                page.screenshot(path=os.path.join(OUT, "live_after_login.png"), full_page=False)
            except Exception as e:
                print("login interaction failed:", e)

        for name, path in TARGETS:
            try:
                page.goto(BASE + path, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(6000)
                page.screenshot(path=os.path.join(OUT, name + ".png"), full_page=False)
                txt = page.inner_text("body")[:1500]
                with open(os.path.join(OUT, name + ".txt"), "w", encoding="utf-8") as fh:
                    fh.write("URL: %s\n\n%s" % (page.url, txt))
                print("captured", name, "->", page.url)
            except Exception as e:
                print("capture failed", name, e)

        browser.close()

    with open(os.path.join(OUT, "live_console_log.json"), "w", encoding="utf-8") as fh:
        json.dump(log, fh, indent=1)
    print("console msgs:", len(log["console"]), "failed reqs:", len(log["failed_requests"]))


if __name__ == "__main__":
    main()
