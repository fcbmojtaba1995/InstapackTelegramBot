import json
from flask import Flask, request, Response
import config as db_config
import functions as bot_functions
import inline_keyboards_handler
from Public import messages
from Instagram_API import functions as instagram_api
import urllib.parse

# setup flask and index page
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        update = request.get_json()
        parse_update(update)

        return Response('ok', status=200)

    else:
        return '<h1>Insta Pack Telegram Bot</h1>'


# parse received update function
def parse_update(update):
    if 'message' in update:

        user_id = update['message']['from']['id']
        chat_id = update['message']['chat']['id']
        message_id = update['message']['message_id']
        username = update['message']['from']['username'] if 'username' in update['message']['from'] else None
        first_name = update['message']['from']['first_name']
        last_name = update['message']['from']['last_name'] if 'last_name' in update['message']['from'] else None
        text = update['message']['text']
        user_command_handler(chat_id, user_id, message_id, first_name, last_name, username, text)

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
        inline_keyboard_handler(chat_id, user_id, text)


# User Command Handler Function
def user_command_handler(chat_id, user_id, message_id, first_name, last_name, username, text):
    if text == '/start':
        start_command_handler(chat_id, user_id, first_name, last_name, username)
    elif text == '/help':
        pass
    else:
        edit_prev_message(chat_id, bot_functions.get_last_message_id(user_id))
        bot_functions.set_last_message_id(user_id, message_id)
        username_command_handler(chat_id, user_id, text)


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

    bot_functions.send_message(chat_id=chat_id, msg=messages.welcome_msg, parse_mode='HTML')


# enter instagram username by user (command) handler function
def username_command_handler(chat_id, user_id, text):
    if '@' in str(text):
        at_sign_char_index = str(text).index('@')
        if at_sign_char_index == 0:
            text = text[1:]
    if 'https://instagram.com/' in str(text):
        url_char_index = str(text).index('https://instagram.com/')
        if url_char_index == 0:
            text = text[22:]

    bot_functions.set_last_username(user_id, text)
    username_info = instagram_api.get_username_info(text)

    if username_info is not None:

        if username_info == '404':  # 404 mean : user not found
            bot_functions.send_chat_action(chat_id=chat_id, action='typing')
            bot_functions.send_message(chat_id=chat_id, msg=messages.user_not_found + bot_functions.bot_address_caption,
                                       parse_mode='HTML')

        elif username_info == '401':  # 401 mean : wrong input
            bot_functions.send_chat_action(chat_id=chat_id, action='typing')
            bot_functions.send_message(chat_id=chat_id, msg=messages.wrong_input + bot_functions.bot_address_caption,
                                       parse_mode='HTML')

        elif username_info == '403':  # 403 mean : login required (the problem is ours : cookies is expired)
            bot_functions.send_chat_action(chat_id=chat_id, action='typing')
            bot_functions.send_message(chat_id=chat_id, msg=messages.bot_not_work + bot_functions.bot_address_caption,
                                       parse_mode='HTML')

        else:
            full_name = username_info['full_name']
            username = username_info['username']
            media_count = username_info['media_count']
            follower_count = username_info['follower_count']
            following_count = username_info['following_count']

            is_private = username_info['is_private']
            if is_private:
                page_status = 'قفل (Private)'
            else:
                page_status = 'باز (Public)'

            biography = username_info['biography']
            external_url = username_info['external_url']

            caption = '''\U0001F5E3 <b>نام نمایشی: </b>{}
            
\U0001F464 <b>نام کاربری: </b>{}

\U0001F4E5 <b>تعداد پست: </b>{:,}

\N{leftwards black arrow} <b>تعداد فالوور: </b>{:,}

\N{black rightwards arrow} <b>تعداد فالووینگ: </b>{:,}

\N{lock} <b>وضعیت صفحه: </b>{}

\U0001F4DC <b>بیوگرافی:</b>
{}

\U0001F517 <b>لینک:</b>

<a href='{}'>{}</a>
'''.format(full_name, username, media_count, follower_count, following_count, page_status,
           urllib.parse.quote_plus(biography),
           external_url, external_url) + bot_functions.bot_address_caption

            markup = {'inline_keyboard': [[{'text': '\U0001F4E5 ' + 'بیوگرافی', 'callback_data': 'get_biography'},
                                           {'text': '\U0001F4E5 ' + 'عکس پروفایل',
                                            'callback_data': 'get_user_profile'}],
                                          [{'text': '\U0001F4E5 ' + 'هایلایت ها', 'callback_data': 'get_highlights'},
                                           {'text': '\U0001F4E5 ' + 'استوری ها', 'callback_data': 'get_stories'},
                                           {'text': '\U0001F4E5 ' + 'پست ها', 'callback_data': 'get_posts'}],
                                          [{'text': '\U0001F4E5 ' + 'مشاهده صفحه در اینستاگرام',
                                            'url': 'https://instagram.com/{}'.format(text)}]]}

            bot_functions.send_chat_action(chat_id=chat_id, action='upload_photo')
            response = bot_functions.send_photo(chat_id=chat_id,
                                                photo_link=username_info['hd_profile_pic_url_info']['url'],
                                                caption=caption, parse_mode='HTML', markup=json.dumps(markup))
            message_id = response['result']['message_id']
            bot_functions.set_last_message_id(user_id, message_id)


# edit previous message (with inline keyboard) and remove keyboard function
def edit_prev_message(chat_id, message_id):
    bot_functions.edit_message_caption(chat_id=chat_id, message_id=message_id)


# inline keyboard handler function
def inline_keyboard_handler(chat_id, user_id, text):
    if text == 'get_biography':
        inline_keyboards_handler.get_biography(chat_id, user_id)

    elif text == 'get_user_profile':
        inline_keyboards_handler.get_user_profile(chat_id, user_id)

    elif text == 'get_highlights':
        pass

    elif text == 'get_stories':
        pass

    elif text == 'get_posts':
        inline_keyboards_handler.get_user_posts(chat_id, user_id)

    elif text == 'show_page':
        pass


if __name__ == '__main__':
    db_config.connect_to_database()
    app.run(debug=True)
