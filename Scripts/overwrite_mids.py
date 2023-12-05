import pandas as pd
import sys
import re
from asreview import ASReviewData

def overwrite_mids(old_file, updated_file, motherfile):
    old_df = pd.read_excel(old_file)
    new_df = pd.read_excel(old_file)
    mother_df = pd.read_csv(motherfile)
    correct_df = match_and_overwrite(old_df, new_df, mother_df)
    correct_df.to_excel(updated_file, index=False)


def match_and_overwrite(old, new, mother, pid='doi', inplace=False, reset_index=True):

    for i in range(len(mother.index)):
        mother.iloc[i, mother.columns.get_loc("title")] = str(mother.iloc[i, mother.columns.get_loc("title")])
        mother.iloc[i, mother.columns.get_loc("abstract")] = str(mother.iloc[i, mother.columns.get_loc("abstract")])

    mother_arobject = ASReviewData(df=mother)

    old_arobject = ASReviewData(df=old)

    mother_texts = mother_arobject.texts

    mother_texts = [clean(text) for text in mother_texts]

    mother_dois = mother_arobject.doi

    old_texts = old_arobject.texts
    old_texts = [clean(text) for text in old_texts]
    old_dois = old_arobject.doi

    
    for old_row in range(len(old.index)):
        for mother_row in range(len(mother.index)):

            # print(mother_row , " " , len(mother_doi))
            mother_doi = str(mother_dois[mother_row])
            mother_text = mother_texts[mother_row]
 
            old_doi = str(old_dois[old_row])
            old_text = old_texts[old_row]

            #check if duplicate matches with doi if it is not empty, else do the same check with texts
            if mother_doi != "nan" and mother_doi == old_doi:
                new.iloc[old_row, new.columns.get_loc("MID")] = mother.iloc[mother_row, mother.columns.get_loc("MID")]
                
            elif len(str(mother_text)) > 0 and mother_text == old_text:
                new.iloc[old_row, new.columns.get_loc("MID")] = mother.iloc[mother_row, mother.columns.get_loc("MID")]

    # Re-order columns such that: first source columns and second label columns
    for column in new.columns:
        if ".csv" in column:
            c = new.pop(column)
            new.insert(len(new.columns), column, c)

    for column in new.columns:
        if "included_" in column:
            c = new.pop(column)
            new.insert(len(new.columns), column, c)
    
    
    if reset_index:
        new = new.reset_index(drop=True)
    return new


def clean(text):
    text = re.sub(r'^https?:\/\/(www\.)?doi\.org\/', "", text)
    text = re.sub(r'[^A-Za-z0-9]', "", text)
    # text = text.lower().strip().replace("", None)
    return text


def main():
    old_file = sys.argv[1]
    updated_file = sys.argv[2]
    mother_file = sys.argv[3]
    overwrite_mids(old_file, updated_file, mother_file)

if __name__ == "__main__":
    main()