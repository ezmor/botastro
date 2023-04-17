import requests
from config import GPT_API_KEY

API_URL = "https://api.openai.com/v1/engines/text-davinci-003/completions"

def generate_response(prompt, max_tokens=100):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GPT_API_KEY}",
    }

    data = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["text"].strip()
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return None

# webhook.py

from flask import Flask, request, jsonify
import json
from gpt_api import generate_response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    user_id = data["user_id"]
    message = data["message"]
    
    response_text = generate_response(message)
    
    if response_text:
        response_content = {
            "content": {
                "actions": [],
                "messages": [
                    {
                        "type": "text",
                        "text": response_text
                    }
                ],
                "quick_replies": []
            },
            "version": "v2"
        }
    else:
        response_content = {
            "content": {
                "actions": [],
                "messages": [
                    {
                        "type": "text",
                        "text": "Извините, я не смог обработать ваш запрос. Пожалуйста, попробуйте снова."
                    }
                ],
                "quick_replies": []
            },
            "version": "v2"
        }

    return jsonify(response_content)

if __name__ == '__main__':
    app.run()
