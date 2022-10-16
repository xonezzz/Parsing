from bs4 import BeautifulSoup as BS
import requests
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_soup(html):
    soup = BS(html)
    return soup

def get_data(soup):
    catalog = soup.find('div' ,class_='table-view-list')
    cars = catalog.find_all('div' ,class_="list-item list-label")
    
    for car in cars:
        
        try:
            title = car.find('h2', class_='name').text.strip()
        except AttributeError:
            title = 'Названия отсуствует'
        try:
            prices = car.find('div', class_='block price').find('p').text
            prices_join = ''.join([price for price in prices if price != ' ']).replace('\n', ' ').split()
            price = ', '.join(prices_join)
        except AttributeError:
            price = '0'
        try:
            images = car.find_all('img', class_='lazy-image')
            image = ' ; '.join([img.get('data-src') for img in images])
        except AttributeError:
            image = 'Фото отсуствует'
        try:
            descriptions = car.find('div', class_='block info-wrapper item-info-wrapper').text.replace(' ', '')
            descriptions_join = ''.join([i for i in descriptions]).replace('\n', ' ').split()
            description = ','.join(descriptions_join)
        except AttributeError:
            description = 'Описание отсуствует'
       
        write_csv({
            'title': title,
            'price': price,
            'image': image,
            'description': description
        })


def write_csv(data):
    with open('cars.csv', 'a') as file:
        names = ['title', 'price', 'description', 'image']
        write = csv.DictWriter(file, delimiter=',', fieldnames=names)
        write.writerow(data)

def main():
        try:
            for i in range(1, 2000):
                BASE_URL = f'https://www.mashina.kg/search/?currency=2&price_from=&price_to=&page={i}'
                html = get_html(BASE_URL)
                soup = get_soup(html)
                get_data(soup)
                print(f'Вы спарсили - {i} страницу')
        except:
            print('Это была последняя странца')

if __name__ == '__main__':
    main()