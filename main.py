import os
import random
import requests
import datetime
import time
from playwright.sync_api import sync_playwright

# ==========================================
# CONFIGURATION & DATA
# ==========================================
QUERIES = [
    "USA best places", 
    "USA tourist places", 
    "USA visiting places", 
    "best vacation spots in USA", 
    "famous cities in USA to visit",
    "top tourist attractions USA",
    "beautiful places to live in USA"
]

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
def get_seo_content(query_text):
    """Generates clean title and platform-specific hashtags"""
    title = f"Exploring {query_text} - United States"
    fb_tags = "#USA #TravelUSA #AmericanCulture #ExploreMore #Vacation"
    ig_tags = "#USATravel #InstaTravel #ExploreUSA #TravelGram #USATrip"
    yt_tags = "#TravelGuide #USA #VacationUSA #Shorts #USATour"
    
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
# MAIN HUMAN-BEHAVIOR AUTOMATION
# ==========================================
def run_automation():
    history = get_history()
    
    base_query = random.choice(QUERIES)
    search_query = f"{base_query} high resolution {random.randint(1, 999)}"
    title, fb_tags, ig_tags, yt_tags = get_seo_content(base_query)
    
    print(f"Starting Human-like search for: {search_query}")
    
    success = False
    
    # Failover Logic: Try up to 3 times
    for attempt in range(3):
        if success:
            break
            
        browser_engine = random.choice(["chromium", "firefox", "webkit"])
        user_agent = random.choice(USER_AGENTS)
        print(f"Attempt {attempt + 1}: Using {browser_engine.upper()}")

        try:
            with sync_playwright() as p:
                browser = getattr(p, browser_engine).launch(headless=True)
                # Setting a large viewport to mimic a real desktop monitor
                context = browser.new_context(
                    user_agent=user_agent, 
                    locale='en-US',
                    viewport={'width': 1920, 'height': 1080}
                )
                page = context.new_page()
                
                # --- 1. OPEN GOOGLE ---
                print("1. Opening Google.com")
                page.goto("https://www.google.com/")
                page.wait_for_timeout(random.randint(2000, 4000))
                
                # --- 2. HUMAN TYPING ---
                print("2. Typing like a human...")
                search_input = page.locator('[name="q"]')
                # Type each character with a random delay to simulate human typing
                search_input.press_sequentially(search_query, delay=random.randint(50, 150))
                page.wait_for_timeout(random.randint(800, 1500))
                search_input.press("Enter")
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(random.randint(2000, 3000))
                
                # --- 3. CLICK IMAGES TAB ---
                print("3. Clicking 'Images' tab")
                page.locator("a", has_text="Images").first.click()
                page.wait_for_timeout(random.randint(3000, 5000))
                
                # --- 4. HUMAN SCROLLING ---
                print("4. Scrolling naturally...")
                page.mouse.wheel(0, random.randint(600, 1200))
                page.wait_for_timeout(random.randint(1500, 3000))
                
                # --- 5. CLICK A THUMBNAIL (Like a user picking a photo) ---
                print("5. Clicking a photo to open HD preview...")
                # Select a random image from the top 5 results and click it
                index_to_click = random.randint(0, 4)
                page.locator("div[data-ri] img, img[jsname='Q4LuWd']").nth(index_to_click).click(force=True)
                
                # Wait for the HD image to load in the side panel
                page.wait_for_timeout(random.randint(4000, 7000))
                
                # --- 6. EXTRACT & DOWNLOAD EXACT HD IMAGE ---
                print("6. Extracting HD image URL...")
                hd_img_url = None
                
                # We extract the image that does NOT have 'encrypted' in URL (which means it's the real HD one, not a thumbnail)
                all_images = page.locator("img").all()
                for img in all_images:
                    src = img.get_attribute("src")
                    if src and src.startswith("http") and "encrypted-tbn0" not in src and src not in history:
                        hd_img_url = src
                        break # Stop searching, we found our single HD image
                
                if hd_img_url:
                    print(f"Downloading HD URL: {hd_img_url[:60]}...")
                    img_data = requests.get(hd_img_url, timeout=15).content
                    with open("temp.jpg", "wb") as f:
                        f.write(img_data)
                    
                    # --- TELEGRAM: Send ONLY Image + Date/Time ---
                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
                    tg_chat = os.getenv("TELEGRAM_CHAT_ID")
                    
                    if tg_token and tg_chat:
                        tg_url = f"https://api.telegram.org/bot{tg_token}/sendPhoto"
                        requests.post(tg_url, data={"chat_id": tg_chat, "caption": f"Date: {now}"}, files={"photo": open("temp.jpg", "rb")})
                        print("Sent to Telegram.")
                    
                    # --- WEBHOOK: Send Full Data (URL, Caption, Tags) ---
                    webhook_url = os.getenv("WEBHOOK_URL")
                    if webhook_url:
                        webhook_data = {
                            "image_url": hd_img_url,
                            "title": title,
                            "query_used": base_query,
                            "facebook_tags": fb_tags,
                            "instagram_tags": ig_tags,
                            "youtube_tags": yt_tags,
                            "caption": f"Check out this amazing spot: {base_query}!"
                        }
                        requests.post(webhook_url, json=webhook_data)
                        print("Sent to Webhook.")
                    
                    # Save to history so it's never repeated
                    save_history(hd_img_url)
                    success = True
                else:
                    print("Could not find HD image link, trying another browser...")
                
                browser.close()
                
        except Exception as e:
            print(f"Attempt {attempt + 1} Failed: {e}")
            time.sleep(3)
            continue

if __name__ == "__main__":
    run_automation()
