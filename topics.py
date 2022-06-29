import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrap_topics(number):
    base_site = 'https://github.com/topics'
    total = int(number/30)
    topic_titles = []
    topic_descs = []
    topic_url_list = []
    for i in range(total):
        page = '?page='+str(i+1)
        site = base_site+page
        req = requests.get(site)
        page_content = req.text
        doc = BeautifulSoup(page_content, "html.parser")
        # getting topic title
        selection_class = "f3 lh-condensed mb-0 mt-1 Link--primary"
        topic_title_tag =  doc.find_all('p',class_ = selection_class)
        for tag in topic_title_tag:
            topic_titles.append(tag.text)
        # getting topic description
        selection_class = "f5 color-fg-muted mb-0 mt-1"
        topic_desc_tag = doc.find_all('p',class_ = selection_class)
        for desc in topic_desc_tag:
            topic_descs.append(desc.text.strip())

        # getting topic links
        selection_class = "no-underline flex-1 d-flex flex-column"
        topic_url_tag = doc.find_all('a',class_ = selection_class)
        base_url = 'https://github.com'
        for i in range(len(topic_url_tag)):
            href = topic_url_tag[i]['href']
            topic_url = base_url + href
            topic_url_list.append(topic_url)
        
    # creating dataframe    
    dict = {
        'topic':topic_titles,
        'description': topic_descs,
        'url' : topic_url_list,
    }
    topic_df = pd.DataFrame(dict)
    return topic_df  