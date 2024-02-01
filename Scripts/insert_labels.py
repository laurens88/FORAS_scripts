import sys
import re
import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype
from asreview import ASReviewData

CURSOR_UP = '\033[1A'
CLEAR = '\x1b[2K'
CLEAR_LINE = CURSOR_UP + CLEAR

def insert(motherfile:str, annotation_file:str):
    mother_frame = pd.read_csv(motherfile, low_memory=False)
    annotation_frame = pd.read_excel(annotation_file)

    mother_frame, label_columns = add_label_columns(mother_frame, annotation_frame)

    #loop through annotation file rows
    for annotation_row in range(len(annotation_frame)):
        print(f'Inserting: {annotation_row/len(annotation_frame)*100}%')
        print(CLEAR_LINE, end="")
    #     #loop through motherfile rows
        for mother_row in range(len(mother_frame)):
    #         #check if papers match
            if records_match(mother_frame, annotation_frame, mother_row, annotation_row):
                mother_frame = set_label_values(mother_frame, annotation_frame, mother_row, annotation_row, label_columns)
    
    mother_frame.to_csv(motherfile[:-4]+"+labels.csv", index=False)


#Add empty label columns to motherfile with names from annotation file
def add_label_columns(mother_df:pd.DataFrame, annotation_df:pd.DataFrame):
    label_columns = annotation_df.iloc[:,-7:].columns

    for column in label_columns:
        if not column in mother_df.columns:
            mother_df[column] = ""
    return mother_df, label_columns


def set_label_values(mother_frame: pd.DataFrame, annotation_frame: pd.DataFrame, mother_index: int, annotation_index: int, columns: list):
    #set values of columns from moterfile to those of annotation file
    for column in columns:
        mother_frame.iloc[mother_index, mother_frame.columns.get_loc(column)] = annotation_frame.iloc[annotation_index, annotation_frame.columns.get_loc(column)]
    return mother_frame


def records_match(df1: pd.DataFrame, df2: pd.DataFrame, index1: int, index2: int):
    mid1 = df1.iloc[index1, df1.columns.get_loc("MID")]
    mid2 = df2.iloc[index2, df2.columns.get_loc("MID")]
    return mid1 == mid2


def main():
    motherfile = sys.argv[1]
    annotation_file = sys.argv[2]
    insert(motherfile, annotation_file)


if __name__ == '__main__':
    main()
