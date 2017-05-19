# encoding=utf-8
from local_settings import *
import codecs
import re
from sefaria.system.exceptions import *
from sefaria.system.database import db
from sefaria.model import *
from sefaria.system.exceptions import InputError
import unicodecsv, glob, json, codecs, re
from collections import OrderedDict, defaultdict

def input_ketaim_into_table(ketaim, table, level_num):
    for file_name in glob.glob("data/herzog_ketaim_json/*level{}.json".format(level_num)):

        print file_name

        with codecs.open(file_name, 'rb', encoding='utf8') as fp2:
            json_obj = json.load(fp2, encoding='utf8')
            for keta_obj in json_obj:
                ref = Ref(keta_obj['ref'])

dict = {}

with codecs.open("data/only_shorashim", 'rb', 'utf8' ) as fr:

    input_ketaim_into_table(shorash_obj, table, 2)
    for keta_name, keta_dict in table.documents:
        keta_words = keta_dict.keys()
        similarities = table.similarities(keta_words)
        sim_matrix += similarities


