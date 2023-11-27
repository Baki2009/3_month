from bs4 import BeautifulSoup
import requests

def parsing_akiexpress():
    url = "https://akipress.org/"
    response = requests.get(url=url)
    # print(response)
    # print(response.text)

    soup = BeautifulSoup(response.text, "lxml")
    # print(soup)
    all_news = soup.find_all('a', class_="newslink")
    print(all_news)
    n = 0
    for news in all_news:
        n += 1
        print(f"{n}){news.text}")

def parsing_sulpak():
    url = 'https://www.sulpak.kg/f/smartfoniy/osh/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    all_phones = soup.find_all('div', class_='product__item-name')
    all_prices = soup.find_all('div', class_='product__item-price')
    all_pictures = soup.find_all('img', class_='image-size-cls')
    # print(all_pictures)
    for image in all_pictures:
        result = image['src'].split("/")[-1].split("_")
        print(result[0])
    for name, price in zip(all_phones, all_prices):
        current_price = "".join(price.text.split())
        print(name.text, current_price)

parsing_sulpak()