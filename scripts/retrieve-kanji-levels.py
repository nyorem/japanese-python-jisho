#! /usr/bin/env python

from bs4 import BeautifulSoup
import requests

def find_kanji(level, verbose=False):
    if verbose:
        print("level={}".format(level))

    baseurl = "https://jisho.org/search/%23kanji%20%23jlpt-n{}?page={}"
    page = 1
    kanji_list = []

    while True:
        if verbose:
            print("page={}".format(page))

        url = baseurl.format(level, page)
        req = requests.get(url)
        s = req.text
        soup = BeautifulSoup(s, "html.parser")

        page_container = soup.find(id="page_container")
        secondary = page_container.find(id="secondary")
        kanji_block = secondary.find(class_="kanji_light_block")
        found = kanji_block.h4.text

        if verbose:
            print(found)

        kanji_entries = kanji_block.findAll(class_="entry")

        if verbose:
            print("{} kanji".format(len(kanji_entries)))

        for k in kanji_entries:
            kanji = k.find(class_="character literal japanese_gothic").a.text
            kanji_list.append(kanji)

        more = kanji_block.find(class_="more")
        if more is None:
            break

        page += 1

    if verbose:
        print("")

    return kanji_list

if __name__ == "__main__":
    levels = [ 5, 4, 3, 2, 1 ]

    for level in levels:
        kanji_list = find_kanji(level, verbose=True)
        fname = "data/kanji_n{}.txt".format(level)
        with open(fname, "w") as f:
            f.write("\n".join(kanji_list))
