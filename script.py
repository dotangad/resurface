import datetime
import feedparser
import os
import random
import re
import requests
from config import POCKET_USERNAME, POCKET_PASSWORD, TG_BOT_TOKEN, TG_CHAT_ID

def total_stars(res):
    link_header = res.headers['Link']
    # <https://api.github.com/user/30556800/starred?page=2>; rel="next",
    # <https://api.github.com/user/30556800/starred?page=38>; rel="last"
    return int(link_header[link_header.rfind("page=") + 5:-13])

def random_repo(res, API_URL):
    random_repo_n = random.randint(1, total_stars(res))
    random_repo = requests.get(
        API_URL.format(f"starred?per_page=1&page={random_repo_n}")
    ).json()[0]

def gh_random_repo():
    API_URL = 'https://api.github.com/users/ChristianChiarulli/{}'

    res = requests.get(API_URL.format("starred?per_page=1"))
    rr = random_repo(res, API_URL)

    return rr['full_name'], rr['html_url']

def pocket_random():
    RSS_URL = 'http://getpocket.com/users/{}/feed/unread'
    res = requests.get(RSS_URL.format(POCKET_USERNAME),
                 auth=requests.auth.HTTPBasicAuth(POCKET_USERNAME,
                                                  POCKET_PASSWORD))
    parsed = feedparser.parse(res.content)['entries']
    rnd = parsed[random.randint(0, len(parsed) - 1)]
    return rnd['title'], rnd['link']

# links = [['link title', 'link href']]
def send_telegram_message(links):
    bot_token = TG_BOT_TOKEN
    today = datetime.date.today().strftime("%A, %d %b %Y")
    API_URL = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    links_html = '\n'.join([f'<a href="{link[0]}">{link[1]}</a>' for link in links])

    res = requests.post(API_URL, {
        'chat_id': TG_CHAT_ID,
        'text': f'<strong>{today}</strong>\n' +
                links_html,
        'parse_mode': "HTML",
        'disable_web_page_preview': 'true',
    })

    print(res.content)

gh_title, gh_link = gh_random_repo()
pocket_title, pocket_link = pocket_random()

# send_telegram_message([[gh_title, gh_link], [pocket_title, pocket_link]])
print(gh_title, gh_link)
