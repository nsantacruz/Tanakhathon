from local_settings import *
from sefaria.model import *
import tfidf, json, codecs, glob

class Keta:

    def __init__(self, ref, name, words):
        self.ref = ref
        self.name = name
        self.words = words

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not(self == other)

    def __str__(self):
        return u"{} - {}".format(self.name, self.ref.normal())


def reduce_list(list_in):
    return reduce(lambda a, b: a+b, list_in)

def input_ketaim_into_table(ketaim, table, level_num):
    for file_name in glob.glob("data/herzog_ketaim_json/*level{}.json".format(level_num)):

        print file_name



        with codecs.open(file_name, 'rb', encoding='utf8') as fp2:
            json_obj = json.load(fp2, encoding='utf8')
            for keta_dict in json_obj:
                ref = Ref(keta_dict['ref'])
                word_list = []
                for sub_ref in ref.range_list():
                    word_list += ketaim[sub_ref.index.title][sub_ref.sections[0]-1][sub_ref.sections[1]-1]
                keta_obj = Keta(ref, keta_dict['name'], word_list)
                table.addDocument(keta_obj, word_list)
    table.finalize()

def find_parallels():

    sim_matrix = []

    count = 0
    with codecs.open("data/only_shorashim.json", 'rb', encoding='utf8') as fp:
        shorash_obj = json.load(fp)
        all_words = set()
        for k, v in shorash_obj.items():
            if k == u"Obadiah":
                continue
            all_words |= set(reduce_list(reduce_list(v)))

        table = tfidf.tfidf(all_words)
        input_ketaim_into_table(shorash_obj, table, 2)
        for keta_obj, keta_dict in table.documents.items():
            similarities = table.similarities(keta_obj, 5)
            sim_matrix += similarities

            for similarity in similarities:
                if similarity[1] > 0.5:
                    print u"{}\n\t{}\n\t{}".format(similarity[1], keta_obj, similarity[0])

        pass





find_parallels()
