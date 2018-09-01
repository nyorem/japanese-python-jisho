#!/usr/bin/env python3

import json
import requests
import sys

def lookup(query):

    data = json.loads(requests.get(
            "http://jisho.org/api/v1/search/words?keyword=%s" % query).text)

    results = {}

    for result in range(len(data["data"])):

        results[result] = {"readings": [], "words": [], "senses": {}}

        for a in range(len(data["data"][result]["japanese"])):
            b = data["data"][result]["japanese"][a]
            if ("reading" in b.keys() and b["reading"] not in results[result]["readings"]):
                results[result]["readings"].append(b["reading"])

            if ("word" in b.keys() and b["word"] not in results[result]["words"]):
                results[result]["words"].append(b["word"])

        for b in range(len(data["data"][result]["senses"])):
            results[result]["senses"][b] = \
                {"english": [], "parts": []}

            for c in range(len(data["data"][result]["senses"][b]["english_definitions"])):
                results[result]["senses"][b]["english"].append(
                    data["data"][result]["senses"][b]["english_definitions"][c])

            for d in range(len(data["data"][result]["senses"][b]["parts_of_speech"])):
                results[result]["senses"][b]["parts"].append(
                    data["data"][result]["senses"][b]["parts_of_speech"][d])

    return results

def get_english_translations(results):
    senses = results[0]["senses"]
    a = senses[0]["english"][:2]
    return a

# Remove non-kanji characters in a string
# see: https://stackoverflow.com/questions/33338713/filtering-out-all-non-kanji-characters-in-a-text-with-python-3
import re

hiragana_full = r'[ぁ-ゟ]'
katakana_full = r'[゠-ヿ]'
kanji = r'[㐀-䶵一-鿋豈-頻]'
radicals = r'[⺀-⿕]'
katakana_half_width = r'[｟-ﾟ]'
alphanum_full = r'[！-～]'
symbols_punct = r'[、-〿]'
misc_symbols = r'[ㇰ-ㇿ㈠-㉃㊀-㋾㌀-㍿]'
ascii_char = r'[ -~]'
def extract_unicode_block(unicode_block, string):
    return re.findall(unicode_block, str(string))
def remove_unicode_block(unicode_block, string):
    return re.sub(unicode_block, "", str(string))

def extract_kanji(text):
    return extract_unicode_block(kanji, text)

def get_kanji_translations(results):
    translations = []
    for kanji in extract_kanji(results[0]["words"][0]):
        t = get_english_translations(lookup(kanji))
        translations.append(t[0])
    return translations

if __name__ == "__main__":
    query = sys.argv[1]
    results = lookup(query)

    # jp -> english
    senses = get_english_translations(results)
    print("; ".join(senses))
    reading = get_kanji_translations(results)
    print(reading)
