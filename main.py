import os
import random
import requests
import datetime
from playwright.sync_api import sync_playwright

# --- Configuration ---
CITIES = ["New York City", "Los Angeles", "Chicago", "Miami", "San Francisco", "Las Vegas", "Seattle", "Austin", "Washington DC", "Boston"]
CATEGORIES = ["Famous Places", "Must Visit", "Tourist Attractions", "Vacation Spots", "Best Places to Live", "City Life"]
HISTORY_FILE = "history.txt"

# 15+ Different User Agents for Browser Rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.1; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/119.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/104.0.0.0",
    "Mozilla/5.0 (X11; CrOS x86_64 14544.112.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/119.0 Firefox/119.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.70 Safari/537.36"
]

# SEO Tags Logic
def get_seo_content(city, category):
    title = f"Exploring {city} {category}"
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

def run_automation():
    history = get_history()
    city = random.choice(CITIES)
    category = random.choice(CATEGORIES)
    query = f"{city} {category} USA"
    
    # Platform-specific data
    title, fb_tags, ig_tags, yt_tags = get_seo_content(city, category)
    
    # Browser Failover Logic (Try up to 3 times with different browsers)
    success = False
    for attempt in range(3):
        try:
            with sync_playwright() as p:
                browser_type = random.choice(["chromium", "firefox", "webkit"])
                user_agent = random.choice(USER_AGENTS)
                
                browser = getattr(p, browser_type).launch(headless=True)
                context = browser.new_context(user_agent=user_agent)
                page = context.new_page()
                
                # Image search with Large filter
                page.goto(f"https://www.google.com/search?q={query}&tbm=isch&tbs=isz:l")
                page.wait_for_timeout(4000)
                
                images = page.query_selector_all("img")
                for img in images:
                    src = img.get_attribute("src")
                    if src and src.startswith("http") and src not in history:
                        img_data = requests.get(src, timeout=15).content
                        with open("temp.jpg", "wb") as f:
                            f.write(img_data)
                        
                        # --- TELEGRAM: Only Image + Date/Time ---
                        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                        tg_url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendPhoto"
                        requests.post(tg_url, data={"chat_id": os.getenv("TELEGRAM_CHAT_ID"), "caption": f"Date: {now}"}, files={"photo": open("temp.jpg", "rb")})
                        
                        # --- WEBHOOK: Full Data ---
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
                        requests.post(os.getenv("WEBHOOK_URL"), json=webhook_data)
                        
                        save_history(src)
                        success = True
                        break
                
                browser.close()
                if success: break
        except Exception as e:
            print(f"Browser attempt {attempt+1} failed: {e}")
            continue

if __name__ == "__main__":
    run_automation()
