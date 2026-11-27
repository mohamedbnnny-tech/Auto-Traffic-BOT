import requests
import random
import time

WORKER_REDIRECT_URL = "https://workers.dev"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

KEYWORDS_POOL = [
    "Download GTA 6 Mobile Beta APK Free 2026",
    "Watch Full HD Movies Online Free No Sign Up",
    "Roblox Promo Codes Free Robux Generator 2026",
    "Free PDF Books Download Library Direct Link",
    "Best AI Video Generator Free Unlimited Access",
    "Download Spotify Premium Mod APK Latest Version",
    "Free Netflix Account Generator Working 2026",
    "Minecraft Java and Bedrock Free Download PC",
    "CapCut Pro Mod APK No Watermark Download",
    "FIFA 26 Mobile APK OBB Offline Download",
    "Free Steam Gift Card Codes Generator 2026",
    "Watch Live Football Matches HD Streaming Free"
]

def create_telegraph_account():
    res = requests.get(
        "https://telegra.ph",
        params={"short_name": f"Hub_{random.randint(1000,9999)}", "author_name": "Digital Hub"},
        headers=HEADERS, timeout=15
    ).json()
    return res["result"]["access_token"]

def publish_telegraph(token, kw):
    content = [
        {"tag": "p", "children": [f"Access {kw} directly through our verified 2026 high-speed resource server."]},
        {"tag": "p", "children": [
            {"tag": "a", "attrs": {"href": WORKER_REDIRECT_URL}, "children": [f"👉 CLICK HERE TO ACCESS: {kw.upper()} 👈"]}
        ]}
    ]
    res = requests.post(
        "https://telegra.ph",
        json={"access_token": token, "title": f"{kw} - Direct Link", "content": content},
        headers=HEADERS, timeout=15
    ).json()
    if res.get("ok"):
        return res["result"]["url"]
    return None

def publish_paste(kw):
    text = f"{kw.upper()}\n\nDirect Access Link:\n{WORKER_REDIRECT_URL}\n"
    res = requests.post("https://paste.rs", data=text.encode("utf-8"), timeout=15)
    if res.status_code in [200, 201]:
        return res.text.strip()
    return None

if __name__ == "__main__":
    # Pick 5 random keywords every hour
    selected = random.sample(KEYWORDS_POOL, 5)
    new_links = []
    
    try:
        token = create_telegraph_account()
    except Exception:
        token = None

    for kw in selected:
        if token:
            t_link = publish_telegraph(token, kw)
            if t_link:
                new_links.append(t_link)
        p_link = publish_paste(kw)
        if p_link:
            new_links.append(p_link)
        time.sleep(2)

    if new_links:
        with open("published_links.txt", "a", encoding="utf-8") as f:
            for link in new_links:
                f.write(link + "\n")
        print(f"Successfully generated {len(new_links)} links!")
