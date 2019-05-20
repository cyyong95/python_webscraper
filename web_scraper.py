import requests
from bs4 import BeautifulSoup


def get_request():
    req = requests.get('https://www.yelp.com/search?find_desc=&find_loc=KL')
    req_soup = BeautifulSoup(req.text, 'html.parser')
    for name in req_soup.findAll('h3', {'class': 'lemon--h3__373c0__sQmiG'}):
        print(name.text)


if __name__ == '__main__':
    get_request()