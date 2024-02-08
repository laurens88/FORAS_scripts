# Merge script

## Introduction
This script can be used to merge scientific paper datasets of `.csv` format whilst keeping track of where duplicates originate from. Besides a merged output file, the script also produces a copy of the subset of papers which do not have an abstract, and a `.txt` file describing the number of unique records from each input set and the number of records found for every combination of input sets.

## Features
- **Data Merging:** Combines multiple datasets into a single file.
- **Source Column Filling:** Marks the source file for each data entry.
- **Duplicate Removal:** Identifies and removes duplicate entries based on titles, abstracts, and DOIs.
- **Annotation File Creation:** Generates files for missing abstracts with columns for annotator judgments.
- **Statistics Generation:** Outputs statistics about the input and merged datasets.

## Requirements
- Python 3.x
- Libraries: `pandas`, `numpy`, `matplotlib`, `argparse`, `warnings`, `pathlib`, `re`, `sys`
- ASReview (`asreview`) for handling systematic review data

## Installation
Before running the script, ensure you have Python installed and the required libraries. You can install the required Python libraries using pip:

```
pip install pandas numpy matplotlib argparse asreview
```

## Usage
To use the script, you must have Python installed on your system. The script is executed from the command line with the output file name and the list of input files as arguments.

### Command Line Syntax
```bash
python foras_project.py <output_file> <input_file1> <input_file2> ... <input_fileN>
```

### Example
```bash
python foras_project.py merged_output.csv dataset1.csv dataset2.csv dataset3.csv
```

This command merges `dataset1.csv`, `dataset2.csv`, and `dataset3.csv` into a new file named `merged_output.csv`.

## Function Descriptions
- `merge(output_file, input_files)`: Main function to merge input files into a single output file.
- `output_annotation_df(annotation_df, annotators, output_file)`: Creates annotation files for missing abstracts.
- `fill_source_columns(dataframe, column_names)`: Fills source columns in the merged dataframe.
- `assign_mother_id(df)`: Assigns a unique mother ID to each entry.
- `clean_columns(dataframe)`: Cleans up unnecessary columns from the dataframe.
- `count_unique_records(dataframe)`: Counts unique records in the merged dataset.
- `source_counts(dataframe, output_file)`: Counts the number of sources for each entry.
- `duplicated(asrdata, pid='doi')`: Identifies duplicate entries based on DOI or text content.
- `drop_duplicates(asrdata, pid='doi', inplace=False, reset_index=True)`: Removes duplicate entries from the dataset.
- `main()`: Entry point of the script.

## Output Files
- **Merged Dataset:** A CSV file containing the merged records.
- **Missing Abstracts File:** Excel files for each annotator with records missing abstracts.
- **Statistics File:** A text file containing statistics about the inupt datasets and the merged dataset.

## Note
This script is intended for use in research and systematic reviews. It simplifies the process of merging and cleaning datasets from different sources, making systematic reviews more efficient.

# Preprocess script


# Serve script


# Serve vocabulary script


# Insert labels script
