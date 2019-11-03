import urllib3
import json
import config as db_config

api_token = '848398962:AAEgrgPTEHBNXnDiGBSaPGEGHlstSA9WvwE'

# Admin Bot Info
bot_name = "Insta Pack Bot"
bot_username = "@instapackbot"
bot_id = 848398962

bot_address_caption = "\n\n\U0001F916<a href='{}'>{}</a>".format('tg://user?id={}'.format(bot_id), bot_username)
base_url = 'https://api.telegram.org/bot{}/'.format(api_token)


def bot(method_name):
    response = urllib3.PoolManager().request(method='GET', url=base_url + method_name)
    return json.loads(response.data.decode('utf-8'))


def send_message(chat_id, msg, markup=None, parse_mode=None, disable_web_page_preview=True, reply_to_message_id=None):
    if parse_mode is not None:
        if markup is not None:

            bot(
                "sendMessage?chat_id={}&text={}&reply_markup={}&parse_mode={}&disable_web_page_preview={}&reply_to_message_id={}".format(
                    chat_id, msg, markup, parse_mode, disable_web_page_preview, reply_to_message_id))

        else:

            bot(
                "sendMessage?chat_id={}&text={}&parse_mode={}&disable_web_page_preview={}&reply_to_message_id={}".format(
                    chat_id, msg,
                    parse_mode,
                    disable_web_page_preview, reply_to_message_id))

    else:
        if markup is not None:

            bot("sendMessage?chat_id={}&text={}&reply_markup={}&disable_web_page_preview={}".format(chat_id, msg,
                                                                                                    markup,
                                                                                                    disable_web_page_preview))

        else:

            bot("sendMessage?chat_id={}&text={}&disable_web_page_preview={}".format(chat_id, msg,
                                                                                    disable_web_page_preview))


def forward_message(chat_id, from_chat_id, message_id):
    bot("forwardMessage?chat_id={}&from_chat_id={}&message_id={}".format(chat_id, from_chat_id, message_id))


def edit_message(chat_id, message_id, msg):
    bot("editMessageText?chat_id={}&message_id={}&text={}".format(chat_id, message_id, msg))


def delete_message(chat_id, message_id):
    bot("deleteMessage?chat_id={}&message_id={}".format(chat_id, message_id))


def send_photo(chat_id, photo_link, caption=None, parse_mode=None, markup=None, reply_to_message_id=None):
    if markup is not None:
        response = bot(
            "sendPhoto?chat_id={}&photo={}&caption={}&reply_markup={}&parse_mode={}&reply_to_message_id={}".format(
                chat_id, photo_link, caption, markup, parse_mode, reply_to_message_id))
    else:
        response = bot(
            "sendPhoto?chat_id={}&photo={}&caption={}&parse_mode={}&reply_to_message_id={}".format(
                chat_id, photo_link, caption, parse_mode, reply_to_message_id))
    return response


def edit_message_caption(chat_id, message_id):
    bot("editMessageReplyMarkup?chat_id={}&message_id={}".format(chat_id, message_id))


def send_video(chat_id, video_link, caption=None, parse_mode=None, markup=None):
    response = bot(
        "sendVideo?chat_id={}&video={}&caption={}&parse_mode={}&reply_markup={}&supports_streaming={}".format(chat_id,
                                                                                                              video_link,
                                                                                                              caption,
                                                                                                              parse_mode,
                                                                                                              markup,
                                                                                                              True))
    return response


def send_media_group(chat_id, media, reply_to_message_id):
    bot("sendMediaGroup?chat_id={}&media={}&reply_to_message_id={}".format(chat_id, media, reply_to_message_id))


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


def get_last_username(user_id):
    query = "select last_username from users WHERE user_id={}".format(user_id)
    db_config.cursor.execute(query)
    res = db_config.cursor.fetchall()
    return res[0][0]


def set_last_username(user_id, username):
    query = "UPDATE users SET last_username = (%s) WHERE user_id = (%s)"
    val = (username, user_id)
    db_config.cursor.execute(query, val)
    db_config.cnx.commit()


def get_last_message_id(user_id):
    query = "select last_message_id from users WHERE user_id={}".format(user_id)
    db_config.cursor.execute(query)
    res = db_config.cursor.fetchall()
    return res[0][0]


def set_last_message_id(user_id, message_id):
    query = "UPDATE users SET last_message_id = (%s) WHERE user_id = (%s)"
    val = (message_id, user_id)
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
