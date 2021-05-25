import datetime
import feedparser
import os
import random
import re
import requests
from dotenv import load_dotenv

load_dotenv()

def gh_random_repo():
    API_URL = 'https://api.github.com/users/dotangad/{}'

    res = requests.get(API_URL.format("starred"))
    link_header = res.headers['Link']
    last_page = int(
        re.compile('\d+').findall(
            re.compile('page=\d+>; rel="last"').findall(link_header)[0]
        )[0]
    )

    random_page = random.randint(1, last_page)

    res = requests.get(API_URL.format(f"starred?page={random_page}"))
    res_json = res.json()
    random_repo = res_json[random.randint(0, len(res_json) - 1)]

    return random_repo['full_name'], random_repo['html_url']

def pocket_random():
    RSS_URL = 'http://getpocket.com/users/{}/feed/unread'
    res = requests.get(RSS_URL.format(os.getenv('POCKET_USERNAME')),
                 auth=requests.auth.HTTPBasicAuth(os.getenv('POCKET_USERNAME'),
                                                  os.getenv('POCKET_PASSWORD')))
    parsed = feedparser.parse(res.content)['entries']
    rnd = parsed[random.randint(0, len(parsed) - 1)]
    return rnd['title'], rnd['link']

# links = [['link title', 'link href']]
def send_telegram_message(links):
    bot_token = os.getenv("TG_BOT_TOKEN")
    today = datetime.date.today().strftime("%A, %d %b %Y")
    API_URL = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    links_html = '\n'.join([f'<a href="{link[0]}">{link[1]}</a>' for link in links])

    res = requests.post(API_URL, {
        'chat_id': os.getenv("TG_CHAT_ID"),
        'text': f'<strong>{today}</strong>\n' +
                links_html,
        'parse_mode': "HTML",
        'disable_web_page_preview': 'true',
    })

    print(res.content)

gh_title, gh_link = gh_random_repo()
pocket_title, pocket_link = pocket_random()

send_telegram_message([[gh_title, gh_link], [pocket_title, pocket_link]])
