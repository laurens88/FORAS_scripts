#FORAS PROJECT
#DEBUG VERSION

import argparse
import warnings
from pathlib import Path

import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype
from asreview import ASReviewData, config
from asreview.data.base import load_data

import matplotlib.pyplot as plt
import re
import sys

pd.options.mode.chained_assignment = None

CURSOR_UP = '\033[1A'
CLEAR = '\x1b[2K'
CLEAR_LINE = CURSOR_UP + CLEAR

def _check_suffix(input_files, output_file):
    # Also raises ValueError on URLs that do not end with a file extension
    suffixes = [Path(item).suffix for item in input_files if item is not None]
    suffixes.append(Path(output_file).suffix)

    set_ris = {".txt", ".ris"}
    set_tabular = {".csv", ".tab", ".tsv", ".xlsx"}
    set_suffixes = set(suffixes)

    if len(set(suffixes)) > 1:
        if not (set_suffixes.issubset(set_ris) or set_suffixes.issubset(set_tabular)):
            raise ValueError(
                "• Several file types were given; All input files, as well as the output file should be of the same "
                "type. "
            )


def merge(output_file, input_files):
    _check_suffix(input_files, output_file)
    list_dfs = [load_data(item).df for item in input_files]

    file_dict = dict(zip(input_files, list_dfs))

    #fill source column of individual file dataframes
    for df_i in range(len(list_dfs)):
        if input_files[df_i] != output_file:
            list_dfs[df_i][input_files[df_i]] = 1 

    df_vstacked = pd.concat(list_dfs).reset_index(drop=True)

    source_columns = input_files + [c for c in df_vstacked if ".csv" in c and not "included" in c]
    if output_file in source_columns:
        source_columns.remove(output_file)

    df_vstacked_s = fill_source_columns(df_vstacked, source_columns)

    df = drop_duplicates(ASReviewData(df_vstacked_s))
    df = assign_mother_id(df)
    df = clean_columns(df)

    #Output file
    merged_complete_records = df
    as_merged = ASReviewData(df=merged_complete_records)
    as_merged.df.to_csv("../Output/"+output_file, index=False)

    df_missing_abstracts = df[df['abstract'] == ""]

    #Output missing abstracts file
    if not df_missing_abstracts.empty:
        as_missing_abstracts = ASReviewData(df=df_missing_abstracts)
        as_missing_abstracts.df.to_csv("../Output/"+output_file[:-4]+"_missing_AB.csv", index=False)

    #Display statistics about datasets merged
    print()
    print("Statistics about input sets:")
    for k,v in file_dict.items():
        print(f'{len(v.index)} \t elements in {k}')
    print()
    print("Statistics after merging:")
    unique_records_dict = count_unique_records(merged_complete_records)
    for k, v in unique_records_dict.items():
        print(f'{int(v)}\t unique records in {k}')
    source_counts(merged_complete_records)
    

def fill_source_columns(dataframe, column_names):
    for name in column_names:
        if not 'included_' in name:
            for row in range(dataframe.shape[0]):
                if dataframe.iloc[row, dataframe.columns.get_loc(name)] != 1:
                    dataframe.iloc[row, dataframe.columns.get_loc(name)] = 0
    return dataframe


def assign_mother_id(df):
    if 'MID' in df.columns:
        # If 'MID' column exists, find the last assigned ID
        last_id = df['MID'].dropna().apply(lambda x: int(x[1:])).max()
    else:
        # If 'MID' column doesn't exist, create it and start from 0
        df.insert(0, 'MID', pd.Series(), True)

        last_id = -1

    # Assign unique IDs to rows where 'MID' is NaN
    mask = df['MID'].isna()
    df.loc[mask, 'MID'] = ['M'+str(i) for i in range(last_id+1, last_id+1+mask.sum())]

    return df


def clean_columns(dataframe):
    columns_to_drop = [c for c in dataframe.columns if len(c)==0 or "Unnamed" in c]
    return dataframe.drop(columns_to_drop, axis=1)


def count_unique_records(dataframe):
    source_cols = [col for col in dataframe.columns if 'Data_' in col and 'included' not in col]
    df = dataframe[source_cols]

    df['row_sum'] = df.sum(axis=1)

    df_single = df[df['row_sum'] == 1]

    df_single = df_single.drop(columns=['row_sum'])

    result = df_single.sum().to_dict()

    return result


