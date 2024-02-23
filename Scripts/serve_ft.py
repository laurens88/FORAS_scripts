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


def serve_ft(motherfile, annotators):
    if not annotators:
        print("No annotators were given.")
        return

    dataframe = pd.read_csv(motherfile, low_memory=False)

    annotation_df = dataframe

    #drop all columns except title, abstract, doi, and MID
    important_columns = config.COLUMN_DEFINITIONS['title'] + config.COLUMN_DEFINITIONS['abstract'] \
    + config.COLUMN_DEFINITIONS['doi'] + ['MID'] \
    + [col for col in annotation_df.columns if 'year' in col] \
    + ['first_authors']
    annotation_df =  annotation_df[annotation_df.columns.intersection(important_columns)]

    output_annotation_df(annotation_df, annotators)


def output_annotation_df(annotation_df, annotators):
    #add annotator columns to annotation dataframe
    for annotator in annotators:
        #create copy of dataframe for each annotator
        df = annotation_df.copy()

        #add full text annotation columns
        df[f'FT_IC1_{annotator}'] = np.nan
        df[f'FT_IC2_{annotator}'] = np.nan
        df[f'FT_IC3_{annotator}'] = np.nan
        df[f'FT_IC4_{annotator}'] = np.nan
        df[f'FT_other_exlusion_reason_{annotator}'] = np.nan
        df[f'FT_final_label_{annotator}'] = np.nan

        #output new annotation dataframe
        df = df.applymap(lambda x: x.encode('unicode_escape').
                 decode('utf-8') if isinstance(x, str) else x)
        df.to_excel(annotator+".xlsx", index=False)


def sort_by_date(df):
    for c in df.columns:
        if 'year' in c:
            return df.sort_values(c, ascending=True)
    return
    

def main():
    motherfile = sys.argv[1]
    annotators = sys.argv[2:]
    serve_ft(motherfile, annotators)


if __name__ == "__main__":
    main()
