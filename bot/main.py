import requests
import json
from flask import Flask, request, Response
import config as db_config
import functions as bot_functions
import messages

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        update = request.get_json()
        parse_update(update)

        return Response('ok', status=200)

    else:
        return '<h1>Insta Pack Telegram Bot</h1>'


def parse_update(update):
    if 'message' in update:

        user_id = update['message']['from']['id']
        chat_id = update['message']['chat']['id']
        message_id = update['message']['message_id']
        username = update['message']['from']['username'] if 'username' in update['message']['from'] else None
        first_name = update['message']['from']['first_name']
        last_name = update['message']['from']['last_name'] if 'last_name' in update['message']['from'] else None
        text = update['message']['text']
        handle_user_message(chat_id, user_id, first_name, last_name, username, text)

    elif 'callback_query' in update:

        callback_id = update['callback_query']['id']
        user_id = update['callback_query']['from']['id']
        chat_id = update['callback_query']['message']['chat']['id']
        message_id = update['callback_query']['message']['message_id']
        username = update['callback_query']['from']['username'] if 'username' in update['callback_query'][
            'from'] else None
        first_name = update['callback_query']['from']['first_name']
        last_name = update['callback_query']['from']['last_name'] if 'last_name' in update['callback_query'][
            'from'] else None
        text = update['callback_query']['data']


def handle_user_message(chat_id, user_id, first_name, last_name, username, text):
    if text == '/start':
        start_command_handler(chat_id, user_id, first_name, last_name, username)
    else:
        pass


# Start Command Handler Function
def start_command_handler(chat_id, user_id, first_name, last_name, username):
    bot_functions.send_chat_action(chat_id=chat_id, action='typing')
    query = "select * from users WHERE user_id={}".format(user_id)
    db_config.cursor.execute(query)
    result = db_config.cursor.fetchall()
    row_number = len(result)
    if row_number == 0:
        query = "INSERT INTO users(user_id,first_name,last_name,username,step) VALUES (%s, %s, %s, %s, %s)"
        val = (user_id, first_name, last_name, username, 'home')
        db_config.cursor.execute(query, val)
        db_config.cnx.commit()

    bot_functions.send_message(chat_id=chat_id, msg=messages.welcome_msg)
    bot_functions.set_step(user_id, 'home')


if __name__ == '__main__':
    db_config.connect_to_database()
    app.run(debug=True)
