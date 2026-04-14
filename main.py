import os
import random
import requests
import datetime
import shutil
import hashlib
from duckduckgo_search import DDGS
from bing_image_downloader import downloader

# ==========================================
# 1. 80+ UNIVERSAL TITLES (NO Hashtags/Stars)
# ==========================================
UNIVERSAL_TITLES = [
    "Exploring American Beauty", "The Great American Escape", "Stunning USA Views", "Wonders of the United States",
    "A Journey Through America", "Iconic American Landscapes", "Hidden Gems of the USA", "City Lights in America",
    "Beautiful US Destinations", "The Ultimate American Road Trip", "Nature at its Best in USA", "Urban Exploration USA",
    "Capturing American Charm", "Unforgettable US Vacation", "The Heart of the United States", "American Dream Destinations",
    "Discovering the US", "Breathtaking American Scenery", "A Perfect Day in the USA", "Wanderlust United States",
    "The Magic of America", "Majestic Views of the USA", "Travel Goals United States", "The Beauty of US Cities",
    "Exploring the American Wild", "A Glimpse of the USA", "Must Visit Spots in America", "The Best of US Tourism",
    "American Coast to Coast", "Incredible US Landmarks", "The Spirit of America", "Beautiful Mornings in the USA",
    "Chasing Sunsets in America", "The American Adventure", "Discovering US Heritage", "Scenic Routes of the USA",
    "The Vibrant US Culture", "A Traveler's Guide to America", "The Great Outdoors USA", "Captivating American Cities",
    "The Charm of US Small Towns", "Epic US Travel Destinations", "The Diversity of America", "American Wanderlust",
    "The Best Views in the US", "Exploring American History", "The Soul of the United States", "American Travel Diaries",
    "The Beauty of US National Parks", "A View from the USA", "The Magic of US Landscapes", "American Travel Inspiration",
    "The Heartbeat of America", "Discovering Hidden US Treasures", "The Best Places to Visit in USA", "American Scenic Drives",
    "The Beauty of US Coastlines", "A Glimpse into American Life", "The Wonders of US Nature", "American Cityscapes",
    "The Best of American Tourism", "Exploring the US Outdoors", "The Magic of US Cities", "American Travel Adventures",
    "The Beauty of US Architecture", "A Journey Across America", "The Splendor of the USA", "American Travel Dreams",
    "The Best US Vacation Spots", "Exploring American Landmarks", "The Beauty of US Landscapes", "American Travel Experiences",
    "The Best of the United States", "Discovering American Beauty", "The Magic of the USA", "American Travel Moments",
    "The Beauty of US Destinations", "Exploring the United States", "The Best of America", "American Travel Destinations"
]

