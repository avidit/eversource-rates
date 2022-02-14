import requests
from bs4 import BeautifulSoup

supply_rates_url = 'https://www.eversource.com/content/nh/residential/account-billing/manage-bill/about-your-bill/rates-tariffs/electric-supply-rates'
delivery_rates_url = 'https://www.eversource.com/content/nh/residential/account-billing/manage-bill/about-your-bill/rates-tariffs/electric-delivery-rates'


def get_supply_rates():
    site = requests.get(supply_rates_url)
    soup = BeautifulSoup(site.content, 'html.parser')
    data = soup.select('#Main_Main_C005_Col00 > div > p:nth-child(4) > strong')[0]
    name = 'Current Supply Rate'
    rate = float(data.string.split()[1])
    unit = '$/kWh'
    return [{'name': name, 'rate': rate, 'unit': unit}]


def get_delivery_rates():
    site = requests.get(delivery_rates_url)
    soup = BeautifulSoup(site.content, 'html.parser')
    rates = []
    for i in range(1, 7):
        item = soup.select(f'#Main_Main_C005_Col00 > div > div > div > table > tbody > tr:nth-child({i}) > td:nth-child(1)')[0]
        data = soup.select(f'#Main_Main_C005_Col00 > div > div > div > table > tbody > tr:nth-child({i}) > td:nth-child(2)')[0]
        name = item.string
        if i == 1:
            rate = float(data.text.split('\n')[0].replace('$', ''))
            unit = '$/month'
        else:
            rate = float(data.text.split('\n')[0].replace(' ', ''))
            unit = data.text.split('\n')[1].replace('(', '').replace(')', '').strip()
        rates.append({'name': name, 'rate': rate, 'unit': unit})
    return rates

rates = get_supply_rates() + get_delivery_rates()
for item in rates:
    print(f"{item['name']:<50} {item['rate']:<10} {item['unit']}")
