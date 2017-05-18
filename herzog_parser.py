# -*- coding: utf-8 -*-
from local_settings import *
from sefaria.model import *
from sefaria.system.exceptions import InputError
import unicodecsv, glob, json, codecs, re
from collections import OrderedDict

toPasuk = u'עד פסוק'
toPerek = u'עד פרק'
toSefer = u'עד ספר'
pasuk = u'מפסוק'
perek = u'מפרק'
sefer = u'מספר'
level1 = u'חטיבה (1)'
level2 = u'יחידה (2)'
level3 = u'פירוט (3)'

csv_root = "data/herzog_ketaim"
json_root = "data/herzog_ketaim_json"
for file_name in glob.glob("{}/*.txt".format(csv_root)):
    prev_level1 = None
    prev_level2 = None
    prev_level3 = None

    level1_dict = []
    level2_dict = []
    level3_dict = []
    with open(file_name, 'rb') as f:
        csv_f = unicodecsv.DictReader(f, delimiter='\t')
        for i, row in enumerate(csv_f):

            if row[sefer] != row[toSefer]:
                print u"AHHHHH '{}' '{}'".format(row[sefer], row[toSefer])
                raise Exception(u"AHHH {}".format(i))

            if row[sefer] == u"" or row[perek] == u"" or row[pasuk] == u"":
                print 'continueing'
                break
            try:
                ref1 = Ref(u"{} {}:{}".format(row[sefer], row[perek], row[pasuk]))
                ref2 = Ref(u"{} {}:{}".format(row[sefer], row[toPerek], row[toPasuk]))

                curr_ref = ref1.to(ref2)
                print curr_ref
                if row[level1] != prev_level1:
                    prev_level1 = row[level1]
                    level1_dict += [{u"name": row[level1],
                                     u"ref": curr_ref.normal()}]
                elif row[level2] != prev_level2:
                    prev_level2 = row[level2]
                    level2_dict += [{u"name": row[level2],
                                     u"ref": curr_ref.normal()}]
                elif row[level3] != prev_level3:
                    prev_level3 = row[level3]
                    level3_dict += [{u"name": row[level3],
                                     u"ref": curr_ref.normal()}]


            except InputError:
                print u"{} {}:{}".format(row[sefer], row[perek], row[pasuk])
                print u"{} {}:{}".format(row[sefer], row[toPerek], row[toPasuk])

    book_name = re.findall(r"\/([^\/]+).txt", file_name)[0]
    with codecs.open("{}/{}_level1.json".format(json_root, book_name), "wb", encoding='utf8') as fp:
        json.dump(level1_dict, fp, indent=4, ensure_ascii=False)
    with codecs.open("{}/{}_level2.json".format(json_root, book_name), "wb", encoding='utf8') as fp:
        json.dump(level2_dict, fp, indent=4, ensure_ascii=False)
    with codecs.open("{}/{}_level3.json".format(json_root, book_name), "wb", encoding='utf8') as fp:
        json.dump(level3_dict, fp, indent=4, ensure_ascii=False)



