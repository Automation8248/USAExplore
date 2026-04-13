import os
import random
import requests
import datetime
import time
from playwright.sync_api import sync_playwright

# ==========================================
# CONFIGURATION & DATA
# ==========================================
CITIES = ["New York City", "Los Angeles", "Chicago", "Miami", "San Francisco", "Las Vegas", "Seattle", "Austin", "Washington DC", "Boston"]
CATEGORIES = ["Famous Places", "Must Visit", "Tourist Attractions", "Vacation Spots", "Best Places to Live", "City Life"]
HISTORY_FILE = "history.txt"

# 15+ Unique User-Agents to prevent blocking
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.2; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Mozilla/5.0 (X11; CrOS x86_64 14544.112.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Android 14; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36"
]

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def get_seo_content(city, category):
    """Generates clean title and platform-specific hashtags"""
    # Clean Title (No hashtags or stars)
    title = f"Exploring {city} {category}"
    
    # Platform Specific SEO Hashtags
    fb_tags = "#USA #TravelUSA #CityVibes #AmericanCulture #ExploreMore"
    ig_tags = "#USATravel #InstaTravel #CityPhotography #ExploreUSA #TravelGram"
    yt_tags = "#TravelGuide #USA #CityTour #VacationUSA #Shorts"
    
    return title, fb_tags, ig_tags, yt_tags

def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_history(url):
    with open(HISTORY_FILE, "a") as f:
        f.write(url + "\n")

# ==========================================
# MAIN AUTOMATION LOGIC
# ==========================================
def run_automation():
    history = get_history()
    city = random.choice(CITIES)
    category = random.choice(CATEGORIES)
    
    # Adding random number to make search query unique every time (helps bypass blocks)
    query = f"{city} {category} USA {random.randint(1, 999)}"
    title, fb_tags, ig_tags, yt_tags = get_seo_content(city, category)
    
    print(f"Starting search for: {query}")
    
    success = False
    # Failover Logic: Try up to 3 times
    for attempt in range(3):
        if success:
            break
            
        browser_engine = random.choice(["chromium", "firefox", "webkit"])
        user_agent = random.choice(USER_AGENTS)
        print(f"Attempt {attempt + 1}: Using {browser_engine.upper()} with random User-Agent")

        try:
            with sync_playwright() as p:
                browser = getattr(p, browser_engine).launch(headless=True)
                context = browser.new_context(user_agent=user_agent)
                page = context.new_page()
                
                # Google Images URL with 'Large' size filter (tbs=isz:l)
                search_url = f"https://www.google.com/search?q={query}&tbm=isch&tbs=isz:l"
                page.goto(search_url)
                page.wait_for_timeout(5000) # Wait 5 seconds to let images load fully
                
                images = page.query_selector_all("img")
                print(f"Found {len(images)} potential images.")
                
                for img in images:
                    src = img.get_attribute("src")
                    
                    # Filter out invalid, tiny thumbnails, and already downloaded images
                    if src and src.startswith("http") and len(src) > 100 and src not in history:
                        print(f"Downloading image: {src[:50]}...")
                        
                        img_data = requests.get(src, timeout=15).content
                        with open("temp.jpg", "wb") as f:
                            f.write(img_data)
                        
                        # --- 1. SEND TO TELEGRAM (ONLY Image + Date/Time) ---
                        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
                        tg_chat = os.getenv("TELEGRAM_CHAT_ID")
                        
                        if tg_token and tg_chat:
                            tg_url = f"https://api.telegram.org/bot{tg_token}/sendPhoto"
                            requests.post(tg_url, data={"chat_id": tg_chat, "caption": f"Date: {now}"}, files={"photo": open("temp.jpg", "rb")})
                            print("Sent to Telegram.")
                        
                        # --- 2. SEND TO WEBHOOK (Full Meta Data) ---
                        webhook_url = os.getenv("WEBHOOK_URL")
                        if webhook_url:
                            webhook_data = {
                                "image_url": src,
                                "title": title,
                                "city": city,
                                "category": category,
                                "facebook_tags": fb_tags,
                                "instagram_tags": ig_tags,
                                "youtube_tags": yt_tags,
                                "caption": f"Welcome to {city}! Check out this amazing {category}."
                            }
                            requests.post(webhook_url, json=webhook_data)
                            print("Sent to Webhook.")
                        
                        # Save to history so it never downloads again
                        save_history(src)
                        success = True
                        break # Exit the image loop once one is successfully processed
                
                browser.close()
                
        except Exception as e:
            print(f"Attempt {attempt + 1} Failed: {e}")
            time.sleep(2) # Chota pause before next retry
            continue

if __name__ == "__main__":
    run_automation()
