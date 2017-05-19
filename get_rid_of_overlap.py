# -*- coding: utf8 -*-

import json, codecs, glob
from local_settings import *
import codecs
import re
from sefaria.system.exceptions import *
from sefaria.system.database import db
from sefaria.model import *
from sefaria.system.exceptions import InputError
import unicodecsv, glob, json, codecs, re
from collections import OrderedDict, defaultdict

    # {
    #     "ref": "Deuteronomy 12:1-14:21",
    #     "name": "היבדלות מעבודה זרה ודרכיה

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    print type(obj)
    raise TypeError

for i in [1,2,3]:
    refs = []
    for file_name in glob.glob("data/herzog_ketaim_json/*level{}.json".format(i)):

        with codecs.open(file_name, 'rb', encoding='utf8') as fp2:
            json_obj = json.load(fp2, encoding='utf8')
            prev_ref_list = []
            for keta_obj in json_obj:
                ref = Ref(keta_obj['ref'])

                ref_list = ref.range_list()

                if bool(set(ref_list) & set(prev_ref_list)):
                    for sub_ref in ref_list:
                        if sub_ref in prev_ref_list:
                            ref_list = ref_list[1:]
                prev_ref_list = ref_list

                refs += [{u"name": keta_obj["name"],
                         u"b_ref": ref_list[0].normal(),
                         u"e_ref": ref_list[-1].normal()}]
                # print ref_list[0], ref_list[-1]

    with codecs.open("data/level_{}_wo_overlaps.json".format(i), 'wb', encoding='utf8') as file_write:
        json.dump(refs, file_write, ensure_ascii=False, indent=4)
