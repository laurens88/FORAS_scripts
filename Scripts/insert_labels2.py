import pandas as pd
import sys

def optimized_insert(motherfile: str, annotation_file: str, annotator: str):
    mother_frame = pd.read_csv(motherfile, low_memory=False)
    annotation_frame = pd.read_excel(annotation_file)
    
    # Convert relevant columns to strings
    mother_frame['abstract'] = mother_frame['abstract'].astype(str)
    mother_frame['title'] = mother_frame['title'].astype(str)
    annotation_frame['abstract'] = annotation_frame['abstract'].astype(str)
    annotation_frame['title'] = annotation_frame['title'].astype(str)

    merged_frame = mother_frame.merge(annotation_frame, on='MID', how='left', suffixes=('', '_annot'))

    # Update only the specified columns
    annotation_columns = annotation_frame.filter(like=annotator).columns
    for column in annotation_columns:  # Replace with your actual columns
        mother_frame[column] = merged_frame[column + '_annot']

    # Save the updated frame
    mother_frame.to_csv(motherfile[:-4] + "+labels.csv")

def main():
    motherfile = sys.argv[1]
    annotationfile = sys.argv[2]
    annotator = sys.argv[3]
    optimized_insert(motherfile, annotationfile, annotator)

if __name__ == '__main__':
    main()