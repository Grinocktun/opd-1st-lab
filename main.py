# Импорт библиотеки requests для выполнения HTTP-запросов
import requests
# Импорт BeautifulSoup из библиотеки bs4 для парсинга HTML
from bs4 import BeautifulSoup


# Функция для получения цен со страницы каталога по номеру страницы
def get_prices_from_page(page_number):
    # Заголовки HTTP-запроса, чтобы сайт воспринимал нас как браузер, а не скрипт
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Формируем URL страницы с учетом номера страницы
    url = f'https://smartgo.su/catalog/smartfony/apple/?PAGEN_1={page_number}'

    # Отправляем GET-запрос к указанному URL с нашими заголовками
    response = requests.get(url, headers=headers)

    # Проверяем статус ответа сервера
    if response.status_code == 200:  # 200 означает успешный запрос
        # Создаем объект BeautifulSoup для парсинга HTML, используя встроенный парсер Python
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим все HTML-элементы span с классом 'price_value'
        prices = soup.find_all('span', class_='price_value')

        # Создаем список для хранения очищенных цен
        cleaned_prices = []
        # Перебираем все найденные элементы с ценами
        for price in prices:
            # Очищаем текст цены: удаляем пробелы, неразрывные пробелы (\xa0) и другие лишние символы
            price_text = price.text.strip().replace('\xa0', '').replace(' ', '')
            # Преобразуем очищенный текст в число с плавающей точкой и добавляем в список
            cleaned_prices.append(float(price_text))

        # Возвращаем список цен с текущей страницы
        return cleaned_prices
    else:
        # Если статус ответа не 200, выводим сообщение об ошибке
        print('Ошибка при получении страницы:', response.status_code)
        # Возвращаем пустой список, если не удалось получить данные
        return []


# Создаем основной список для хранения всех цен со всех страниц
all_prices = []

# Проходим по страницам с 1 по 5 (range(1,6) дает числа 1,2,3,4,5)
for page in range(1, 6):
    # Выводим информационное сообщение о текущей странице
    print(f'Получение цен со страницы {page}')
    # Получаем цены с текущей страницы
    prices = get_prices_from_page(page)
    # Добавляем полученные цены в общий список
    all_prices.extend(prices)

# Выводим все собранные цены по отдельности
for price in all_prices:
    print(price)

# Проверяем, что мы получили хотя бы одну цену
if all_prices:
    # Находим максимальную цену в списке
    max_price = max(all_prices)
    # Находим минимальную цену в списке
    min_price = min(all_prices)
    # Вычисляем среднюю цену (сумма всех цен деленная на их количество)
    avg_price = sum(all_prices) / len(all_prices)

    # Выводим результаты статистики
    print(f'\nМаксимальная цена: {max_price} ')
    print(f'Минимальная цена: {min_price} ')
    print(f'Средняя цена: {avg_price:.2f} ')  # Форматируем вывод средней цены до 2 знаков после запятой
else:
    # Если список цен пуст, выводим сообщение
    print('Цены не найдены.')