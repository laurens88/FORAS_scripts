import sys
import pandas as pd
import numpy as np

def insert(motherfile:str, annotation_file:str, annotator:str):
    ...
    #get correct columns from motherfile and annotation file (.filter(like=annotator).columns)?
    #loop through annotation rows
    #   check if papers match
    #       set_label_values(mother_row, annotation_row)

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


def main():
    motherfile = sys.argv[1]
    annotation_file = sys.argv[2]
    annotator = sys.argv[3]
    insert(motherfile, annotation_file)


if __name__ == '__main__':
    main()
