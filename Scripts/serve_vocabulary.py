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

    dataframe = pd.read_csv(file)

    label_columns = [col for col in dataframe.columns if 'final_label_' in col or 'included' in col]

    if label_columns:

        annotation_df = pd.DataFrame(columns=dataframe.columns)

        for row in range(len(dataframe)):
            #check if none of the columns that contain "final_label_" have a label 0 or 1
            if not row_has_label(dataframe.iloc[row], label_columns):
                unlabeled_row = dataframe.iloc[row]
                annotation_df.loc[len(annotation_df)] = unlabeled_row
                print(CLEAR_LINE)
                print(row,"/",len(dataframe), end="")
    
        print(f'Found {len(annotation_df)} records without label.')
    
    else:
        annotation_df = dataframe

    #drop all columns except title, abstract, doi, and MID
    important_columns = config.COLUMN_DEFINITIONS['title'] + config.COLUMN_DEFINITIONS['abstract'] \
    + config.COLUMN_DEFINITIONS['doi'] + ['MID'] \
    + [col for col in annotation_df.columns if 'year' in col]
    annotation_df =  annotation_df[annotation_df.columns.intersection(important_columns)]

    sorted_df = sort_by_date(annotation_df)

    #remove records that were in previous calibration phases
    prior_calibration_df = pd.read_excel(prior_calibration_file)
    prior_mid = prior_calibration_df['MID']

    df = old_random_new(sorted_df, n_records, prior_mid)

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
        df.to_excel(annotator+".xlsx", index=False)


def sort_by_date(df):
    for c in df.columns:
        if 'year' in c:
            return df.sort_values(c, ascending=True)
    return
    


def old_random_new(df, n_records, prior_mid=[]):
    for c in df.columns:
        if 'year' in c:
            df = df[df[c].notnull()]

    n_records = int(n_records)
    try:
        if len(df) < n_records*2:
            raise ValueError("There are not enough (dated) records.")
        else:
            old = df[0:n_records]
            new = df[-n_records:len(df)]
            #remove all records with MID in prior_mid from df
            df = df[~df['MID'].isin(prior_mid)]

            random = df.sample(n=n_records, random_state=1)
            print(old)
            print(random)
            print(new)
            return pd.concat([old, random, new]).reset_index(drop=True)
    except ValueError as e:
        print(e)
        sys.exit(1)
    

def main():
    file = sys.argv[1]
    prior_file = sys.argv[2]
    n_records = sys.argv[3]
    annotators = sys.argv[4:]
    serve(file, prior_file, n_records, annotators)

if __name__ == "__main__":
    main()
