# -*- coding: utf-8 -*-
import os
import openai
import requests
import logging
from config import GPT_API_KEY
import ast
import json

API_URL = "https://api.openai.com/v1/completions"

openai.api_key = GPT_API_KEY

def generate_response(prompt, max_tokens=50, temperature=1.0, top_p=1, n=1):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=None,
        temperature=temperature,
        top_p=top_p,
    )

    generated_text = response.choices[0].text.strip()
    return generated_text

def generate_analyze_horoscope_response(problem, horoscope_text):
    prompt = f"Проанализируйте гороскоп пользователя: {horoscope_text}. Ответьте на вопрос пользователя: {problem}."
    response_text = generate_response(prompt)
    return response_text


def generate_response_with_variables(prompt_template, max_tokens=500, temperature=0.7, top_p=1, n=1, presence_penalty=0.6, **kwargs):
    prompt = prompt_template.format(**kwargs)
    start_sequence = "\nAI:"
    restart_sequence = "\nHuman: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=[" Human:", " AI:"],
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=0,
        presence_penalty=presence_penalty,

    )

    generated_text = response.choices[0].text.strip()
    print("API Response:", response.choices[0].text)
    return generated_text


def generate_response_with_variables_turbo(prompt_template, system_role="You are a helpful assistant.", max_tokens=150, temperature=0.7, top_p=1, n=1, presence_penalty=0.6, **kwargs):
    prompt = prompt_template.format(**kwargs)
    user_message = {"role": "assistant", "content": prompt}
    system_message = {"role": "system", "content": system_role}
    messages = [system_message, user_message]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        n=n,
        stop=[""],
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=0,
        presence_penalty=presence_penalty,
        max_tokens=max_tokens
    )

    generated_text = response.choices[0].message['content'].strip()
    print("API Response:", response.choices[0].message['content'])
    return generated_text


def generate_response_with_variables_gpt4(prompt_template, system_role="You are a helpful assistant.", max_tokens=150, temperature=0.7, top_p=1, n=1, presence_penalty=0.6, **kwargs):
    prompt = prompt_template.format(**kwargs)
    user_message = {"role": "assistant", "content": prompt}
    system_message = {"role": "system", "content": system_role}
    messages = [system_message, user_message]

    response = openai.ChatCompletion.create(
        model="gpt-4-0314",
        messages=messages,
        n=n,
        stop=[" Human:", " AI:"],
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=0,
        presence_penalty=presence_penalty,
        max_tokens=max_tokens
    )

    generated_text = response.choices[0].message['content'].strip()
    print("API Response:", response.choices[0].message['content'])
    return generated_text

