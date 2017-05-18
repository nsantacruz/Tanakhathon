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


gematria = {}
gematria[u'א'] = 1
gematria[u'ב'] = 2
gematria[u'ג'] = 3
gematria[u'ד'] = 4
gematria[u'ה'] = 5
gematria[u'ו'] = 6
gematria[u'ז'] = 7
gematria[u'ח'] = 8
gematria[u'ט'] = 9
gematria[u'י'] = 10
gematria[u'כ'] = 20
gematria[u'ל'] = 30
gematria[u'מ'] = 40
gematria[u'נ'] = 50
gematria[u'ס'] = 60
gematria[u'ע'] = 70
gematria[u'פ'] = 80
gematria[u'צ'] = 90
gematria[u'ק'] = 100
gematria[u'ר'] = 200
gematria[u'ש'] = 300
gematria[u'ת'] = 400


def getGematria(txt):
        if not isinstance(txt, unicode):
            txt = txt.decode('utf-8')
        index=0
        sum=0
        while index <= len(txt)-1:
            if txt[index:index+1] in gematria:
                sum += gematria[txt[index:index+1]]

            index+=1
        return sum



test_string2 = u"וַתֹּוצֵ֨א --- ‎וְ__conj__None__None__None__---__n687 /// יצא[__verb__hif__wayq__None__-3fsg__n694" \
              u"הָאָ֜רֶץ --- ‎הַ__art__expl__None__None__---__n697 /// אֶרֶץ/__subs__None__None__a__-?sg__n697" \
              u"דֶּ֠שֶׁא --- ‎דֶּשֶׁא/__subs__None__None__a__-msg__n701" \
              u"עֵ֣שֶׂב --- ‎עֵשֶׂב/__subs__None__None__a__-msg__n701" \
              u"מַזְרִ֤יעַ --- ‎זרע[__verb__hif__ptca__a__?msg__n706"

# {
#     "Genesis": {
#         "1": {
#             "1": [list of words]
#         }
#     }
#
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
        # print line

        if line == u'\r\n':
            end_of_verse = not end_of_verse

        elif end_of_verse:
            words = line.split()

            perek.append(pasuk)
            pasuk = []

            new_perek_num = words[-2]
            if new_perek_num != perek_num:
                book.append(perek)
                perek = []
                perek_num = new_perek_num

            new_book_title = u" ".join(words[:-2]) if len(words) > 3 else words[0]
            if new_book_title != book_title:
                books[book_title] = book
                book = []
                book_title = new_book_title

        else:
            index = line.find(u"=")

            if index is not -1:
                b_index = line.rfind(u' ', 0, index)
                word = line[b_index+1:index]
                pasuk.append(stripNikkud(word))

            else:
                index = line.find(u"/_")

                if index is not -1:
                    b_index = line.rfind(u' ', 0, index)
                    word = line[b_index:index]
                    pasuk.append(stripNikkud(word))

                else:
                    index = line.find(u"[")
                    if index is not -1:
                        b_index = line.rfind(u' ', 0, index)

                        word = line[b_index+1:index]
                        pasuk.append(stripNikkud(word))


    with codecs.open("only_shorashim.json", 'wb', encoding='utf8') as file_write:
        json.dump(books, file_write, ensure_ascii=False, indent=4)

    #     exact_words = wo_preps.write(stripNikkud(line))
    #
    # wo_preps.write("</pasuk></root>")
    # only_shorashim.write("</pasuk></root>")


