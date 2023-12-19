import sys
import re
import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype
from asreview import ASReviewData

def insert(motherfile:str, annotation_file:str, annotator:str):
    mother_frame = pd.read_csv(motherfile)
    annotation_frame = pd.read_excel(annotation_file)

    mother_frame = add_label_columns(mother_frame, annotation_frame, annotator)

    #get correct columns from motherfile and annotation file (.filter(like=annotator).columns)?
    mother_label_columns = mother_frame.filter(like=annotator).columns
    annotation_label_columns = annotation_frame.filter(like=annotator).columns

    #TODO
    #get the intersection of the two label column lists to know which to fill in for the motherfile

    #loop through annotation file rows
    for annotation_row in range(len(annotation_frame)):
        #loop through motherfile rows
        for mother_row in range(len(mother_frame)):
            #check if papers match
            if records_match(mother_frame, annotation_frame, mother_row, annotation_row):
                ...
                #set_label_values(mother_row, annotation_row)

#Add empty label columns to motherfile with names from annotation file
def add_label_columns(mother_df:pd.DataFrame, annotation_df:pd.DataFrame, annotator:str):
    label_columns = annotation_df.filter(like=annotator).columns
    for column in label_columns:
        if not column in mother_df.columns:
            mother_df[column] = np.nan
    return mother_df


def set_label_values(mother_index: int, annotation_index: int):
    ...
    #set values of columns from moterfile to those of annotation file


def records_match(df1: pd.DataFrame, df2: pd.DataFrame, index1: int, index2: int):
    df = pd.DataFrame(columns=df1.columns)
    df.loc[0] = df1.iloc[index1]
    df.loc[1] = df2.iloc[index2]

    return duplicated(ASReviewData(df)).any()


def duplicated(asrdata, pid='doi'):
        """Return boolean Series denoting duplicate rows.
        Identify duplicates based on titles and abstracts and if available,
        on a persistent identifier (PID) such as the Digital Object Identifier
        (`DOI <https://www.doi.org/>`_).
        Arguments
        ---------
        pid: string
            Which persistent identifier to use for deduplication.
            Default is 'doi'.
        Returns
        -------
        pandas.Series
            Boolean series for each duplicated rows.
        """
        
        if pid in asrdata.df.columns:
            # in case of strings, strip whitespaces and replace empty strings with None
            if is_string_dtype(asrdata.df[pid]):
                s_pid = asrdata.df[pid].str.strip().replace("", None)
                s_pid = re.sub(r'^https?:\/\/(www\.)?doi\.org\/', "", s_pid)
            else:
                s_pid = asrdata.df[pid]

            # save boolean series for duplicates based on persistent identifiers
            s_dups_pid = ((s_pid.duplicated()) & (s_pid.notnull()))
        else:
            s_dups_pid = None      

        # get the texts, clean them and replace empty strings with None
        s = pd.Series(asrdata.texts) \
            .str.replace("[^A-Za-z0-9]", "", regex=True) \
            .str.lower().str.strip().replace("", None)

        # save boolean series for duplicates based on titles/abstracts
        s_dups_text = ((s.duplicated()) & (s.notnull()))

        # final boolean series for all duplicates
        if s_dups_pid is not None:
            s_dups = s_dups_pid | s_dups_text
        else:
            s_dups = s_dups_text
        return s_dups


def main():
    motherfile = sys.argv[1]
    annotation_file = sys.argv[2]
    annotator = sys.argv[3]
    # insert(motherfile, annotation_file, annotator)
    print(records_match(pd.read_csv(motherfile, encoding="ISO-8859-1"), pd.read_csv(motherfile, encoding="ISO-8859-1"), 0, 0))
    


if __name__ == '__main__':
    main()
