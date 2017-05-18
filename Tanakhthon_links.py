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


def katov_3_linked(mikta1, mikta2):

    rfset1 = refset(mikta1)
    rfset2 = refset(mikta2)

    shset1 = sheet_set(mikta1)
    shset2 = sheet_set(mikta2)

    intersect_rf = rfset1.intersection(rfset2)
    intersect_sheet = shset1.intersection(shset2)
    return intersect_rf, intersect_sheet


def refset(mikta):
    ref = Ref(mikta)

    ls = ref.linkset().array()

    rfset = []
    for lnk in ls:
        rfset.extend(lnk.refs)
    rfset = set(rfset)
    # set.remove(mikta) #it will fall since there aren't links from tanach to tanach,
    # note: this line might be a prob with other texts we will have

    return rfset


def sheet_set(mikta):
    mkt_dict_lst = get_sheets_for_ref(mikta, pad=True, context=1)
    mkt_lst = []
    for dict in mkt_dict_lst:
        mkt_lst.append(dict['_id'])
    return set(mkt_lst)  # should it be a set or should we count it?



def get_sheets_for_ref(tref, pad=True, context=1):
    """
    Returns a list of sheets that include ref,
    formating as need for the Client Sidebar.
    """
    oref = Ref(tref)
    if pad:
        oref = oref.padded_ref()
    if context:
        oref = oref.context_ref(context)

    ref_re = oref.regex()

    results = []

    regex_list = oref.regex(as_list=True)
    ref_clauses = [{"sources.ref": {"$regex": r}} for r in regex_list]
    sheets = db.sheets.find({"$or": ref_clauses, "status": "public"},
        {"id": 1, "title": 1, "owner": 1, "sources.ref": 1, "views": 1}).sort([["views", -1]])
    for sheet in sheets:
        matched_refs = []
        if "sources" in sheet:
            for source in sheet["sources"]:
                if "ref" in source:
                    matched_refs.append(source["ref"])
        matched_refs = [r for r in matched_refs if re.match(ref_re, r)]
        for match in matched_refs:
            try:
                match = Ref(match)
            except InputError:
                continue

            com = {
                "_id":             str(sheet["_id"]),
                "anchorRef":       match.normal(),
                "anchorVerse":     match.sections[-1] if len(match.sections) else 1,
            }

            results.append(com)

    return results

def get_ketaim():
    in_json = json.load(fp, encoding='utf8')


def get_miktaim():
    for file_name in glob.glob("data/herzog_ketaim_json/*level{}.json".format(2)):

        print file_name
        with codecs.open(file_name, 'rb', encoding='utf8') as fp2:
            json_obj = json.load(fp2, encoding='utf8')
            refs = []
            names = []
            for keta_obj in json_obj:
                refs += [keta_obj['ref']]
                names += [keta_obj['name']]
            # return refs, names
    return json_obj


if __name__ == "__main__":
    # ind = library.get_index('Genesis')
    # mktaim = []
    # for seg in ind.all_section_refs():
    #     title = seg.index.title
    #     sections = seg.sections
    #     mkt = u'{} {}'.format(title, sections)
    #     mktaim.append(mkt)
    min_ref_insec = 100
    min_sheet_insec = 2
    # mktaim, names = get_miktaim()
    mktaim = get_miktaim()
    for i, mkt1 in enumerate(mktaim):
        for mkt2 in mktaim[i+1:]:
            ref_insec, sheet_insec = katov_3_linked(mkt1['ref'], mkt2['ref'])
            if (len(ref_insec) > min_ref_insec and len(sheet_insec) > min_sheet_insec):
                print mkt1['name'], mkt1['ref'], mkt2['name'], mkt2['ref']
                print 'segments linked ' + str(len(ref_insec))
                print 'segment sheets ' + str(len(sheet_insec))

