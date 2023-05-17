# -*- coding: utf-8 -*-
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from config import MANICHAT_API_KEY, REQUEST_TIMEOUT, MANICHAT_API_KEY_WHATSAPP

MANICHAT_API_URL = "https://api.manychat.com/fb"

def send_message(user_id, text, tag=None, tag_remove=None, callback_url=None, callback_timeout=None):
    url = f"{MANICHAT_API_URL}/sending/sendContent"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANICHAT_API_KEY}"}
    data = {
        "subscriber_id": user_id,
        "data": {
            "version": "v2",
            "content": {
                "messages": [
                    {
                        "type": "text",
                        "text": text
                    }
                ],
                "actions": [],
                "quick_replies": [] #optional, not supported for WhatsApp and Telegram
            }
        },
        "messaging_type": "RESPONSE"
    }

    if tag:
        add_tag_action = {
            "action": "add_tag",
            "tag_name": tag
        }
        data["data"]["content"]["actions"].append(add_tag_action)

    if tag_remove:
        remove_tag_action = {
            "action": "remove_tag",
            "tag_name": tag_remove
        }
        data["data"]["content"]["actions"].append(remove_tag_action)

    if callback_url:
        print(f"Sending message with tag: {tag}")
        external_message_callback = {
            "url": callback_url,
            "method": "post",
            "headers": {"Content-Type": "application/json"},
            "payload": {
                "id": user_id,
                "tag": "final_message_2",
                "message": text,
            }
        }
        if callback_timeout:
            external_message_callback["timeout"] = callback_timeout
        
        data["data"]["content"]["messages"][0]["external_message_callback"] = external_message_callback
        print(f"external_message_callback content: {external_message_callback}")

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    try:
        response = session.post(url, json=data, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        print(f"Status code: {response.status_code}")  
        print(f"Response content: {response.content.decode('utf-8')}") 
        return None

    return response.json()

def set_custom_field(user_id, field_id, field_value):
    url = f"{MANICHAT_API_URL}/subscriber/setCustomField"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANICHAT_API_KEY}"}
    data = {
        "subscriber_id": user_id,
        "field_id": field_id,
        "field_value": field_value
    }

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    try:
        response = session.post(url, json=data, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error setting custom field: {e}")
        print(f"Status code: {response.status_code}")  
        print(f"Response content: {response.content.decode('utf-8')}") 
        return None

    return response.json()

def add_tag_by_name(user_id, tag_name):  
  url = f"{MANICHAT_API_URL}/subscriber/addTagByName"  
  headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANICHAT_API_KEY}"}  
  data = {  
  "subscriber_id": user_id,  
  "tag_name": tag_name  
  }  

  session = requests.Session()  
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])  
  adapter = HTTPAdapter(max_retries=retries)  
  session.mount('https://', adapter)  
  session.mount('http://', adapter)  

  try:  
  response = session.post(url, json=data, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=False)  
  response.raise_for_status()  
  except requests.exceptions.RequestException as e:  
  print(f"Error adding tag: {e}")  
  print(f"Status code: {response.status_code}")   
  print(f"Response content: {response.content.decode('utf-8')}")   
  return None  

  return response.json()  

def remove_tag_by_name(user_id, tag_name):  
  url = f"{MANICHAT_API_URL}/subscriber/removeTagByName"  
  headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANICHAT_API_KEY}"}  
  data = {  
  "subscriber_id": user_id,  
  "tag_name": tag_name  
  }  

  session = requests.Session()  
  retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])  
  adapter = HTTPAdapter(max_retries=retries)  
  session.mount('https://', adapter)  
  session.mount('http://', adapter)  

  try:  
  response = session.post(url, json=data, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=False)  
  response.raise_for_status()  
  except requests.exceptions.RequestException as e:  
  print(f"Error removing tag: {e}")  
  print(f"Status code: {response.status_code}")   
  print(f"Response content: {response.content.decode('utf-8')}")   
  return None  

  return response.json()  


def send_whatsapp(user_id, text, tag=None, tag_remove=None, callback_url=None, callback_timeout=None):
    url = f"{MANICHAT_API_URL}/sending/sendContent"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANICHAT_API_KEY_WHATSAPP}"}
    data = {
        "subscriber_id": user_id,
        "data": {
            "version": "v2",
            "content": {
                "type": "whatsapp",
                "messages": [
                    {
                        "type": "text",
                        "text": text
                    }
                ],
                "actions": [],
                "quick_replies": []
            }
        },
        "message_tag": "ACCOUNT_UPDATE"
    }

    if tag:
        add_tag_action = {
            "action": "add_tag",
            "tag_name": tag
        }
        data["data"]["content"]["actions"].append(add_tag_action)

    if tag_remove:
        remove_tag_action = {
            "action": "remove_tag",
            "tag_name": tag_remove
        }
        data["data"]["content"]["actions"].append(remove_tag_action)

    if callback_url:
        print(f"Sending message with tag: {tag}")
        external_message_callback = {
            "url": callback_url,
            "method": "post",
            "headers": {"Content-Type": "application/json"},
            "payload": {
                "id": user_id,
                "tag": "final_message_2",
                "message": text,
            }
        }
        if callback_timeout:
            external_message_callback["timeout"] = callback_timeout
        
        data["data"]["content"]["messages"][0]["external_message_callback"] = external_message_callback
        print(f"external_message_callback content: {external_message_callback}")

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    try:
        response = session.post(url, json=data, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        print(f"Status code: {response.status_code}")  
        print(f"Response content: {response.content.decode('utf-8')}") 
        return None

    return response.json()



def get_user_info(user_id):
    url = f"{MANICHAT_API_URL}/subscriber/getInfo"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {MANICHAT_API_KEY}"}
    params = {"subscriber_id": user_id}

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    try:
        response = session.get(url, params=params, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error getting user info: {e}") 
        return None

    print(f"Full response: {response.text}")
    return response.json()
