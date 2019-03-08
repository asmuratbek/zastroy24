# URL: /products/create/

import requests
from BeautifulSoup import BeautifulSoup


def get_html(url):
    response = requests.get('http://mybrands.kg/')
    return response.text


def parse(html):
    soup = BeautifulSoup(html)


def main():
    print get_html('http://bybrands.kg/')


if __name__ == '__main__':
    main()