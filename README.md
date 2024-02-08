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

## Introduction
The FORAS Project preprocessing script is designed for cleaning and standardizing datasets before they are used for systematic reviews or data analysis. This script focuses on generalizing column names, cleaning data, and preparing datasets for further processing. It supports CSV input files and outputs the processed data to a specified CSV file.

## Features
- **Column Generalization:** Renames columns to standard names for titles, years, and DOIs.
- **Label Preparation:** Prepares the label column by renaming and cleaning values.
- **DOI Cleaning:** Cleans and standardizes DOI column values.
- **Column Cleaning:** Removes unnecessary columns from the dataset.

## Requirements
- Python 3.x
- Libraries: `pandas`, `numpy`, `argparse`, `warnings`, `pathlib`, `sys`, `re`
- ASReview (`asreview`) for handling systematic review data configurations

## Installation
Ensure you have Python installed on your system along with the required libraries. You can install the necessary Python libraries using pip:

```
pip install pandas numpy argparse asreview
```

## Usage
This script is executed from the command line, taking the input file name and the output file name as arguments.

### Command Line Syntax
```bash
python preprocess_script.py <input_file.csv> <output_file.csv>
```

### Example
```bash
python preprocess_script.py dataset.csv cleaned_dataset.csv
```

This command will preprocess `dataset.csv` and save the cleaned and standardized data to `cleaned_dataset.csv`.

## Function Descriptions
- `preprocess(file, output_file)`: Main function for preprocessing the input CSV file.
- `clean_columns(dataframe)`: Removes unnecessary columns from the dataframe.
- `generalize_title_column(dataframe)`: Standardizes the column name for titles.
- `generalize_year_column(dataframe)`: Standardizes the column name for years.
- `generalize_doi_column(dataframe)`: Standardizes the column name for DOIs.
- `prepare_label_column(dataframe)`: Prepares the label column by renaming and cleaning.
- `clean_doi_column(dataframe)`: Cleans DOI column values.
- `main()`: Entry point of the script.

### Before Preprocessing
The original dataset (`dataset.csv`) might have entries with varying column names, missing data, and unstandardized formats. For example:

| Title                        | Pub Year | Document Object Identifier           | Included | Unnamed: 4 |
|------------------------------|----------|--------------------------------------|----------|------------|
| Sample Research Article      | 2020     | https://doi.org/10.1000/journal.2020 | 1        | NaN        |
| Another Research Article     | 2019     | 10.1001/journal.2019                 | -1       | NaN        |

- Column names are inconsistent (e.g., "Pub Year" instead of "year").
- The DOI column includes prefixes and is not lowercase.
- The "Included" column contains `-1` for indicating exclusion, which is not standard.
- There is an unnecessary column ("Unnamed: 4").

### After Preprocessing
After running `python preprocess_script.py dataset.csv cleaned_dataset.csv`, the dataset is cleaned and standardized:

| title                      | year | doi                 | included_dataset.csv | 
|----------------------------|------|---------------------|----------------------|
| Sample Research Article    | 2020 | 10.1000/journal.2020| 1                     |
| Another Research Article   | 2019 | 10.1001/journal.2019|                       |

- Column names are standardized to "title", "year", "doi", and "included_dataset.csv" to reflect the source file and inclusion status.
- The DOI is cleaned to remove the URL prefix and is all lowercase.
- The "Included" column is renamed to "included_dataset.csv" and `-1` values are replaced with blanks to indicate exclusion more clearly.
- Unnecessary columns are removed.

This example demonstrates how the preprocessing script standardizes dataset entries, making them cleaner and more consistent for subsequent analysis or systematic review processes.

## Output File
- **Processed Dataset:** A CSV file containing the preprocessed dataset with standardized column names and cleaned data.

## Note
This preprocessing script is part of the FORAS Project, aimed at streamlining the preparation of datasets for systematic reviews and analysis. It simplifies the initial data cleaning steps, ensuring consistency and ease of use in subsequent analyses.

# Serve script


# Serve vocabulary script


# Insert labels script
