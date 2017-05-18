from local_settings import *
from sefaria.model import *
import tfidf, json, codecs, glob

def reduce_list(list_in):
    return reduce(lambda a, b: a+b, list_in)

def input_ketaim_into_table(ketaim, table, level_num):
    for file_name in glob.glob("data/herzog_ketaim_json/*level{}.json".format(level_num)):

        print file_name



        with codecs.open(file_name, 'rb', encoding='utf8') as fp2:
            json_obj = json.load(fp2, encoding='utf8')
            for keta_obj in json_obj:
                ref = Ref(keta_obj['ref'])

                word_list = []
                for sub_ref in ref.range_list():
                    word_list += ketaim[sub_ref.index.title][sub_ref.sections[0]-1][sub_ref.sections[1]-1]
                table.addDocument(keta_obj['name'], word_list)

def find_parallels():
    table = tfidf.tfidf()
    sim_matrix = []

    count = 0
    with codecs.open("data/only_shorashim.json", 'rb', encoding='utf8') as fp:
        shorash_obj = json.load(fp)
        input_ketaim_into_table(shorash_obj, table, 2)
        for keta_name, keta_dict in table.documents:
            keta_words = keta_dict.keys()
            similarities = table.similarities(keta_words)
            sim_matrix += similarities




find_parallels()
