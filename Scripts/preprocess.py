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
import re

def preprocess(file, output_file):
    dataframe = pd.read_csv(file)
    dataframe.name = file

    dataframe = generalize_title_column(dataframe)
    dataframe = generalize_year_column(dataframe)
    dataframe = generalize_doi_column(dataframe)
    dataframe = prepare_label_column(dataframe)
    dataframe = clean_doi_column(dataframe)
    dataframe = clean_columns(dataframe)

    dataframe.to_csv(output_file, index=False)


def clean_columns(dataframe):
    columns_to_drop = [c for c in dataframe.columns if len(c)==0 or "Unnamed" in c]
    return dataframe.drop(columns_to_drop, axis=1)


def generalize_title_column(dataframe):
    title_mapping = {'title': config.COLUMN_DEFINITIONS['title']}
    reverse_dict = {item: key for key, value_list in title_mapping.items() for item in value_list}
    dataframe.rename(columns=reverse_dict, inplace=True)
    return dataframe


def generalize_year_column(dataframe):
    for col in dataframe.columns:
         if 'year' in col:
            dataframe.rename(columns={col: 'year'}, inplace=True)
    return dataframe


def generalize_doi_column(dataframe):
    for col in dataframe.columns:
        if 'DOI' in col or 'Doi' in col:
            dataframe.rename(columns={col: 'doi'}, inplace=True)
    return dataframe

def prepare_label_column(dataframe):
    for included_column in config.COLUMN_DEFINITIONS['included']:
        if included_column in dataframe.columns:
            #Remove -1 labels
            dataframe[included_column] = dataframe[included_column].replace(-1, None)
            #rename included column to include file name
            dataframe.rename(columns={included_column: 'included_'+dataframe.name}, inplace=True) #change dataframe to dataframe.name?
    return dataframe


def clean_doi_column(dataframe):
     dataframe['doi'] = dataframe['doi'].astype(str)
     dataframe['doi'] = dataframe['doi'].fillna(np.nan)

    #  for index, row in dataframe.iterrows():
    #      doi = dataframe.iloc[index, dataframe.columns.get_loc('doi')]
    #      dataframe.iloc[index, dataframe.columns.get_loc('doi')] = clean_doi(str(doi))

     dataframe['doi'] = dataframe['doi'].apply(lambda doi: re.sub(r'^https?:\/\/(www\.)?doi\.org\/', "", doi))
     return dataframe


def main():
    file = sys.argv[1]
    output_file = sys.argv[2]
    preprocess(file, output_file)

if __name__ == "__main__":
    main()
