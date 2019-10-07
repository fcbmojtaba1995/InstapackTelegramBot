import requests
import config as db_config
import json

api_token = '960175982:AAGLHQvIzlLv7iHksaWV6DR2soVlgPlb0Tk'

# Admin Bot Info
channel_id = "@nashenas_7learn"
bot_username = "file_shop_7learn_bot"
admin_user_id = 252519699
bot_directory = "http://fbf55e78.ngrok.io/telegram-bot-course/project3/"


def bot(data):
    res = requests.get("https://api.telegram.org/bot{}/{}".format(api_token, data))
    return res.json()


def send_message(chat_id, msg, markup=None, parse_mode=None):
    if parse_mode is not None:
        if markup is not None:

            bot("sendMessage?chat_id={}&text={}&reply_markup={}&parse_mode={}".format(chat_id, msg, markup, parse_mode))

        else:

            bot("sendMessage?chat_id={}&text={}&parse_mode={}".format(chat_id, msg, markup))

    else:
        if markup is not None:

            bot("sendMessage?chat_id={}&text={}&reply_markup={}".format(chat_id, msg, markup))

        else:

            bot("sendMessage?chat_id={}&text={}".format(chat_id, msg))


def forward_message(chat_id, from_chat_id, message_id):
    bot("forwardMessage?chat_id={}&from_chat_id={}&message_id={}".format(chat_id, from_chat_id, message_id))


def edit_message(chat_id, message_id, msg):
    bot("editMessageText?chat_id={}&message_id={}&text={}".format(chat_id, message_id, msg))


def delete_message(chat_id, message_id):
    bot("deleteMessage?chat_id={}&message_id={}".format(chat_id, message_id))


def send_photo(chat_id, photo_link, caption=None):
    bot("sendPhoto?chat_id={}&photo={}&caption={}".format(chat_id, photo_link, caption))


def send_video(chat_id, video_link, caption=None):
    bot("sendVideo?chat_id={}&video={}&caption={}".format(chat_id, video_link, caption))


def send_file(chat_id, file_id, caption=None):
    bot("sendDocument?chat_id={}&document={}&caption={}".format(chat_id, file_id, caption))


def send_chat_action(chat_id, action):
    bot("sendChatAction?chat_id={}&action={}".format(chat_id, action))


def answer_callback_query(query_id, text, show_alert=False):
    bot("answerCallbackQuery?callback_query_id={}&text={}&show_alert={}".format(query_id, text, show_alert))


def get_file_link(file_id):
    array = bot("getFile?file_id={}".format(file_id))
    link = "https://api.telegram.org/file/bot{}/".format(array['result']['file_path'])
    return link


def get_step(user_id):
    query = "select step from users WHERE user_id={}".format(user_id)
    db_config.cursor.execute(query)
    res = db_config.cursor.fetchall()
    return res['step']


def set_step(user_id, step):
    query = "UPDATE users SET step = (%s) WHERE user_id = (%s)"
    val = (step, user_id)
    db_config.cursor.execute(query, val)
    db_config.cnx.commit()


def get_admin_step(user_id):
    query = "select step from admin WHERE user_id={}".format(user_id)
    db_config.cursor.execute(query)
    res = db_config.cursor.fetchall()
    return res['step']


def set_admin_step(user_id, step):
    query = "update admin set step={} WHERE user_id={}".format(step, user_id)
    db_config.cursor.execute(query)
    db_config.cnx.commit()
    res = db_config.cursor.fetchall()
    return res


def get_user_by_username(username):
    query = "select * from users WHERE username={}".format(username)
    db_config.cursor.execute(query)
    res = db_config.cursor.fetchall()
    return res
