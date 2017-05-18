# encoding=utf-8

import codecs
import re
from sefaria.model import *
from sefaria.system.exceptions import *
from sefaria.system.database import db


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


if __name__ == "__main__":
    mkt1 = 'Numbers 13' #'Genesis 12'
    mkt2 = 'Deuteronomy 1'#'Genesis 20'
    ref_insec, sheet_insec = katov_3_linked(mkt1, mkt2)
    ind = library.get_index('Genesis')
    # pesukim = []
    # for seg in ind.all_segment_refs():
    #     title = seg.index.title
    #     sections = seg.sections
    #     mkt = title + sections
    #     pesukim.append(mkt)
    #
    # for mkt1 in pesukim:
    #     for mkt2 in pesukim:
    #         ref_insec, sheet_insec = katov_3_linked(mkt1, mkt2)
    #         print 'segments linked ' + str(len(ref_insec))
    #         print 'segment sheets ' + str(len(sheet_insec))
    print 'segments linked ' + str(len(ref_insec))
    print 'segment sheets ' + str(len(sheet_insec))