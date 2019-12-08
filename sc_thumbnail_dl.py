"""
TO DOWNLOAD THUMBNAIL OFF SOUNDCLOUD TRACKS
"""
import requests
import bs4
import os
from sys import exit
from requests import HTTPError


def fetch_res(link):
    try:
        res = requests.get(link)
        res.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
        exit()
    except Exception as err:
        print(f'Other error occurred: {err}')
        exit()
    else:
        return res


def write_res(res):
    try:
        res_file = open('res_file.txt', 'wb')
        for chunk in res.iter_content(1000):
            res_file.write(chunk)
        res_file = open('res_file.txt', 'r', encoding="utf8")
        soup_file = bs4.BeautifulSoup(res_file, features='html.parser')
        res_file.close()
    except Exception as err:
        print(f"Error has occured: {err}")
        exit()
    else:
        return soup_file


def parse_res(soups_file):
    try:
        thumbnail = soups_file.findAll('img')
        thumb_link = thumbnail[0]['src']
        title_up = soups_file.findAll('title')
        title_str = title_up[0].text
    except Exception as err:
        print(f'Error has occured: {err}')
        exit()
    else:
        return thumb_link, title_str


def download_image(url, title_str):
    try:
        os.makedirs("images", exist_ok=True)
        image = requests.get(url)
        image.raise_for_status()
        img_file = open(os.path.join('images', os.path.basename(title_str.split(' by')[0]) + ".jpg"), 'wb')
        for chunk in image.iter_content(1000):
            img_file.write(chunk)
        img_file.close()
        print("Album art downloaded. Available at Images Folder")
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        exit()
    except Exception as err:
        print(f"Error has occured: {err}")
        exit()


def get_input():
    try:
        sc_url = str(input("Enter the soundcloud link of the track :  "))
    except ValueError as v_err:
        print(f"Invalid Link Provided : {v_err}")
        exit()
    except Exception as err:
        print(f"The link provided does not seem to be invalid. Error: {err}")
        exit()
    else:
        return sc_url


# sc_link = 'https://soundcloud.com/ichibanhm1/porter-robinson-shelter-ichibanhm1-remix'
# https://shorturl.at/dehox
# https://cutt.ly/De4FBDN
sc_link = get_input()
http_res = fetch_res(sc_link)
resource_file = write_res(http_res)
tb_url, title = parse_res(resource_file)
download_image(tb_url, title)
