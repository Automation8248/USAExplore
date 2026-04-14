import os
import random
import requests
import datetime

# --- Configuration from GitHub Secrets ---
API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX")
HISTORY_FILE = "history.txt"

# Search Queries based on your requirement
QUERIES = [
    "USA best places", 
    "USA tourist places", 
    "USA visiting places", 
    "best vacation spots in USA", 
    "famous cities in USA to visit",
    "top tourist attractions USA",
    "beautiful places to live in USA"
]

def get_seo_content(query_text):
    """Generates clean title and platform-specific hashtags"""
    title = f"Exploring {query_text} - United States"
    
    # Platform Specific SEO (No stars or hashtags in titles as per your rule)
    fb_tags = "#USA #TravelUSA #AmericanCulture #ExploreMore #Vacation #USAPlaces"
    ig_tags = "#USATravel #InstaTravel #ExploreUSA #TravelGram #USATrip #USAHighRes"
    yt_tags = "#TravelGuide #USA #VacationUSA #Shorts #USATour #America"
    
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
    base_query = random.choice(QUERIES)
    title, fb_tags, ig_tags, yt_tags = get_seo_content(base_query)
    
    print(f"Searching for: {base_query}")
    
    # Google Custom Search API URL (searchType=image and size=large)
    api_url = f"https://www.googleapis.com/customsearch/v1?q={base_query}&cx={CX}&key={API_KEY}&searchType=image&imgSize=large"
    
    try:
        response = requests.get(api_url).json()
        items = response.get("items", [])
        
        success = False
        for item in items:
            img_url = item['link']
            
            # Skip if already in history
            if img_url not in history:
                print(f"Processing new image: {img_url}")
                
                # Download Image
                img_response = requests.get(img_url, timeout=20)
                if img_response.status_code == 200:
                    with open("temp.jpg", "wb") as f:
                        f.write(img_response.content)
                    
                    # --- 1. TELEGRAM: Only Image + Date/Time ---
                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
                    tg_chat = os.getenv("TELEGRAM_CHAT_ID")
                    
                    if tg_token and tg_chat:
                        tg_url = f"https://api.telegram.org/bot{tg_token}/sendPhoto"
                        tg_data = {"chat_id": tg_chat, "caption": f"Date: {now}"}
                        with open("temp.jpg", "rb") as photo:
                            requests.post(tg_url, data=tg_data, files={"photo": photo})
                        print("Sent to Telegram.")

                    # --- 2. WEBHOOK: Full Data for FB, IG, YT ---
                    webhook_url = os.getenv("WEBHOOK_URL")
                    if webhook_url:
                        payload = {
                            "image_url": img_url,
                            "title": title,
                            "query": base_query,
                            "facebook_tags": fb_tags,
                            "instagram_tags": ig_tags,
                            "youtube_tags": yt_tags,
                            "caption": f"Check out this amazing spot: {base_query}!",
                            "timestamp": now
                        }
                        requests.post(webhook_url, json=payload)
                        print("Sent to Webhook.")

                    save_history(img_url)
                    success = True
                    break # Process only one image per run
        
        if not success:
            print("No new images found in this batch.")
            
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    run_automation()
