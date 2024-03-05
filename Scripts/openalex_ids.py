import pandas as pd
from pyalex import Works
import os
import copy
import requests
from time import sleep
import unicodedata
import urllib.parse

LENS_TOKEN = os.getenv("LENS_TOKEN")

SPECIAL_TOKENS = """()[]{}'@#:;"%&`’,.?!/\\^®"""


def main():
    motherfile = pd.read_excel("Motherfile_050324.xlsx")
    inclusions = pd.read_excel("FT_Screening_Bruno_labeled.xlsx")

    for inclusion in range(len(inclusions)):
        for record in range(len(motherfile)):
            inclusion_mid = inclusions.at[inclusion, "MID"]
            mother_mid = motherfile.at[record, "MID"]
            if inclusion_mid == mother_mid:
                inclusions.at[inclusion, "openalex_id"] = motherfile.at[record, "openalex_id"]

    inclusions.to_excel("FT_Screening_Bruno_labeled_V2.xlsx", index=False)

def search_record(title, year=None, label_included=None):

    title_raw = copy.copy(title)

    # clean title to prevent zero hits in openalex due to bad special char
    # handling.
    for x in SPECIAL_TOKENS:
        title = title.replace(x, "")

    # search for the work on OpenAlex
    try:
        r = Works().search(title).get()
    except requests.exceptions.JSONDecodeError:
        sleep(5)
        r = Works().search(title).get()

    matches = []
    for work in r:
        if (
            "title" in work
            and work["title"]
            and title
            and compare_titles(work["title"], title)
        ):
            matches.append(work)

    if len(matches) == 1:
        return matches[0]["doi"], matches[0]["id"], "search_title"

    # if there was no match of more than one match, go to this step.
    # we match year as well.
    matches_year = []
    for work in matches:
        if (
            "publication_year" in work
            and work["publication_year"]
            and year
            and work["publication_year"] == year
        ):
            matches_year.append(work)

    if len(matches_year) == 1:
        return matches_year[0]["doi"], matches_year[0]["id"], "search_title_year"

    if LENS_TOKEN and label_included == 1:
        print("Search with Lens")

        title_quote = urllib.parse.quote(title)
        url = f"https://api.lens.org/scholarly/search?query=title:({title_quote})&include=external_ids,title,year_published,lens_id&size=1&token={LENS_TOKEN}"

        r = requests.get(url)
        rdata = r.json()
        print(title)
        print(rdata)
        try:
            sleep(6)
            ids = rdata["data"][0]["external_ids"]
            doi = filter(lambda x: x["type"] == "doi", ids).__next__()["value"]
            print(doi)
            openalex_id = Works()["doi:" + doi]["id"]
            print(openalex_id)
            return None, openalex_id, "lens_lookup"
        except Exception as err:
            print(err)

    return None, None, None

def compare_titles(s1, s2):

    # print(compare_titles("Test & orčpžsíáýd", "Testorcpzsiayd"))

    s1_uni = unicodedata.normalize("NFKD", s1).lower()
    s2_uni = unicodedata.normalize("NFKD", s2).lower()

    s1_clean = "".join(i for i in s1_uni if i.isalnum())
    s2_clean = "".join(i for i in s2_uni if i.isalnum())

    return s1_clean == s2_clean

main()