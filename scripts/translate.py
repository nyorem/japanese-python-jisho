#! /usr/bin/env python3

import sys
sys.path.append(".")
from jisho import get_english_translations, lookup, get_kanji_translations

space = "　"

def read_file(fname):
    with open(fname, "r") as f:
        lines = f.readlines()
        lines = [ line.strip() for line in lines]
    return lines

if __name__ == "__main__":
    fname = sys.argv[1]
    contents = read_file(fname)
    translation = []
    for line in contents:
        if len(line) == 0: # Empty lines
            translated = line
        elif "/" in line: # Translation already exists
            translated = line
        elif len(line) >= 1 and line[0] == "#": # Comments
            translated = line
        else:
            if len(line) >= 1:
                elements = line.split(space)
                to_translate = elements[0]
                print(to_translate)
                results = lookup(to_translate)
                english = get_english_translations(results)
                if english is None:
                    translated = "NO TRANSLATION FOUND"
                else:
                    english = "; ".join(english)
                    if len(elements) == 1: # no pronunciation
                        english = " / " + english
                        kanji_translations = None
                    else: # translations of the kanji
                        kanji_translations = get_kanji_translations(results)
                    elements.insert(len(elements), english)
                    translated = " / ".join(elements)
                    if (kanji_translations is not None) and (len(kanji_translations) > 1):
                        kanji_translations = [ kanji_translation if kanji_translation is not None else "KANJI NOT FOUND" for kanji_translation in kanji_translations ]
                        kanji = " + ".join(kanji_translations)
                        translated += " => " + kanji
                    # print(translated)

        translation.append(translated)
    translated = "\n".join(translation)
    # print(translated)
    fout = open("out.txt", "w")
    fout.write(translated)
