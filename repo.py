import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrap_repo(url):
    base_url = 'https://github.com'
    response= requests.get(url)
    topic_page = response.text
    topic_doc = BeautifulSoup(topic_page, 'html.parser')
    repo_tag = topic_doc.find_all('h3',class_ = 'f3 color-fg-muted text-normal lh-condensed')
    username = []
    repository = []
    user_link = []
    repo_link = []
    for tag in repo_tag:
        user_link.append(base_url+tag.find_all('a')[0]['href'].strip())
        repo_link.append(base_url+tag.find_all('a')[1]['href'].strip())
        username.append(tag.find_all('a')[0].text.strip())
        repository.append(tag.find_all('a')[1].text.strip())
    star_tag = topic_doc.find_all('span',{'id' : "repo-stars-counter-star"})
    stars = []
    for tag in star_tag:
        star = tag['title']
        star = int(star.replace(',',''))
        stars.append(star)
    dict = {
        'Username':username,
        'User Link':user_link,
        'Repository': repository,
        'Repository Link':repo_link,
        'Stars': stars
    }
    df = pd.DataFrame(dict)
    return df
