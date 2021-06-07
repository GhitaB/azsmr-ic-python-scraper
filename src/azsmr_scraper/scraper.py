from bs4 import BeautifulSoup
import os
import urllib
import urllib2


data = {}
CONSECUTIVE_NO_NEW = 100  # We don't know how many songs there are, but if we
# don't find new onces for x consecutive page reloads, we conclude we found
# all of them.

SAVE_DETAILS_IN_FILE = True
FILE_NAME = "songs_details.txt"

SAVE_MP3S = True
FOLDER_NAME = "Songs"


def scrap_once():
    url = "http://www.rvs.ro/"
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    music_div = soup.find("div", {"id": "melodii"})
    songs = music_div.find("ul", {"class": "songs"}).findAll("li")

    new = 0
    for song in songs:
        song_title = song.text.strip()
        if data.get(song_title, None) is None:
            new += 1
        song_url = song.findAll()[0].attrs['data-url']
        data[song_title] = song_url

    return new


def main():
    consecutive_new = 0
    while consecutive_new != CONSECUTIVE_NO_NEW:
        new = 1
        while new != 0:
            new = scrap_once()
            print "(Re)try: Found {0} new songs. Total: {1}".format(
                new,
                len(data.keys())
            )

        if new == 0:
            consecutive_new += 1
        else:
            consecutive_new = 0

    print "Total songs found: {0}".format(len(data.keys()))

    print "The list of URLs:"
    for song_title in data.keys():
        song_url = data[song_title]
        print "{0}".format(song_url)

    if SAVE_DETAILS_IN_FILE is True:
        with open(FILE_NAME, "w") as text_file:
            text_file.write("{0}".format(data))

        print "Details saved in {0}.".format(FILE_NAME)

    if SAVE_MP3S is True:
        print "Downloading mp3 files to {0}...".format(FOLDER_NAME)

        if not os.path.exists(FOLDER_NAME):
            os.makedirs(FOLDER_NAME)

        for song_title in data.keys():
            song_url = data[song_title]
            print "Downloading {0}...".format(song_url)

            mp3_file_destination = "{0}/{1}.mp3".format(
                FOLDER_NAME,
                song_title.encode("utf-8")
            )
            mp3_file = urllib.URLopener()
            mp3_file.retrieve(
                song_url,
                mp3_file_destination
            )

    print "Done!"
