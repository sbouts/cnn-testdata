import requests
from bs4 import BeautifulSoup
import re

# Make a request to https://lite.cnn.com
url = "https://lite.cnn.com"
req = requests.get(url)
# print(req.text)

# PARSE LINKS
soup = BeautifulSoup(req.content, 'html.parser')
# print(soup)

parent = soup.find('ul')
# print(parent)

for li in parent.find_all('li'):
    ref = li.find('a')
    link = ref.get('href')
    # print(f'{url}{link}')

    article = requests.get(f'{url}{link}')
    article_soup = BeautifulSoup(article.content, 'html.parser')
    # HEADER
    try:
        section = article_soup.find('h2', {'class': 'headline'}).text
        # replace all spaces in variable section with underscore
        section = f'cnn_{section.lower().replace(" ", "_")}'
        section = re.sub(r'\W+', '', section)
        

        article_text = article_soup.find_all('article')
        news = article_text[0].text
        # print(news)
        #write the variable news to a file
        with open(f'scraped/{section}.txt', 'w') as f:
            f.write(news)
    except Exception as e:
        print(f'{url}{link}')
        print(e)
