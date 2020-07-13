#!/usr/bin/env python3
import os

import requests

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
team_id = os.getenv('TEAM_ID')
mm_host = os.getenv('MM_HOST')
sc_key = os.getenv('SC_KEY')


def http_get(url, cookie):
    headers = {
        'authority': mm_host.split('//')[1],
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept-language': 'zh-CN',
        'user-agent': user_agent,
        'x-requested-with': 'XMLHttpRequest',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'cookie': cookie,
    }
    rsp = requests.get(url, headers=headers)
    if rsp.ok:
        return rsp.json()


def mention_count(cookie):
    count = 0
    url = '{}/api/v4/users/me/teams/unread'.format(mm_host)
    for item in http_get(url, cookie):
        count += item.get('mention_count', 0)
    url = mm_host + '/api/v4/users/me/teams/{}/channels?include_deleted=false'.format(team_id)
    for channel in http_get(url, cookie):
        if channel.get('type') == 'P':  # private channel
            url = mm_host + '/api/v4/users/me/channels/{}/unread'.format(channel.get("id"))
            count += http_get(url, cookie).get('mention_count', 0)
    return count


def send_notify(title, msg):
    requests.get('https://sc.ftqq.com/{}.send?text={}&desp={}'.format(sc_key, title, msg))


def main(cookie):
    try:
        count = mention_count(cookie)
    except Exception as exp:
        send_notify('Exception', str(exp))
    else:
        if count > 0:
            title = 'Notification from MM'
            msg = 'You have {} unread msg(s)'.format(count)
            send_notify(title, msg)


if __name__ == '__main__':
    main(os.getenv('MM_COOKIE'))
