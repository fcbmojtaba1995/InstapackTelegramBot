import re
import urllib3
from Instagram_API import config
import json

base_url = 'https://i.instagram.com/api/v1/'


# get user info function
def get_username_info(username):
    if re.match("^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$", username):
        url = base_url + 'users/{}/usernameinfo/'.format(username)
        response = urllib3.PoolManager().request(method='POST', url=url, headers=config.headers)

        if response.status == 200:  # 200 mean : request ok and user founded
            user_info = json.loads(response.data.decode('utf-8'))['user']
            return user_info

        elif response.status == 403:  # 403 mean : login required (the problem is ours : cookies is expired)
            return '403'

        elif response.status == 404:
            return '404'  # 404 mean : user not found

    else:
        return '401'  # 401 mean : wrong input


# get user biography function
def get_user_biography(username):
    username_info = get_username_info(username)
    biography = username_info['biography']
    return biography


# get user profile image function
def get_user_profile_image(username):
    username_info = get_username_info(username)
    profile_image_url = username_info['hd_profile_pic_url_info']['url']
    return profile_image_url


# get user id (pk) function
def get_user_id(username):
    username_info = get_username_info(username)
    user_id = username_info['pk']
    return user_id


# get user posts function
def get_user_posts(username):
    username_info = get_username_info(username)
    user_id = username_info['pk']
    url = base_url + 'feed/user/{}/'.format(user_id)
    response = urllib3.PoolManager().request(method='POST', url=url, headers=config.headers)

    if response.status == 200:  # 200 mean : request ok and user founded
        return json.loads(response.data.decode('utf-8'))

    elif response.status == 400:
        return '400'  # 400 mean : not authorized to view user(page is private)

    elif response.status == 403:  # 403 mean : login required (the problem is ours : cookies is expired)
        return '403'


# show more post function
def show_more_post(user_id, next_max_id):
    url = base_url + 'feed/user/{}?max_id={}'.format(user_id, next_max_id)
    response = urllib3.PoolManager().request(method='POST', url=url, headers=config.headers)

    if response.status == 200:  # 200 mean : request ok and user founded
        return json.loads(response.data.decode('utf-8'))

    elif response.status == 400:
        return '400'  # 400 mean : not authorized to view user(page is private)

    elif response.status == 403:  # 403 mean : login required (the problem is ours : cookies is expired)
        return '403'


# get user posts info function
def get_user_posts_info(media_id):
    url = base_url + 'media/{}/info'.format(media_id)
    response = urllib3.PoolManager().request(method='GET', url=url, headers=config.headers)
    if response.status == 200:  # 200 mean : request ok and user founded
        return json.loads(response.data.decode('utf-8'))

    elif response.status == 400:
        return '400'  # 400 mean : not authorized to view user(page is private)

    elif response.status == 403:  # 403 mean : login required (the problem is ours : cookies is expired)
        return '403'
