# config.py

# API ключи
MANICHAT_API_KEY = "106153512442485:3fada7a2f914d2760f8afb2c3effb0fb"
GPT_API_KEY = "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"

# URL для отправки данных клиента в CRM
CRM_POST_URL = "https://your_crm_url.com/api/create_order"

# Настройки диалога
WELCOME_MESSAGE = "Здравствуйте, я астролог-ясновидящая. Как могу помочь вам сегодня?"
AMULET_PROMPT = "Хотите узнать больше об амулете? Нажмите на кнопку ниже."
AMULET_MORE_INFO = "Амулет помогает привлечь удачу, успех и счастье. Если вы заинтересованы, мне понадобятся ваше имя и номер телефона для оформления заказа."
PHONE_PROMPT = "Пожалуйста, введите ваш номер телефона:"
NAME_PROMPT = "Пожалуйста, введите ваше имя:"
THANK_YOU_MESSAGE = "Спасибо за предоставленную информацию. Ваш заказ принят. Мы свяжемся с вами в ближайшее время."

# Настройки статистики
STATS_FILE = "dialogue_statistics.json"

# Таймаут между запросами к GPT-API и ManyChat API
REQUEST_TIMEOUT = 2