def source_counts(dataframe):
    source_cols = [col for col in dataframe.columns if 'Data_' in col and 'included' not in col]
    df = dataframe[source_cols]
    df['row_as_str'] = df.apply(lambda row: ''.join(row.values.astype(int).astype(str)), axis=1)

    # Count the frequency of each unique row
    df_freq = df['row_as_str'].value_counts().reset_index()
    df_freq.columns = ['row_as_str', 'frequency']

    print(df_freq)

    # Convert the string rows back to a DataFrame
    df_freq = df_freq.join(df_freq['row_as_str'].apply(lambda x: pd.Series(list(x))))
    df_freq = df_freq.drop(columns=['row_as_str'])

    print(df_freq)

    # Convert the DataFrame to a matrix
    matrix = df_freq.values
  

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
                s_pid = asrdata.df[pid].str.strip().replace("", None) ###
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
            # .str.lower().str.strip().replace("", None)

        # save boolean series for duplicates based on titles/abstracts
        s_dups_text = ((s.duplicated()) & (s.notnull()))

        # final boolean series for all duplicates
        if s_dups_pid is not None:
            s_dups = s_dups_pid | s_dups_text
        else:
            s_dups = s_dups_text
        return s_dups


def clean(text):
    text = re.sub(r'^https?:\/\/(www\.)?doi\.org\/', "", text)
    text = re.sub(r'[^A-Za-z0-9]', "", text)
    # text = text.lower().strip().replace("", None)
    return text


def drop_duplicates(asrdata, pid='doi', inplace=False, reset_index=True):
    """Drop duplicate records.
    Drop duplicates based on titles and abstracts and if available,
    on a persistent identifier (PID) such the Digital Object Identifier
    (`DOI <https://www.doi.org/>`_).
    Arguments
    ---------
    pid: string, default 'doi'
        Which persistent identifier to use for deduplication.
    inplace: boolean, default False
        Whether to modify the DataFrame rather than creating a new one.
    reset_index: boolean, default True
        If True, the existing index column is reset to the default integer index.
    Returns
    -------
    pandas.DataFrame or None
        DataFrame with duplicates removed or None if inplace=True
    """
    df = asrdata.df[~duplicated(asrdata, pid)]

    dupes = asrdata.df[duplicated(asrdata, pid)]

    df_arobject = ASReviewData(df=df)

    if dupes.empty:
        return df

    dupes_arobject = ASReviewData(df=dupes)

    # original_titles = df_arobject.title
    original_titles = df_arobject.texts

    vectorized_clean = np.vectorize(clean)

    original_titles = vectorized_clean(original_titles)

    original_doi = df_arobject.doi
    original_abstract = df_arobject.abstract

    # dupes_titles = dupes_arobject.title
    dupes_titles = dupes_arobject.texts
    dupes_titles = vectorized_clean(dupes_titles)
    dupes_doi = dupes_arobject.doi
    dupes_abstract = dupes_arobject.abstract

    dupe_source_columns = []
    for s_column in dupes.columns:
        if ".csv" in s_column and not "include" in s_column:
            dupe_source_columns.append(s_column)


    
    for row in range(len(df.index)):
        print(f"{row}/{len(df.index)}")
        print(CLEAR_LINE, end="")
        for dupe in range(len(dupes.index)):

            doi = str(original_doi[row])
            title = original_titles[row]
            abstract = original_abstract[row]

            dupe_doi = str(dupes_doi[dupe])

            dupe_title = dupes_titles[dupe]
            dupe_abstract = dupes_abstract[dupe]

            #check if duplicate matches with doi if it is not empty, else do the same check with title
            if doi != "nan" and doi == dupe_doi:
                for c in dupe_source_columns:
                    if dupes.iloc[dupe, dupes.columns.get_loc(c)] == 1:
                        df.iloc[row, df.columns.get_loc(c)] = 1
                
            elif len(str(title)) > 0 and title == dupe_title:
                for c in dupe_source_columns:
                    if dupes.iloc[dupe, dupes.columns.get_loc(c)] == 1:
                        df.iloc[row, df.columns.get_loc(c)] = 1

            # elif len(abstract) > 0 and abstract == dupe_abstract:
            #     for c in dupe_source_columns:
            #         if dupes.iloc[dupe, dupes.columns.get_loc(c)] == 1:
            #             df.iloc[row, df.columns.get_loc(c)] = 1

    # Re-order columns such that: first source columns and second label columns
    for column in df.columns:
        if ".csv" in column:
            c = df.pop(column)
            df.insert(len(df.columns), column, c)

    for column in df.columns:
        if "included_" in column:
            c = df.pop(column)
            df.insert(len(df.columns), column, c)
    
    
    if reset_index:
        df = df.reset_index(drop=True)
    if inplace:
        asrdata.df = df
        return
    return df


def _parse_arguments_vstack():
    parser = argparse.ArgumentParser(prog="asreview data vstack")
    parser.add_argument("output_path", type=str, help="The output file path.")
    parser.add_argument(
        "datasets", type=str, nargs="+", help="Any number of datasets to stack vertically."
    )

    return parser


def main():
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    merge(output_file, input_files)

if __name__ == "__main__":
    main()
