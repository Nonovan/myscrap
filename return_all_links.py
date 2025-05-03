import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
 
def get_links():
    countries_list = 'https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)'
    all_links = []
    response = requests.get(countries_list)
    soup = BeautifulSoup(response.text, "lxml")
    countries_el = soup.select('td .flagicon+ a')
    for link_el in countries_el:
        link = link_el.get("href")
        link = urljoin(countries_list, link)
        all_links.append(link)
    return all_links