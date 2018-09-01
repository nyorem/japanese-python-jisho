#! /usr/bin/env python3

import sys
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
        if len(line) == 0: # empty lines
            translated = line
        elif len(line) >= 1 and line[0] == "#": # Title lines
            translated = line
        else:
            if len(line) >= 1:
                elements = line.split(space)
                to_translate = elements[0]
                print(to_translate)
                results = lookup(to_translate)
                english = get_english_translations(results)
                english = "; ".join(english)
                if len(elements) == 1: # no pronunciation
                    english = " / " + english
                    kanji_translations = None
                else: # translations of the kanji
                    kanji_translations = get_kanji_translations(results)
                elements.insert(len(elements), english)
                translated = " / ".join(elements)
                if kanji_translations is not None:
                    kanji = " + ".join(kanji_translations)
                    translated += " => " + kanji
                # print(translated)

        translation.append(translated)
    translated = "\n".join(translation)
    # print(translated)
    fout = open("out.txt", "w")
    fout.write(translated)
