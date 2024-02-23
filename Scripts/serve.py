#FORAS PROJECT
#DEBUG VERSION

import argparse
import warnings
from pathlib import Path
import sys

import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype
from asreview import ASReviewData, config
from asreview.data.base import load_data

CURSOR_UP = '\033[1A'
CLEAR = '\x1b[2K'
CLEAR_LINE = CURSOR_UP + CLEAR


def serve(file, prior_calibration_file, n_records, annotators):
    if not annotators:
        print("No annotators were given.")
        return

    dataframe = pd.read_csv(file, low_memory=False)

    annotation_df = dataframe

    #drop all columns except title, abstract, doi, and MID
    important_columns = config.COLUMN_DEFINITIONS['title'] + config.COLUMN_DEFINITIONS['abstract'] \
    + config.COLUMN_DEFINITIONS['doi'] + ['MID'] \
    + [col for col in annotation_df.columns if 'year' in col]
    annotation_df =  annotation_df[annotation_df.columns.intersection(important_columns)]

    #remove records that were in previous batches
    prior_calibration_df = pd.read_excel(prior_calibration_file)
    prior_mid = prior_calibration_df['MID']

    #add MIDs of Synergy to be sure they are excluded
    for i in range(12914):
        prior_mid.loc[len(prior_mid)] = "M"+str(i)

    df = sample(annotation_df, n_records, prior_mid)

    output_annotation_df(df, annotators)


def row_has_label(row, label_columns):
    return any(row[col] in [0, 1] for col in label_columns)


def output_annotation_df(annotation_df, annotators):
    #add annotator columns to annotation dataframe
    for annotator in annotators:
        #create copy of dataframe for each annotator
        df = annotation_df.copy()

        #add title abstract annotation columns
        df[f'title_eligible_{annotator}'] = np.nan
        df[f'TI-AB_IC1_{annotator}'] = np.nan
        df[f'TI-AB_IC2_{annotator}'] = np.nan
        df[f'TI-AB_IC3_{annotator}'] = np.nan
        df[f'TI-AB_IC4_{annotator}'] = np.nan
        df[f'TI-AB_other_exlusion_reason_{annotator}'] = np.nan
        df[f'TI-AB_final_label_{annotator}'] = np.nan

        #add full text annotation columns
        # df[f'FT_IC1_{annotator}'] = np.nan
        # df[f'FT_IC2_{annotator}'] = np.nan
        # df[f'FT_IC3_{annotator}'] = np.nan
        # df[f'FT_IC4_{annotator}'] = np.nan
        # df[f'FT_other_exlusion_reason_{annotator}'] = np.nan
        # df[f'FT_final_label_{annotator}'] = np.nan

        #output new annotation dataframe
        df = df.applymap(lambda x: x.encode('unicode_escape').
                 decode('utf-8') if isinstance(x, str) else x)
        df.to_excel(annotator+".xlsx", index=False)


def sort_by_date(df):
    for c in df.columns:
        if 'year' in c:
            return df.sort_values(c, ascending=True)
    return


def sample(df, n_records, prior_mid):
    #remove all records with MID in prior_mid from df
    df = df[~df['MID'].isin(prior_mid)]
    n_records = min(n_records, len(df))
    print()
    print(f'Sampled {n_records} records.')
    print(f'{len(df)-n_records} records left to screen after this batch.')
    random = df.sample(n=n_records, random_state=1)
    return random
    

def main():
    file = sys.argv[1]
    prior_file = sys.argv[2]
    n_records = int(sys.argv[3])
    annotators = sys.argv[4:]
    print(f'Sampling from {file}')
    print(f'Avoiding records from {prior_file}')
    print(f'Attemping to sample {n_records} records for {annotators}')
    print("")
    serve(file, prior_file, n_records, annotators)


if __name__ == "__main__":
    main()
