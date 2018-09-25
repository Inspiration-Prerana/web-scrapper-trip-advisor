import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
df = pd.read_csv('scrap_hotel.csv', sep='\t', encoding='utf-8')
saved_Link = df.Link
saved_name = df.Name
i = 0;
for url in saved_Link:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(saved_name[i])
    i = i + 1
    link_tags = soup.select('div a')
    for link_tag in link_tags:
        url = link_tag.get('href')
        print(url)
    # reviewContainer = soup.find_all(class_='review-container')
    # for container in reviewContainer:
    #
    #     profId = container.find(class_='avatar')
    #     print(profId.get('class'))
    #
    #     review = container.find(class_='ui_bubble_rating')
    #     print(review.get('class'))


