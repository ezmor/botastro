# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import dialogue_script as ds
import astro_whatsapp_dialogue_script as awds
import dialogue_script_fit_ro_message as dsfrm
import database_utils
import database_utils_fit_ro_mess
import logging
import simplejson as json




logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.json_encoder = json.JSONEncoder

@app.route('/message', methods=['POST'])
def handle_message_endpoint():
    data = request.get_json()
    user_id = data['user_id']
    message = data['message']

    database_utils.add_message(user_id, 'user', message)

    tag = get_tag(data)
    response = ds.handle_message(user_id, message, tag)

    if response is None:
        response = ""
        
    logging.debug(f"Calling add_message: user_id={user_id}, role='assistant', content={response}")
    database_utils.add_message(user_id, 'assistant', response)

    return jsonify({"version":"v2","content":{"messages":[{"type":"text","text":response}]}})


@app.route('/astro_whatsapp', methods=['POST'])
def astro_whatsapp_endpoint():
    data = request.get_json()
    user_id = data['user_id']
    message = data['message']

    database_utils.add_message(user_id, 'user', message)

    tag = get_tag(data)
    response = awds.astro_whatsapp(user_id, message, tag)

    if response is None:
        response = ""
        
    logging.debug(f"Calling add_message: user_id={user_id}, role='assistant', content={response}")
    database_utils.add_message(user_id, 'assistant', response)

    return jsonify({"version":"v2","content":{"messages":[{"type":"text","text":response}]}})


@app.route('/fit_ro_message', methods=['POST'])
def fit_ro_message_endpoint():
    data = request.get_json()
    user_id = data['user_id']
    message = data.get('message', '')  # Используйте метод get() для получения сообщения. Если сообщение отсутствует, используйте '' как значение по умолчанию.

    if message.strip():
        database_utils_fit_ro_mess.add_message(user_id, 'user', message)

    tag = get_tag(data)
    response = dsfrm.fit_ro_message(user_id, message, tag)

    if response is None:
        response = ""
        
    logging.debug(f"Calling add_message: user_id={user_id}, role='assistant', content={response}")
    database_utils_fit_ro_mess.add_message(user_id, 'assistant', response)

    return jsonify({"version":"v2","content":{"messages":[{"type":"text","text":response}]}})


def get_tag(data):
    return data.get('tag', 'unknown')


if __name__ == '__main__':
    app.run(debug=True)
