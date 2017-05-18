# -*- coding: utf-8 -*-
from local_settings import *
from sefaria.model import *
from sefaria.system.exceptions import InputError
import unicodecsv, glob, json, codecs, re
from collections import OrderedDict, defaultdict


def parse():
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
        prev_level1 = ''
        prev_level2 = ''
        prev_level3 = ''

        level1_dict = []
        level2_dict = []
        level3_dict = []
        with open(file_name, 'rb') as f:
            book_name = re.findall(r"\/([^\/]+).txt", file_name)[0]
            if book_name == u"Numbers":
                pass
            csv_f = unicodecsv.DictReader(f, delimiter='\t')

            just_switched_2 = False
            but_kinda_did = False
            for i, row in enumerate(csv_f):

                if row[sefer] != row[toSefer]:
                    print u"AHHHHH '{}' '{}'".format(row[sefer], row[toSefer])
                    raise Exception(u"AHHH {}".format(i))

                if row[sefer] == u"" or row[perek] == u"" or row[pasuk] == u"":
                    #print 'continueing'
                    if just_switched_2 or but_kinda_did:
                        level3_dict += [{u"name": level2_dict[-1][u"name"],
                                         u"ref": level2_dict[-1][u"ref"]}]
                        just_switched_2 = False
                    break
                try:
                    if row[perek] == u"טז":
                        pass

                    ref1 = Ref(u"{} {}:{}".format(row[sefer], row[perek], row[pasuk]))
                    ref2 = Ref(u"{} {}:{}".format(row[sefer], row[toPerek], row[toPasuk]))

                    curr_ref = ref1.to(ref2)
                    #print curr_ref
                    if row[level1].strip() != prev_level1.strip() and (row[level2] is None or row[level2].strip() == u"") and \
                            (row[level3] is None or row[level3].strip() == u""):
                        prev_level1 = row[level1]

                        if just_switched_2 or but_kinda_did:
                            level3_dict += [{u"name": level2_dict[-1][u"name"],
                                             u"ref": level2_dict[-1][u"ref"]}]
                            just_switched_2 = False

                        but_kinda_did = False

                        level1_dict += [{u"name": row[level1],
                                         u"ref": curr_ref.normal()}]

                    elif (row[level2].strip() != prev_level2.strip() and (row[level3] is None or row[level3].strip() == u"")):
                        prev_level2 = row[level2]


                        if just_switched_2 or but_kinda_did:
                            level3_dict += [{u"name": level2_dict[-1][u"name"],
                                             u"ref": level2_dict[-1][u"ref"]}]
                            just_switched_2 = False
                            but_kinda_did = True
                        else:
                            just_switched_2 = True
                            but_kinda_did = False

                        level2_dict += [{u"name": row[level2],
                                         u"ref": curr_ref.normal()}]

                    elif row[level3].strip() != prev_level3.strip():
                        prev_level3 = row[level3]
                        level3_dict += [{u"name": row[level3],
                                         u"ref": curr_ref.normal()}]
                        just_switched_2 = False
                        but_kinda_did = False







                except InputError:
                    pass
                    print u"{} {}:{}".format(row[sefer], row[perek], row[pasuk])
                    print u"{} {}:{}".format(row[sefer], row[toPerek], row[toPasuk])


        with codecs.open("{}/{}_level1.json".format(json_root, book_name), "wb", encoding='utf8') as fp:
            json.dump(level1_dict, fp, indent=4, ensure_ascii=False)
        with codecs.open("{}/{}_level2.json".format(json_root, book_name), "wb", encoding='utf8') as fp:
            json.dump(level2_dict, fp, indent=4, ensure_ascii=False)
        with codecs.open("{}/{}_level3.json".format(json_root, book_name), "wb", encoding='utf8') as fp:
            json.dump(level3_dict, fp, indent=4, ensure_ascii=False)


def check_output():
    count = 0
    for file_name in glob.glob("data/herzog_ketaim_json/*.json"):
        print file_name
        book = re.findall(r"\/([^\/]+)_level.\.json", file_name)[0]
        with codecs.open(file_name, 'rb', encoding='utf8') as fp:
            all_segs = library.get_index(book).all_segment_refs()
            ref_dict = defaultdict(int)
            in_json = json.load(fp, encoding='utf8')
            for thingy in in_json:
                r = Ref(thingy['ref'])
                for sub_r in r.range_list():
                    ref_dict[sub_r.normal()] += 1


            for r in all_segs:
                if ref_dict[r.normal()] == 0:
                    count += 1
                    print "{} {}".format(r.normal(), ref_dict[r.normal()])

    print "COUnt {}".format(count)


parse()
check_output()



