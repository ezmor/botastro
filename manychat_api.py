# manychat_api.py

import requests
from config import MANICHAT_API_KEY, REQUEST_TIMEOUT

MANICHAT_API_URL = "https://api.manychat.com/fb"


def send_message(user_id, text):
    url = f"{MANICHAT_API_URL}/sending/sendContent"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANICHAT_API_KEY}"}
    data = {
        "subscriber_id": user_id,
        "message": {
            "text": text
        }
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=REQUEST_TIMEOUT)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error sending message: {response.text}")
        return None


def get_user_info(user_id):
    url = f"{MANICHAT_API_URL}/subscriber/getInfo"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANICHAT_API_KEY}"}
    data = {"subscriber_id": user_id}
    
    response = requests.post(url, json=data, headers=headers, timeout=REQUEST_TIMEOUT)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting user info: {response.text}")
        return None
