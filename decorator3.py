import types
from functools import wraps


def logger(path):
    import datetime
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            start_function = datetime.datetime.now()
            with open(f'{path}', 'a') as f:
                f.write(f'{start_function}\n {old_function.__name__}\n {args},  {kwargs}\n')
                res = old_function(*args, **kwargs)
                f.write(f'{res}\n')
                f.write(f'\n')
            return res

        return new_function

    return __logger


import requests
import bs4
from fake_headers import Headers
from pprint import pprint

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
HABR_URL = "https://habr.com/ru/articles/"


def get_fake_headers():
    return Headers(browser='chrome', os='win').generate()


@logger(r'C:\Users\yotal\Data\Iterator Generator\HW iter\dec3.log')
def get_article_info(article_url, keywords):
    response = requests.get(article_url, headers=get_fake_headers())
    article_soup = bs4.BeautifulSoup(response.text, features='lxml')

    text = article_soup.find('article', class_="tm-article-presenter__content").text.lower()
    if any(keyword in text for keyword in keywords):
        title = article_soup.find('h1').text
        time = article_soup.find('time')['datetime']
        return f'<{time[:10]} {time[11:19]}> – <{title}> – <{article_url}>'
    return None



def get_articles_with_keywords():
    response = requests.get(HABR_URL, headers=get_fake_headers())
    soup = bs4.BeautifulSoup(response.text, features='lxml')
    articles = soup.find_all('article', class_="tm-articles-list__item")

    unique_articles = set()
    for article in articles:
        article_url = "https://habr.com" + article.find('a', class_="tm-title__link")['href']
        article_info = get_article_info(article_url, KEYWORDS)
        if article_info:
            unique_articles.add(article_info)

    return unique_articles


parsed_data = get_articles_with_keywords()
pprint(parsed_data)
