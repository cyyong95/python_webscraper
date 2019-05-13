import requests
from bs4 import BeautifulSoup
import os


def getHTML():

    # Check if user input instagram url
    # if len(sys.argv) != 1:
    #     print("Please input a public Instagram profile!")

    url = requests.get("https://www.instagram.com/taylorswift/?hl=en")
    soup = BeautifulSoup(url.text, 'html.parser')
    f = open("html.txt", "w+")
    f.write(url.text)
    f.close()
    print(soup.title.string[:-31])




if __name__ == '__main__':
    getHTML()
