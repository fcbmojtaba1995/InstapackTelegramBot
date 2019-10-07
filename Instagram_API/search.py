import requests
import re
from Instagram_API import config


def get_user_pk(username):
    if re.match("^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$", username):
        url = 'https://i.instagram.com/api/v1/users/{}/usernameinfo/'.format(username)
        response = requests.get(url, headers=config.headers)
        print(response.json())
        status = response.json()['status']
        if status == 'ok':
            pk = response.json()['user']['pk']
            return pk
        else:
            return 'کاربر یافت نشد'
    else:
        return 'لطفا نام کاربری را به شکل صحیح وارد نمایید.'
