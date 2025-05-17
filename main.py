import requests
from bs4 import BeautifulSoup

def get_prices_from_page(page_number):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f'https://smartgo.su/catalog/smartfony/apple/?PAGEN_1={page_number}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:  # 200 означает успешный запрос
        soup = BeautifulSoup(response.text, 'html.parser')
        prices = soup.find_all('span', class_='price_value')
        cleaned_prices = []
        for price in prices:
            price_text = price.text.strip().replace('\xa0', '').replace(' ', '')
            cleaned_prices.append(float(price_text))
        return cleaned_prices
    else:
        print('Ошибка при получении страницы:', response.status_code)
        return []
all_prices = []
for page in range(1, 6):
    print(f'Получение цен со страницы {page}')
    prices = get_prices_from_page(page)
    all_prices.extend(prices)
for price in all_prices:
    print(price)
if all_prices:
    max_price = max(all_prices)
    min_price = min(all_prices)
    avg_price = sum(all_prices) / len(all_prices)
    print(f'\nМаксимальная цена: {max_price} ')
    print(f'Минимальная цена: {min_price} ')
    print(f'Средняя цена: {avg_price:.2f} ') 
else:
    # Если список цен пуст, выводим сообщение
    print('Цены не найдены.')
