import os
import requests
import random
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from fpdf import FPDF

WORKER_REDIRECT_URL = "https://workers.dev"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json"
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

# 1. Fetch Live Trending Keywords (US, UK, CA, FR)
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

# 2. Publish Instant Page on Telegra.ph
def create_telegraph_account():
    res = requests.get(
        "https://telegra.ph",
        params={"short_name": f"Hub_{random.randint(1000,9999)}", "author_name": "Global Trends Hub"},
        headers=HEADERS, timeout=15
    ).json()
    return res["result"]["access_token"]

def publish_telegraph(token, kw):
    content = [
        {"tag": "p", "children": [f"Access {kw} directly through our verified high-speed resource server without delays."]},
        {"tag": "h4", "children": ["Verified Direct Access"]},
        {"tag": "p", "children": [
            {"tag": "a", "attrs": {"href": WORKER_REDIRECT_URL}, "children": [f"👉 CLICK HERE TO ACCESS: {kw.upper()} 👈"]}
        ]}
    ]
    res = requests.post(
        "https://telegra.ph",
        json={"access_token": token, "title": kw, "content": content},
        headers=HEADERS, timeout=15
    ).json()
    if res.get("ok"):
        return res["result"]["url"]
    return None

# 3. Generate SEO PDF File for Scribd / SlideShare
def generate_pdf(kw, index):
    os.makedirs("pdfs", exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    safe_kw = kw.encode("latin-1", "ignore").decode("latin-1")
    pdf.multi_cell(0, 10, f"Complete Resource Guide:\n{safe_kw}", align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, "Thank you for downloading this resource document. Our servers are updated hourly to provide fast, direct access to trending files, streams, and guides.")
    pdf.ln(15)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 255)
    pdf.cell(0, 10, ">>> CLICK HERE FOR DIRECT ACCESS & DOWNLOAD <<<", ln=True, align="C", link=WORKER_REDIRECT_URL)
    
    filename = f"pdfs/resource_{int(time.time())}_{index}.pdf"
    pdf.output(filename)

# 4. Generate RSS Feed (feed.xml) for Flipboard
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
    <link>{WORKER_REDIRECT_URL}</link>
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
        t_link = None
        if token:
            t_link = publish_telegraph(token, kw)
        
        # Fallback to paste.rs if telegra.ph fails so feed.xml is always populated
        if not t_link:
            res = requests.post("https://paste.rs", data=f"{kw.upper()}\n\n{WORKER_REDIRECT_URL}\n".encode("utf-8"), timeout=15)
            if res.status_code in [200, 201]:
                t_link = res.text.strip()

        if t_link:
            published_items.append((kw, t_link))
            with open("published_links.txt", "a", encoding="utf-8") as f:
                f.write(t_link + "\n")

        if idx < 3:
            generate_pdf(kw, idx)
        time.sleep(2)

    update_rss_feed(published_items)
    print(f"Generated {len(published_items)} pages, RSS feed, and PDFs successfully!")