# ==========================================
# 2. 80+ UNIVERSAL CAPTIONS (NO Hashtags/Stars)
# ==========================================
UNIVERSAL_CAPTIONS = [
    "Take a look at this stunning view from the United States. Truly a masterpiece of nature and architecture.",
    "There is always something new to discover when you travel across America. This spot is simply breathtaking.",
    "A perfect destination to add to your travel bucket list. The USA never fails to amaze.",
    "Experiencing the vibrant culture and beautiful scenery of this amazing American location.",
    "From towering cityscapes to serene natural parks, the United States has it all.",
    "Finding peace and inspiration in one of the most beautiful places in the country.",
    "Every corner of this nation holds a unique story and an unforgettable view.",
    "If you love traveling, this spot in the USA should definitely be your next stop.",
    "Capturing a perfect moment in time at this iconic American landmark.",
    "The energy and beauty of this place are exactly why people love visiting the United States.",
    "Wandering through the beautiful streets and landscapes of America.",
    "This is what the ultimate American getaway looks like. Absolutely mesmerizing.",
    "Exploring the hidden treasures and well known wonders of the US.",
    "A breathtaking scene that showcases the vast diversity of the American landscape.",
    "Whether it is city life or quiet nature, the United States offers incredible experiences.",
    "Taking a moment to appreciate the breathtaking beauty of this US destination.",
    "This spot perfectly captures the spirit and charm of the American outdoors.",
    "An unforgettable view that makes traveling across the USA so worthwhile.",
    "Discovering the perfect blend of history, culture, and natural beauty here.",
    "A picture perfect moment from a highly recommended vacation spot in America.",
    "The stunning contrast of urban life and natural wonders in the United States.",
    "Living for these beautiful travel moments across the USA.",
    "This location offers one of the most scenic and relaxing views you can find.",
    "A fantastic place to explore, unwind, and create amazing memories in America.",
    "The majestic beauty of this place is something everyone should see in person.",
    "Travel brings power and love back into your life, especially in places like this.",
    "Showcasing the true essence of American beauty through this captivating view.",
    "This beautiful spot is a testament to the incredible sights the US has to offer.",
    "A classic American view that continues to inspire travelers from everywhere.",
    "Finding the magic in everyday moments at this spectacular US location.",
    "The ultimate destination for anyone looking to experience the best of America.",
    "A wonderful reminder of how vast and beautiful the United States truly is.",
    "Exploring new places and finding incredible views like this across the USA.",
    "This destination perfectly highlights the breathtaking scenery of America.",
    "A mesmerizing location that should be on every travel enthusiasts radar.",
    "Taking in the sights and sounds of this beautiful and iconic US spot.",
    "The perfect backdrop for an unforgettable American travel experience.",
    "Discovering the charm and elegance of this remarkable place in the United States.",
    "A truly magnificent view that highlights the diverse beauty of America.",
    "This is why the USA remains one of the top travel destinations in the world.",
    "Enjoying the spectacular views and unique atmosphere of this American location.",
    "A breathtaking spot that perfectly captures the wonder of traveling in the US.",
    "Finding incredible beauty and inspiration in this amazing corner of America.",
    "This destination offers a truly unique and unforgettable American experience.",
    "Exploring the wonders of the United States one beautiful location at a time.",
    "A fantastic view that reminds us of the endless beauty found across America.",
    "This spot is a perfect example of the incredible natural and urban landscapes in the US.",
    "Taking a peaceful moment to admire the stunning scenery of this American destination.",
    "A highly recommended place to visit for anyone traveling through the United States.",
    "This beautiful location perfectly represents the vibrant spirit of America.",
    "Enjoying the mesmerizing sights and incredible atmosphere of this US spot.",
    "A truly awe inspiring view that makes exploring America so rewarding.",
    "This destination is a must see for anyone looking for beautiful American scenery.",
    "Finding beauty and tranquility in this wonderful location across the USA.",
    "A perfect example of the breathtaking sights you can discover in the United States.",
    "Exploring the unique charm and incredible views of this American landmark.",
    "This spot offers a fantastic experience and a truly beautiful view of America.",
    "Taking in the magnificent scenery and vibrant culture of this US destination.",
    "A wonderful place to relax and enjoy the incredible beauty of the United States.",
    "This location highlights the stunning diversity and charm of American landscapes.",
    "Enjoying a perfect travel moment at this iconic and beautiful US spot.",
    "A breathtaking view that showcases the amazing sights found across America.",
    "This destination perfectly captures the magic and wonder of the United States.",
    "Finding incredible inspiration and beauty at this spectacular American location.",
    "A highly recommended spot for anyone looking to experience the beauty of the US.",
    "This beautiful place is a perfect reminder of the stunning scenery in America.",
    "Taking a moment to appreciate the unique charm and atmosphere of this US spot.",
    "A truly spectacular view that highlights the amazing diversity of the United States.",
    "This destination offers an unforgettable experience and breathtaking American views.",
    "Exploring the incredible sights and wonderful atmosphere of this location in the USA.",
    "A fantastic place to visit for anyone who loves beautiful American landscapes.",
    "This spot perfectly highlights the majestic beauty and charm of the United States.",
    "Enjoying the stunning scenery and unique experience of this American destination.",
    "A breathtaking location that perfectly captures the true essence of America.",
    "Finding amazing views and incredible beauty at this wonderful spot in the US.",
    "This destination is a perfect example of the spectacular sights across the United States.",
    "Taking in the beautiful atmosphere and incredible views of this American landmark.",
    "A truly mesmerizing spot that highlights the amazing wonder of the USA.",
    "This beautiful location offers a fantastic and unforgettable American travel experience."
]

# ==========================================
# 3. PLATFORM SPECIFIC SEO TAGS 
# ==========================================
def get_platform_tags():
    fb_tags = "#USA #TravelUSA #AmericanCulture #ExploreMore #Vacation"
    ig_tags = "#USATravel #InstaTravel #ExploreUSA #TravelGram #USATrip"
    yt_tags = "#TravelGuide #USA #VacationUSA #Shorts #USATour"
    return fb_tags, ig_tags, yt_tags

QUERIES = [
    "USA best places", "USA tourist places", "USA visiting places", 
    "best vacation spots in USA", "top tourist attractions USA",
    "Grand Canyon USA", "New York City landmarks", "Miami Beach Florida"
]

HISTORY_FILE = "history.txt"
OUTPUT_DIR = "dataset" # For Bing Backup

# ==========================================
# 4. HELPER FUNCTIONS
# ==========================================
def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_history(record):
    with open(HISTORY_FILE, "a") as f:
        f.write(record + "\n")

