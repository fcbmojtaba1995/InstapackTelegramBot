from Instagram_API import functions as instagram_api
import functions as bot_functions
import urllib.parse
from Public import messages
import json
import jdatetime


# get user biography function
def get_biography(chat_id, user_id, message_id):
    biography = instagram_api.get_user_biography(username=bot_functions.get_last_username(user_id))
    bot_functions.send_chat_action(chat_id=chat_id, action='typing')
    bot_functions.send_message(chat_id=chat_id,
                               msg=urllib.parse.quote_plus(biography) + bot_functions.bot_address_caption,
                               parse_mode='HTML', reply_to_message_id=message_id)


# get user profile image
def get_user_profile(chat_id, user_id, message_id):
    profile_image_url = instagram_api.get_user_profile_image(username=bot_functions.get_last_username(user_id))
    bot_functions.send_chat_action(chat_id=chat_id, action='upload_photo')
    print("hi")
    bot_functions.send_photo(chat_id=chat_id, photo_link=urllib.parse.quote_plus(profile_image_url),
                             caption=bot_functions.bot_address_caption, parse_mode='HTML',
                             reply_to_message_id=message_id)


# get user posts function
def get_user_posts(chat_id, user_id):
    response = instagram_api.get_user_posts(username=bot_functions.get_last_username(user_id))
    if response is not None:
        if response == '400':
            bot_functions.send_chat_action(chat_id=chat_id, action='typing')
            bot_functions.send_message(chat_id=chat_id,
                                       msg=messages.page_is_private + bot_functions.bot_address_caption,
                                       parse_mode='HTML')

        elif response == '403':
            bot_functions.send_chat_action(chat_id=chat_id, action='typing')
            bot_functions.send_message(chat_id=chat_id, msg=messages.bot_not_work + bot_functions.bot_address_caption,
                                       parse_mode='HTML')

        else:
            parse_user_posts_response(chat_id, response)
    else:
        bot_functions.send_chat_action(chat_id=chat_id, action='typing')
        bot_functions.send_message(chat_id=chat_id,
                                   msg=messages.no_exist_post + bot_functions.bot_address_caption,
                                   parse_mode='HTML')


# show more user posts function
def show_more_user_posts(chat_id, user_id, next_max_id):
    response = instagram_api.show_more_post(user_id, next_max_id)
    if response is not None:
        if response == '400':
            bot_functions.send_chat_action(chat_id=chat_id, action='typing')
            bot_functions.send_message(chat_id=chat_id,
                                       msg=messages.page_is_private + bot_functions.bot_address_caption,
                                       parse_mode='HTML')

        elif response == '403':
            bot_functions.send_chat_action(chat_id=chat_id, action='typing')
            bot_functions.send_message(chat_id=chat_id, msg=messages.bot_not_work + bot_functions.bot_address_caption,
                                       parse_mode='HTML')

        else:
            parse_user_posts_response(chat_id, response)
    else:
        bot_functions.send_chat_action(chat_id=chat_id, action='typing')
        bot_functions.send_message(chat_id=chat_id,
                                   msg=messages.no_exist_post + bot_functions.bot_address_caption,
                                   parse_mode='HTML')


