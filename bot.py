import os
import requests
import random
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from fpdf import FPDF

WORKER_REDIRECT_URL = "https://workers.dev"
GITHUB_PAGES_BASE = "https://github.io"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36"
}

EVERGREEN_KEYWORDS = [
    "Watch Full HD Movies Online Free No Sign Up",
    "Download GTA 6 Mobile Beta APK Free 2026",
    "Roblox Promo Codes Free Robux Generator 2026",
    "Free PDF Books Download Library Direct Link",
    "Best AI Video Generator Free Unlimited Access",
    "Watch Live Football Matches HD Streaming Free",
    "CapCut Pro Mod APK No Watermark Download",
    "Free Steam Gift Card Codes Generator 2026"
]

def fetch_live_trends():
    geos = ["US", "GB", "CA", "FR"]
    trends = []
    for geo in geos:
        try:
            url = f"https://google.com{geo}"
            res = requests.get(url, headers=HEADERS, timeout=10)
            if res.status_code == 200:
                root = ET.fromstring(res.text)
                for item in root.findall(".//item/title"):
                    if item.text:
                        clean_title = item.text.strip()
                        trends.append(f"{clean_title} Live Stream & Full Guide")
                        trends.append(f"Download {clean_title} Full Resource Pack")
        except Exception:
            continue
    return trends if trends else EVERGREEN_KEYWORDS

def create_html_page(kw, index):
    os.makedirs("posts", exist_ok=True)
    slug = f"post-{int(time.time())}-{index}.html"
    filepath = f"posts/{slug}"
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{kw}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f4f6f9; color: #222; text-align: center; padding: 40px 20px; }}
        .card {{ max-width: 650px; margin: auto; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        h1 {{ font-size: 24px; color: #111; margin-bottom: 15px; }}
        p {{ font-size: 16px; color: #555; line-height: 1.6; }}
        .btn {{ display: inline-block; margin-top: 25px; padding: 16px 32px; background: #0066ff; color: #fff; text-decoration: none; font-size: 18px; font-weight: bold; border-radius: 8px; }}
        .btn:hover {{ background: #0052cc; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>{kw}</h1>
        <p>Access the verified 2026 high-speed resource, live stream, and direct download server below without surveys or delays.</p>
        <a class="btn" href="{WORKER_REDIRECT_URL}">👉 CLICK HERE FOR DIRECT ACCESS 👈</a>
        <p style="font-size: 12px; color: #888; margin-top: 30px;">Server status: Online | Updated automatically</p>
    </div>
</body>
</html>"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    return f"{GITHUB_PAGES_BASE}/{filepath}"

def generate_pdf(kw, index):
    os.makedirs("pdfs", exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    safe_kw = kw.encode("latin-1", "ignore").decode("latin-1")
    pdf.multi_cell(0, 10, f"Complete Resource Guide:\n{safe_kw}", align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, "Click the button below for immediate access to the full resource and live updates.")
    pdf.ln(15)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 255)
    pdf.cell(0, 10, ">>> CLICK HERE FOR DIRECT ACCESS <<<", ln=True, align="C", link=WORKER_REDIRECT_URL)
    pdf.output(f"pdfs/resource_{int(time.time())}_{index}.pdf")

def update_rss_feed(items):
    rss_items = ""
    pub_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    for title, link in items:
        safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        rss_items += f"""
        <item>
            <title>{safe_title}</title>
            <link>{link}</link>
            <description>Direct verified access and live updates for {safe_title}.</description>
            <pubDate>{pub_date}</pubDate>
        </item>"""

    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Global Trending Resources Hub</title>
    <link>{GITHUB_PAGES_BASE}</link>
    <description>Hourly updated trending guides, streams, and direct resources.</description>
    {rss_items}
</channel>
</rss>"""
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_content)

if __name__ == "__main__":
    all_keywords = fetch_live_trends()
    selected = random.sample(all_keywords, min(8, len(all_keywords)))
    published_items = []

    for idx, kw in enumerate(selected):
        page_url = create_html_page(kw, idx)
        published_items.append((kw, page_url))
        with open("published_links.txt", "a", encoding="utf-8") as f:
            f.write(page_url + "\n")
        if idx < 3:
            generate_pdf(kw, idx)

    update_rss_feed(published_items)
    print(f"Generated {len(published_items)} HTML pages, RSS feed, and PDFs successfully!")
