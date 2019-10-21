from Instagram_API import functions as instagram_api
import functions as bot_functions
import urllib.parse
from Public import messages
import json


def get_biography(chat_id, user_id):
    biography = instagram_api.get_user_biography(username=bot_functions.get_last_username(user_id))
    bot_functions.send_chat_action(chat_id=chat_id, action='typing')
    bot_functions.send_message(chat_id=chat_id,
                               msg=urllib.parse.quote_plus(biography) + bot_functions.bot_address_caption,
                               parse_mode='HTML')


def get_user_profile(chat_id, user_id):
    profile_image_url = instagram_api.get_user_profile_image(username=bot_functions.get_last_username(user_id))
    bot_functions.send_chat_action(chat_id=chat_id, action='upload_photo')
    bot_functions.send_photo(chat_id=chat_id, photo_link=profile_image_url,
                             caption=bot_functions.bot_address_caption, parse_mode='HTML')


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
            posts = response['items']
            more_available = response['more_available']
            # next_max_id = response['next_max_id']

            if len(posts) != 0:
                for post in posts:  # show 6 posts at per time
                    post_code = post['code']
                    media_type = post['media_type']
                    like_count = post['like_count']
                    comment_count = post['comment_count']
                    post_caption = post['caption']['text']
                    if media_type == 1:  # send photo
                        post_image_url = post['image_versions2']['candidates'][0]['url']
                        markup, post_caption = check_more_available_and_caption_length(more_available, post, posts,
                                                                                       post_caption,
                                                                                       post_code)

                        bot_functions.send_chat_action(chat_id=chat_id, action='upload_photo')
                        bot_functions.send_photo(chat_id=chat_id, photo_link=post_image_url,
                                                 caption=urllib.parse.quote_plus(
                                                     post_caption) + bot_functions.bot_address_caption,
                                                 parse_mode='HTML',
                                                 markup=json.dumps(markup))

                    elif media_type == 2:  # send video
                        view_count = post['view_count']
                        post_video_url = post['video_versions'][0]['url']
                        markup, post_caption = check_more_available_and_caption_length(more_available, post, posts,
                                                                                       post_caption,
                                                                                       post_code)

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
                            markup, post_caption = check_more_available_and_caption_length(more_available, post, posts,
                                                                                           post_caption,
                                                                                           post_code)

                            bot_functions.send_chat_action(chat_id=chat_id, action='upload_photo')
                            response = bot_functions.send_photo(chat_id=chat_id, photo_link=post_image_url,
                                                                caption=urllib.parse.quote_plus(
                                                                    post_caption) + bot_functions.bot_address_caption,
                                                                parse_mode='HTML',
                                                                markup=json.dumps(markup))
                            current_message_id = response['result']['message_id']

                        elif media_type == 2:  # send video

                            post_video_url = first_media['video_versions'][0]['url']
                            markup, post_caption = check_more_available_and_caption_length(more_available, post, posts,
                                                                                           post_caption,
                                                                                           post_code)

                            bot_functions.send_chat_action(chat_id=chat_id, action='upload_video')
                            response = bot_functions.send_video(chat_id=chat_id,
                                                                video_link=urllib.parse.quote_plus(post_video_url),
                                                                caption=urllib.parse.quote_plus(
                                                                    post_caption) + bot_functions.bot_address_caption,
                                                                parse_mode='HTML',
                                                                markup=json.dumps(markup))
                            current_message_id = response['result']['message_id']

                        other_media = post['carousel_media'][1:]
                        other_media_array = []
                        for media in other_media:
                            media_type = media['media_type']

                            if media_type == 1:  # photo
                                post_image_url = media['image_versions2']['candidates'][0]['url']
                                other_media_array.append(
                                    {'type': 'photo', 'media': urllib.parse.quote_plus(post_image_url)})

                            elif media_type == 2:  # video
                                post_video_url = media['video_versions'][0]['url']
                                other_media_array.append(
                                    {'type': 'video', 'media': urllib.parse.quote_plus(post_video_url)})

                        bot_functions.send_chat_action(chat_id=chat_id, action='upload_document')
                        bot_functions.send_media_group(chat_id=chat_id, media=json.dumps(other_media_array),
                                                       reply_to_message_id=current_message_id)

            else:
                bot_functions.send_chat_action(chat_id=chat_id, action='typing')
                bot_functions.send_message(chat_id=chat_id,
                                           msg=messages.no_exist_post + bot_functions.bot_address_caption,
                                           parse_mode='HTML')


def check_more_available_and_caption_length(more_available, post, posts, post_caption, post_code):
    if more_available and post == posts[-1]:  # posts[-1] : check last list element
        if len(post_caption) >= 1009:
            post_caption = post_caption[0:1005] + '...'
            markup = {'inline_keyboard': [
                [{'text': '\U0001F4E5 ' + 'مشاهده مشخصات پست',
                  'callback_data': 'show_post_detail'}],
                [{'text': '\U0001F4E5 ' + 'مشاهده ادامه کپشن',
                  'callback_data': 'see_more_caption'}],
                [{'text': '\U0001F4E5 ' + 'مشاهده پست در اینستاگرام',
                  'url': 'https://instagram.com/p/{}'.format(post_code)}],
                [{'text': '\U0001F4E5 ' + 'نمایش پست های بیشتر',
                  'callback_data': 'show_more_posts'}]]}
        else:
            markup = {'inline_keyboard': [
                [{'text': '\U0001F4E5 ' + 'مشاهده مشخصات پست',
                  'callback_data': 'show_post_detail'}],
                [{'text': '\U0001F4E5 ' + 'مشاهده پست در اینستاگرام',
                  'url': 'https://instagram.com/p/{}'.format(post_code)}],
                [{'text': '\U0001F4E5 ' + 'نمایش پست های بیشتر',
                  'callback_data': 'show_more_posts'}]]}
    else:
        if len(post_caption) >= 1009:
            post_caption = post_caption[0:1005] + '...'
            markup = {'inline_keyboard': [
                [{'text': '\U0001F4E5 ' + 'مشاهده مشخصات پست',
                  'callback_data': 'show_post_detail'}],
                [{'text': '\U0001F4E5 ' + 'مشاهده ادامه کپشن',
                  'callback_data': 'see_more_caption'}],
                [{'text': '\U0001F4E5 ' + 'مشاهده پست در اینستاگرام',
                  'url': 'https://instagram.com/p/{}'.format(post_code)}]]}

        else:
            markup = {'inline_keyboard': [
                [{'text': '\U0001F4E5 ' + 'مشاهده مشخصات پست',
                  'callback_data': 'show_post_detail'}],
                [{'text': '\U0001F4E5 ' + 'مشاهده پست در اینستاگرام',
                  'url': 'https://instagram.com/p/{}'.format(post_code)}]]}

    return markup, post_caption