# parse user posts response function
def parse_user_posts_response(chat_id, response):
    posts = response['items']
    if len(posts) != 0:
        for post in posts:
            media_id = post['id']
            post_code = post['code']
            media_type = post['media_type']
            post_caption = post['caption']['text']
            user_id = post['user']['pk']
            if media_type == 1:  # send photo
                post_image_url = post['image_versions2']['candidates'][0]['url']
                markup, post_caption = check_more_available_and_caption_length(response, post,
                                                                               post_caption,
                                                                               post_code, media_id, user_id)

                bot_functions.send_chat_action(chat_id=chat_id, action='upload_photo')
                bot_functions.send_photo(chat_id=chat_id, photo_link=urllib.parse.quote_plus(post_image_url),
                                         caption=urllib.parse.quote_plus(
                                             post_caption) + bot_functions.bot_address_caption,
                                         parse_mode='HTML',
                                         markup=json.dumps(markup))

            elif media_type == 2:  # send video
                post_video_url = post['video_versions'][0]['url']
                markup, post_caption = check_more_available_and_caption_length(response, post,
                                                                               post_caption,
                                                                               post_code, media_id, user_id)

                bot_functions.send_chat_action(chat_id=chat_id, action='upload_video')
                bot_functions.send_video(chat_id=chat_id, video_link=urllib.parse.quote_plus(post_video_url),
                                         caption=urllib.parse.quote_plus(
                                             post_caption) + bot_functions.bot_address_caption,
                                         parse_mode='HTML',
                                         markup=json.dumps(markup))

            elif media_type == 8:  # send media album(photo or video or both)
                current_message_id = ''
                first_media = post['carousel_media'][0]
                media_type = first_media['media_type']

                if media_type == 1:  # send photo
                    post_image_url = first_media['image_versions2']['candidates'][0]['url']
                    markup, post_caption = check_more_available_and_caption_length(response, post,
                                                                                   post_caption,
                                                                                   post_code, media_id, user_id)

                    bot_functions.send_chat_action(chat_id=chat_id, action='upload_photo')
                    res = bot_functions.send_photo(chat_id=chat_id, photo_link=urllib.parse.quote_plus(post_image_url),
                                                   caption=urllib.parse.quote_plus(
                                                       post_caption) + bot_functions.bot_address_caption,
                                                   parse_mode='HTML',
                                                   markup=json.dumps(markup))
                    current_message_id = res['result']['message_id']

                elif media_type == 2:  # send video

                    post_video_url = first_media['video_versions'][0]['url']
                    markup, post_caption = check_more_available_and_caption_length(response, post,
                                                                                   post_caption,
                                                                                   post_code, media_id, user_id)

                    bot_functions.send_chat_action(chat_id=chat_id, action='upload_video')
                    res = bot_functions.send_video(chat_id=chat_id,
                                                   video_link=urllib.parse.quote_plus(post_video_url),
                                                   caption=urllib.parse.quote_plus(
                                                       post_caption) + bot_functions.bot_address_caption,
                                                   parse_mode='HTML',
                                                   markup=json.dumps(markup))
                    current_message_id = res['result']['message_id']

                other_media = post['carousel_media'][1:]
                other_media_array = []
                for media in other_media:
                    media_type = media['media_type']

                    if media_type == 1:  # photo
                        post_image_url = media['image_versions2']['candidates'][0]['url']
                        other_media_array.append(
                            {'type': 'photo', 'media': urllib.parse.quote(post_image_url)})

                    elif media_type == 2:  # video
                        post_video_url = media['video_versions'][0]['url']
                        other_media_array.append(
                            {'type': 'video', 'media': urllib.parse.quote(post_video_url)})

                bot_functions.send_chat_action(chat_id=chat_id, action='upload_document')
                bot_functions.send_media_group(chat_id=chat_id, media=json.dumps(other_media_array),
                                               reply_to_message_id=current_message_id)


