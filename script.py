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

    return random_repo['html_url']

def pocket_random():
    RSS_URL = 'http://getpocket.com/users/{}/feed/unread'
    res = requests.get(RSS_URL.format(os.getenv('POCKET_USERNAME')),
                 auth=requests.auth.HTTPBasicAuth(os.getenv('POCKET_USERNAME'),
                                                  os.getenv('POCKET_PASSWORD')))
    parsed = feedparser.parse(res.content)
    print(parsed)

gh_random = gh_random_repo()
p_random = pocket_random()

print(gh_random)
print(p_random)
