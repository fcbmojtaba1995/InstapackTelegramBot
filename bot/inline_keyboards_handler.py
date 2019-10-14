from Instagram_API import functions as instagram_api
import functions as bot_functions


def get_biography(chat_id, user_id):
    biography = instagram_api.get_user_biography(username=bot_functions.get_last_username(user_id))
    bot_functions.send_chat_action(chat_id=chat_id, action='typing')
    bot_functions.send_message(chat_id=chat_id,
                               msg=biography.replace('#', '') + bot_functions.bot_address_caption,
                               parse_mode='HTML')


def get_user_profile(chat_id, user_id):
    profile_image_url = instagram_api.get_user_profile_image(username=bot_functions.get_last_username(user_id))
    bot_functions.send_chat_action(chat_id=chat_id, action='upload_photo')
    bot_functions.send_photo(chat_id=chat_id, photo_link=profile_image_url,
                             caption=bot_functions.bot_address_caption, parse_mode='HTML')