def get_image_hash(filepath):
    with open(filepath, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def get_current_time_data():
    now = datetime.datetime.now()
    return {
        "day": now.strftime("%A"),
        "date": now.strftime("%d-%B-%Y"),
        "time": now.strftime("%H:%M:%S")
    }

def send_to_telegram(photo_path, time_data):
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat = os.getenv("TELEGRAM_CHAT_ID")
    if tg_token and tg_chat:
        tg_url = f"https://api.telegram.org/bot{tg_token}/sendPhoto"
        tg_message = f"Day: {time_data['day']}\nDate: {time_data['date']}\nTime: {time_data['time']}"
        with open(photo_path, "rb") as photo:
            requests.post(tg_url, data={"chat_id": tg_chat, "caption": tg_message}, files={"photo": photo})
        print("📤 Sent to Telegram with Exact Time/Date.")

def send_to_webhook(payload):
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        requests.post(webhook_url, json=payload)
        print("🔗 Sent full data to Webhook.")

# ==========================================
# 5. SEARCH LOGIC (DUCKDUCKGO - Primary)
# ==========================================
def try_duckduckgo(search_query, selected_title, selected_caption, fb_tags, ig_tags, yt_tags, history):
    try:
        print("🌐 Trying Primary Method: DuckDuckGo...")
        with DDGS() as ddgs:
            results = list(ddgs.images(search_query, size="Large", max_results=10))
        
        for result in results:
            img_url = result.get("image")
            if img_url and img_url not in history:
                print(f"✅ [DDG] Found Unique Image URL: {img_url}")
                
                # Download temp for Telegram
                img_data = requests.get(img_url, timeout=15).content
                temp_file = "temp_post.jpg"
                with open(temp_file, "wb") as f:
                    f.write(img_data)
                
                time_data = get_current_time_data()
                
                # Send to Telegram
                send_to_telegram(temp_file, time_data)
                
                # Send to Webhook (With Direct URL)
                webhook_payload = {
                    "image_url": img_url,
                    "title": selected_title,
                    "caption": selected_caption,
                    "facebook_tags": fb_tags,
                    "instagram_tags": ig_tags,
                    "youtube_tags": yt_tags,
                    "status": "Success_DDG",
                    "run_day": time_data["day"],
                    "run_date": time_data["date"],
                    "run_time": time_data["time"]
                }
                send_to_webhook(webhook_payload)
                
                save_history(img_url)
                if os.path.exists(temp_file): os.remove(temp_file)
                return True
    except Exception as e:
        print(f"⚠️ [DDG] Error: {e}")
    return False

# ==========================================
# 6. SEARCH LOGIC (BING - Fallback/Backup)
# ==========================================
def try_bing(search_query, selected_title, selected_caption, fb_tags, ig_tags, yt_tags, history):
    try:
        print("🔄 Primary Failed. Switching to Backup Method: Bing Downloader...")
        downloader.download(search_query, limit=1, output_dir=OUTPUT_DIR, adult_filter_off=True, force_replace=False, timeout=30, verbose=False)
        
        query_folder = os.path.join(OUTPUT_DIR, search_query)
        if not os.path.exists(query_folder):
            return False

        for img_file in os.listdir(query_folder):
            img_path = os.path.join(query_folder, img_file)
            img_hash = get_image_hash(img_path)
            
            if img_hash not in history:
                print(f"✅ [BING] Found Unique Image: {img_file}")
                
                time_data = get_current_time_data()
                
                # Send to Telegram
                send_to_telegram(img_path, time_data)
                
                # Send to Webhook
                webhook_payload = {
                    "image_url": "Downloaded via Bing - No Public URL", 
                    "image_name": img_file,
                    "title": selected_title,
                    "caption": selected_caption,
                    "facebook_tags": fb_tags,
                    "instagram_tags": ig_tags,
                    "youtube_tags": yt_tags,
                    "status": "Success_BING",
                    "run_day": time_data["day"],
                    "run_date": time_data["date"],
                    "run_time": time_data["time"]
                }
                send_to_webhook(webhook_payload)
                
                save_history(img_hash)
                
                # Cleanup
                shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
                return True
            else:
                print("⚠️ [BING] Duplicate Hash found.")
                
        # Cleanup even if no unique image found
        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    except Exception as e:
        print(f"⚠️ [BING] Error: {e}")
        if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    return False

# ==========================================
# 7. MAIN EXECUTION (Failover System)
# ==========================================
def run_automation():
    history = get_history()
    base_query = random.choice(QUERIES)
    
    selected_title = random.choice(UNIVERSAL_TITLES)
    selected_caption = random.choice(UNIVERSAL_CAPTIONS)
    fb_tags, ig_tags, yt_tags = get_platform_tags()
    
    print(f"🎯 Selected Title: {selected_title}")

    success = False
    
    # Try 3 times total
    for attempt in range(3):
        if success:
            break
            
        search_query = f"{base_query} high resolution {random.randint(1, 1000)}"
        print(f"\n🚀 ATTEMPT {attempt+1} for: '{search_query}'")

        # STEP 1: Try DuckDuckGo first
        if try_duckduckgo(search_query, selected_title, selected_caption, fb_tags, ig_tags, yt_tags, history):
            success = True
            break
            
        # STEP 2: If DDG fails, instantly try Bing
        if try_bing(search_query, selected_title, selected_caption, fb_tags, ig_tags, yt_tags, history):
            success = True
            break

    if not success:
        print("❌ All methods (DuckDuckGo & Bing) failed after multiple attempts.")

if __name__ == "__main__":
    run_automation()
