# -*- coding: utf8 -*-
import os, sys
from bs4 import BeautifulSoup
import codecs


# words
# word without prefix
# shoresh

import regex
import json

reload(sys)
sys.setdefaultencoding("utf-8")


def stripNikkud(rawString):
    return regex.sub(r"[\u0591-\u05C7]", "", rawString)


def getShoresh(line, index):
    index_underscore = line.rfind(u'-', 0, index)
    index_slash = line.rfind(u'/', 0, index)

    b_index = index_slash if index_slash > index_underscore else index_underscore
    return stripNikkud(line[b_index+2:index])

def getWord(line, word):
    words = line.split()
    letters_to_delete = (len(words) - 2) / 2
    if u"impl" in line:
        letters_to_delete -= 1
    word = stripNikkud(word)
    return word[letters_to_delete:]




# {
#     "Genesis": [[[list of words]]]
# }

with codecs.open("mikra-morph.txt.withnikudnew.txt", 'rb', encoding='utf8') as file_read:

    # wo_preps.write("<root><book>")
    books = {}

    book_title = "blank"
    book = []

    perek_num = 0
    perek = []

    pasuk = []

    end_of_verse = False


    for line in file_read:

        if line == u'\r\n':
            end_of_verse = not end_of_verse

        elif end_of_verse:
            words = line.split()

            perek.append(pasuk)
            pasuk = []

            new_book_title = u" ".join(words[:-2]) if len(words) > 3 else words[0]
            new_perek_num = words[-2]
            if new_perek_num != perek_num or new_book_title != book_title:
                book.append(perek)
                perek = []
                perek_num = new_perek_num

            if new_book_title != book_title:
                books[book_title] = book
                book = []
                book_title = new_book_title

        else:

            b_index = line.find(u"---")

            index = line.find(u"=")

            if index is not -1:
                pasuk.append(getShoresh(line, index))
            else:
                index = line.find(u"/_")
                if index is not -1:
                  pasuk.append(getShoresh(line, index))
                else:
                    index = line.find(u"[")
                    if index is not -1:
                        pasuk.append(getShoresh(line, index))


    with codecs.open("whole_tanakh.json", 'wb', encoding='utf8') as file_write:
        json.dump(books, file_write, ensure_ascii=False, indent=4)

    #     exact_words = wo_preps.write(stripNikkud(line))
    #
    # wo_preps.write("</pasuk></root>")
    # only_shorashim.write("</pasuk></root>")