# check more available flag and post caption text length function
def check_more_available_and_caption_length(response, post, post_caption, post_code, media_id, user_id):
    posts = response['items']
    more_available = response['more_available']
    if more_available and post == posts[-1]:  # posts[-1] : check last list element
        next_max_id = response['next_max_id']
        if len(post_caption) >= 1009:
            post_caption = post_caption[0:1005] + '...'
            markup = {'inline_keyboard': [
                [{'text': '\U0001F4E5 ' + 'مشاهده مشخصات پست',
                  'callback_data': 'show_post_info@{}'.format(media_id)}],
                [{'text': '\U0001F4E5 ' + 'مشاهده ادامه کپشن',
                  'callback_data': 'see_more_caption@{}'.format(media_id)}],
                [{'text': '\U0001F4E5 ' + 'مشاهده پست در اینستاگرام',
                  'url': 'https://instagram.com/p/{}'.format(post_code)}],
                [{'text': '\U0001F4E5 ' + 'نمایش پست های بیشتر',
                  'callback_data': 'show_more_posts@{}@{}'.format(user_id, next_max_id)}]]}
        else:
            markup = {'inline_keyboard': [
                [{'text': '\U0001F4E5 ' + 'مشاهده مشخصات پست',
                  'callback_data': 'show_post_info@{}'.format(media_id)}],
                [{'text': '\U0001F4E5 ' + 'مشاهده پست در اینستاگرام',
                  'url': 'https://instagram.com/p/{}'.format(post_code)}],
                [{'text': '\U0001F4E5 ' + 'نمایش پست های بیشتر',
                  'callback_data': 'show_more_posts@{}@{}'.format(user_id, next_max_id)}]]}
    else:
        if len(post_caption) >= 1009:
            post_caption = post_caption[0:1005] + '...'
            markup = {'inline_keyboard': [
                [{'text': '\U0001F4E5 ' + 'مشاهده مشخصات پست',
                  'callback_data': 'show_post_info@{}'.format(media_id)}],
                [{'text': '\U0001F4E5 ' + 'مشاهده ادامه کپشن',
                  'callback_data': 'see_more_caption@{}'.format(media_id)}],
                [{'text': '\U0001F4E5 ' + 'مشاهده پست در اینستاگرام',
                  'url': 'https://instagram.com/p/{}'.format(post_code)}]]}

        else:
            markup = {'inline_keyboard': [
                [{'text': '\U0001F4E5 ' + 'مشاهده مشخصات پست',
                  'callback_data': 'show_post_info@{}'.format(media_id)}],
                [{'text': '\U0001F4E5 ' + 'مشاهده پست در اینستاگرام',
                  'url': 'https://instagram.com/p/{}'.format(post_code)}]]}

    return markup, post_caption


# get user post info function
def get_user_post_info(callback_query_id, chat_id, media_id):
    response = instagram_api.get_user_posts_info(media_id)
    if response is not None:
        if response == '400':
            bot_functions.send_chat_action(chat_id=chat_id, action='typing')
            bot_functions.send_message(chat_id=chat_id,
                                       msg=messages.page_is_private + bot_functions.bot_address_caption,
                                       parse_mode='HTML')

        elif response == '403':
            bot_functions.send_chat_action(chat_id=chat_id, action='typing')
            bot_functions.send_message(chat_id=chat_id, msg=messages.bot_not_work + bot_functions.bot_address_caption,
                                       parse_mode='HTML')

        else:
            text = ''
            post = response['items'][0]
            like_count = post['like_count']
            comment_count = post['comment_count']
            post_sender = post['user']['username']
            media_type = post['media_type']
            created_at = post['taken_at']
            created_at = jdatetime.datetime.utcfromtimestamp(created_at).strftime('%H:%M:%S - %Y/%m/%d')

            if media_type == 1 or media_type == 8:
                text = '''\U0001F5E3 فرستنده پست: {}\n\U0001F5E3 تعداد لایک: {:,}\n\U0001F5E3 تعداد کامنت: {:,}\n\U0001F5E3 زمان ارسال پست: {}'''.format(
                    post_sender, like_count, comment_count, created_at)

            elif media_type == 2:
                view_count = post['view_count']
                text = '''\U0001F5E3 فرستنده پست: {}\n\U0001F5E3 تعداد لایک: {:,}\n\U0001F5E3 تعداد کامنت: {:,}\n\U0001F5E3 تعداد بیننده: {:,}\n\U0001F5E3 زمان ارسال پست: {}
                                        '''.format(post_sender, like_count, comment_count, view_count, created_at)

            bot_functions.answer_callback_query(query_id=callback_query_id, text=text, show_alert=True)


# see more caption function
def see_more_caption(chat_id, reply_to_message_id, media_id):
    response = instagram_api.get_user_posts_info(media_id)
    bot_functions.send_chat_action(chat_id=chat_id, action='typing')
    if response is not None:
        if response == '400':

            bot_functions.send_message(chat_id=chat_id,
                                       msg=messages.page_is_private + bot_functions.bot_address_caption,
                                       parse_mode='HTML')

        elif response == '403':

            bot_functions.send_message(chat_id=chat_id, msg=messages.bot_not_work + bot_functions.bot_address_caption,
                                       parse_mode='HTML')

        else:
            post_caption = response['items'][0]['caption']['text']
            bot_functions.send_message(chat_id=chat_id,
                                       msg=urllib.parse.quote_plus(post_caption) + bot_functions.bot_address_caption,
                                       parse_mode='HTML', reply_to_message_id=reply_to_message_id)
