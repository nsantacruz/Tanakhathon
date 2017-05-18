from local_settings import *
from sefaria.model import *
import tfidf, json, codecs, glob

def reduce_list(list_in):
    return reduce(lambda a, b: a+b, list_in)

table = tfidf.tfidf()

count = 0
with codecs.open("data/only_shorashim.json", 'rb', encoding='utf8') as fp:
    shorash_obj = json.load(fp)
    #words1 = reduce(lambda a, b: a+b, obj['Deuteronomy'][0])
    #words2 = reduce(lambda a, b: a+b, obj['Numbers'][12])
    #words3 = reduce(lambda a, b: a+b, obj['Genesis'][0])

    # for file_name in glob.glob("data\/herzog_ketaim_json\/*_level2\.json"):
    for file_name in glob.glob("data/herzog_ketaim_json/*level2.json"):

        print file_name



        with codecs.open(file_name, 'rb', encoding='utf8') as fp2:
            json_obj = json.load(fp2, encoding='utf8')
            for keta_obj in json_obj:
                ref = Ref(keta_obj['ref'])

                word_list = []
                for sub_ref in ref.range_list():
                    try:
                        word_list += shorash_obj[sub_ref.index.title][sub_ref.sections[0]-1][sub_ref.sections[1]-1]
                    except IndexError:
                        count += 1
                table.addDocument(keta_obj['name'], word_list)

print count
pass
