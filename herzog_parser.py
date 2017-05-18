# -*- coding: utf-8 -*-
from local_settings import *
from sefaria.model import *
import unicodecsv, glob

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
for file_name in glob.glob("{}/*.txt".format(csv_root)):
    prev_level1 = None
    prev_level2 = None
    prev_level3 = None

    level1_dict = {}
    level2_dict = {}
    level3_dict = {}
    with open(file_name, 'rb') as f:
        csv_f = unicodecsv.DictReader(f, delimiter='\t')
        for row in csv_f:
            row[toPasuk]
            row[toPerek]
            row[toSefer]
            row[pasuk]
            row[perek]
            row[sefer]
            row[level1]
            row[level2]
            row[level3]

