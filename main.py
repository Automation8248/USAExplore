import os
import random
import requests
import datetime
import shutil
from bing_image_downloader import downloader

# --- Configuration ---
QUERIES = [
    "USA best places", "USA tourist places", "USA visiting places", 
    "best vacation spots in USA", "top tourist attractions USA",
    "Grand Canyon USA", "New York City landmarks", "Miami Beach Florida"
]

HISTORY_FILE = "history.txt"
OUTPUT_DIR = "dataset"

def get_seo_content(query_text):
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

def run_automation():
    history = get_history()
    base_query = random.choice(QUERIES)
    # Adding variety for search
    search_query = f"{base_query} high resolution"
    title, fb_tags, ig_tags, yt_tags = get_seo_content(base_query)
    
    print(f"🚀 Starting Bing Downloader for: {search_query}")

    # Bing downloader logic
    # Limit 5 rakha hai taaki humein history check karne ke liye options milein
    downloader.download(
        search_query, 
        limit=5, 
        output_dir=OUTPUT_DIR, 
        adult_filter_off=True, 
        force_replace=False, 
        timeout=60,
        verbose=False
    )

    # Downloaded images folder check
    query_folder = os.path.join(OUTPUT_DIR, search_query)
    if not os.path.exists(query_folder):
        print("❌ No images downloaded.")
        return

    success = False
    for img_file in os.listdir(query_folder):
        img_path = os.path.join(query_folder, img_file)
        
        # Unique check (using filename as a simple history check for Bing)
        if img_file not in history:
            print(f"✅ Processing New Image: {img_file}")
            
            # --- 1. TELEGRAM ---
            now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
            tg_chat = os.getenv("TELEGRAM_CHAT_ID")
            
            if tg_token and tg_chat:
                tg_url = f"https://api.telegram.org/bot{tg_token}/sendPhoto"
                with open(img_path, "rb") as photo:
                    requests.post(tg_url, data={"chat_id": tg_chat, "caption": f"Date: {now}"}, files={"photo": photo})
                print("📤 Sent to Telegram.")

            # --- 2. WEBHOOK ---
            webhook_url = os.getenv("WEBHOOK_URL")
            if webhook_url:
                payload = {
                    "title": title,
                    "facebook_tags": fb_tags,
                    "instagram_tags": ig_tags,
                    "youtube_tags": yt_tags,
                    "image_name": img_file,
                    "status": "Success"
                }
                requests.post(webhook_url, json=payload)
                print("🔗 Sent to Webhook.")

            save_history(img_file)
            success = True
            break # Process only one image

    # Cleanup: Delete the dataset folder to keep GitHub workspace clean
    shutil.rmtree(OUTPUT_DIR)
    print("🧹 Cleanup done.")

if __name__ == "__main__":
    run_automation()
