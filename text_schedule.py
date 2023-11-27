import schedule, time, requests

def hello_world():
    print("Hello world", time.ctime())

def alert_lesson():
    print("Здравсвуйте, сегодня у вас урок в 18:00")

def get_btc_price():
    url = "https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url=url).json()
    price = round(float(response['price']), 3)
    print(f"Цена Биткоина {price} USD")

def parsing_sulpak():
    from bs4 import BeautifulSoup
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

# schedule.every(5).seconds.do(hello_world)
# schedule.every(1).minutes.do(hello_world)
# schedule.every().day.at("18:34").do(hello_world)
# schedule.every().monday.at("18:36").do(hello_world)
# schedule.every().monday.at("18:39").do(alert_lesson)
# schedule.every().hours.at(":42").do(alert_lesson)
# schedule.every(3).seconds.do(get_btc_price)
schedule.every(15).seconds.do(parsing_sulpak)

while True:
    schedule.run_pending()