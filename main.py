import os
import random
import requests
import datetime

# --- Configuration ---
API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX")
HISTORY_FILE = "history.txt"

QUERIES = [
    "USA best places", "USA tourist places", "USA visiting places", 
    "best vacation spots in USA", "top tourist attractions USA"
]

def get_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def run_automation():
    history = get_history()
    # Adding a random number to query to get fresh results from Google
    base_query = random.choice(QUERIES)
    search_query = f"{base_query} {random.randint(1, 100)}" 
    
    print(f"Searching for: {search_query}")
    
    # Official API URL
    api_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&cx={CX}&key={API_KEY}&searchType=image&imgSize=large"
    
    try:
        response = requests.get(api_url).json()
        items = response.get("items", [])
        
        print(f"Google found {len(items)} images.") # Debug log
        
        success = False
        for item in items:
            img_url = item['link']
            
            if img_url not in history:
                print(f"New Image Found: {img_url}")
                
                img_res = requests.get(img_url, timeout=20)
                if img_res.status_code == 200:
                    with open("temp.jpg", "wb") as f:
                        f.write(img_res.content)
                    
                    # Telegram
                    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
                    tg_chat = os.getenv("TELEGRAM_CHAT_ID")
                    if tg_token and tg_chat:
                        requests.post(f"https://api.telegram.org/bot{tg_token}/sendPhoto", 
                                      data={"chat_id": tg_chat, "caption": f"Date: {now}"}, 
                                      files={"photo": open("temp.jpg", "rb")})
                    
                    # Webhook
                    webhook_url = os.getenv("WEBHOOK_URL")
                    if webhook_url:
                        requests.post(webhook_url, json={"image_url": img_url, "title": f"Exploring {base_query}"})

                    # Save to History
                    with open(HISTORY_FILE, "a") as f:
                        f.write(img_url + "\n")
                    
                    success = True
                    break
            else:
                print("Skipping: Image already in history.")

        if not success:
            print("Finished loop: No new unique images found in this batch.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_automation()
