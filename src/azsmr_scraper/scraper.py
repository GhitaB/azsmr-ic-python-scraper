from bs4 import BeautifulSoup
import os
import requests
import shutil

data = {}

all_urls = []


def download_file(url, to_file):
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    headers = {'User-Agent': user_agent}
    with requests.get(url, headers=headers, stream=True) as r:
        with open("results/" +  to_file, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return to_file


def open_url(url):
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    headers = {'User-Agent': user_agent}
    page = requests.get(url, headers=headers)
    return page


def get_content(url):
    page = open_url(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    ppp = soup.find_all('p', class_='post-title')

    audio = "https://www.azsmr.ro" + soup.find_all("audio")[0].find_all("source")[0].attrs["src"]

    filename = audio.split("?")[0].split("/")[-1]
    audio_file = download_file(audio, filename)
    print("Download: " + audio_file)

    filename_base = filename.split(".mp3")[0]

    filename_png = filename_base + ".png"
    png_file = download_file("https://www.azsmr.ro/media/imnuri-crestine/partituri/" + filename_png, filename_png)
    print("Download: " + png_file)

    filename_txt = filename_base + ".txt"
    with open("results/" + filename_txt, 'w') as f:
        f.write(soup.find_all("div", class_="vers")[0].text)
    print("Download: " + filename_txt)


def get_pages_b(url):
    page = open_url(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    ppp = soup.find_all('p', class_='post-title')

    urls = [x.find_all("a")[0].attrs['href'] for x in ppp]

    global all_urls
    for uuu in urls:
        all_urls.append(uuu)


def main():
    # LEVEL A
    # Example: http://www.azsmr.ro/imnuri-crestine/pagina/5
    print("Level A. Start!")
    url = "http://www.azsmr.ro/imnuri-crestine/pagina/"
    pages_a = 17

    # LEVEL B
    # Example: https://www.azsmr.ro/5-cer-si-mare-si-pamant/
    print("Level B. Start!")
    for page in range(1, pages_a):
        print("Level B. Progress...")
        get_pages_b(url + str(page))

    # LEVEL C
    print("Level C. Start!")
    for url in all_urls:
        get_content(url)
