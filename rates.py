import re
import requests
from bs4 import BeautifulSoup

supply_rates_url = 'https://www.eversource.com/content/residential/account-billing/manage-bill/about-your-bill/rates-tariffs/electric-supply-rates'
delivery_rates_url = 'https://www.eversource.com/content/residential/account-billing/manage-bill/about-your-bill/rates-tariffs/electric-delivery-rates'

def get_supply_rates():
    site = requests.get(supply_rates_url)
    soup = BeautifulSoup(site.content, 'html.parser')
    data = soup.select('#MainContentPlaceholder_TEF602CA6001_Col00 > div.cms > div > p:nth-child(2)')[0]
    name = 'Current Supply Rate'
    rate = float(re.findall('.\d+', data.string)[0])
    unit = '$/kWh'
    return [{'name': name, 'rate': rate, 'unit': unit}]


def get_delivery_rates():
    site = requests.get(delivery_rates_url)
    soup = BeautifulSoup(site.content, 'html.parser')
    rates = []
    for i in range(1, 7):
        item = soup.select(f'#MainContentPlaceholder_TEF602CA6001_Col00 > div:nth-child(4) > div > div > div > table > tbody > tr:nth-child({i}) > td:nth-child(1)')[0]
        data = soup.select(f'#MainContentPlaceholder_TEF602CA6001_Col00 > div:nth-child(4) > div > div > div > table > tbody > tr:nth-child({i}) > td:nth-child(2)')[0]
        name = item.string
        rate_per_unit = data.get_text()
        rate = float(re.findall('\d+.\d+', rate_per_unit)[0])
        unit = re.findall('\((.*?)\)', rate_per_unit)[0]
        rates.append({'name': name, 'rate': rate, 'unit': unit})
    return rates

rates = get_supply_rates() + get_delivery_rates()
for item in rates:
    print(f"{item['name']:<50} {item['rate']:<10} {item['unit']}")
