# utils.py

import re

def clean_phone_number(phone_number):
    """
    Удаляет все символы, кроме цифр, из строки с номером телефона.
    """
    return re.sub(r'\D', '', phone_number)

def truncate_text(text, max_length):
    """
    Обрезает текст до указанной длины и добавляет многоточие, если текст был обрезан.
    """
    if len(text) > max_length:
        return text[:max_length - 1] + "…"
    return text
