import sys
import re
import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype
from asreview import ASReviewData

CURSOR_UP = '\033[1A'
CLEAR = '\x1b[2K'
CLEAR_LINE = CURSOR_UP + CLEAR

def insert(motherfile:str, annotation_file:str, batch:str, suffix:str):
    mother_frame = pd.read_excel(motherfile, low_memory=False)
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
                mother_frame = set_label_values(mother_frame, annotation_frame, mother_row, annotation_row, label_columns, batch)
    
    mother_frame.to_excel(motherfile[:-5]+suffix+".xlsx", index=False)


#Add empty label columns to motherfile with names from annotation file
def add_label_columns(mother_df:pd.DataFrame, annotation_df:pd.DataFrame):
    label_columns = annotation_df.iloc[:,-7:].columns

    for column in label_columns:
        if not column in mother_df.columns:
            mother_df[column] = ""

    if not "Batch" in mother_df.columns:
        mother_df["Batch"] = ""
    return mother_df, label_columns


def set_label_values(mother_frame: pd.DataFrame, annotation_frame: pd.DataFrame, mother_index: int, annotation_index: int, columns: list, batch):
    #set values of columns from moterfile to those of annotation file
    if mother_frame.iloc[mother_index, mother_frame.columns.get_loc(columns[-1])] in [0, 1]:
        print(f'Already a label in motherfile entry with MID {mother_frame.at[mother_index, "MID"]}')
    else:
        for column in columns:
            mother_frame.iloc[mother_index, mother_frame.columns.get_loc(column)] = annotation_frame.iloc[annotation_index, annotation_frame.columns.get_loc(column)]
    mother_frame.iloc[mother_index, mother_frame.columns.get_loc('Batch')] = batch
    return mother_frame


def records_match(df1: pd.DataFrame, df2: pd.DataFrame, index1: int, index2: int):
    mid1 = df1.iloc[index1, df1.columns.get_loc("MID")]
    mid2 = df2.iloc[index2, df2.columns.get_loc("MID")]
    return mid1 == mid2


def main():
    motherfile = sys.argv[1]
    annotation_file = sys.argv[2]
    batch = sys.argv[3]
    suffix = sys.argv[4]
    insert(motherfile, annotation_file, batch, suffix)


if __name__ == '__main__':
    main()
