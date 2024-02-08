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




<br>
<br>
<br>
<br>


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

| Title                        | Pub Year | record DOI           | Included | Unnamed: 4 |
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



# Serve script

## Introduction
The FORAS Project serving script is designed to facilitate the sampling and distribution of records for annotation by multiple annotators. This script takes a dataset, filters out previously annotated records, and randomly selects a specified number of new records to be annotated. Each annotator receives a personalized Excel file with the records to annotate, ensuring an efficient and organized annotation process.

## Features
- **Prior Calibration Filtering:** Excludes records already annotated in previous batches.
- **Random Sampling:** Randomly selects a specified number of records for annotation.
- **Annotation File Generation:** Generates personalized Excel files for each annotator with the records to be annotated.
- **Important Column Preservation:** Retains only essential columns such as title, abstract, DOI, and MID.

## Requirements
- Python 3.x
- Libraries: `pandas`, `numpy`, `argparse`, `warnings`, `pathlib`, `sys`
- ASReview (`asreview`) for handling systematic review data configurations

## Installation
Ensure you have Python installed on your system along with the required libraries. You can install the necessary Python libraries using pip:

```
pip install pandas numpy argparse asreview
```

## Usage
This script is executed from the command line, taking the dataset file, a prior calibration file, the number of records to sample, and the list of annotators as arguments.

### Command Line Syntax
```bash
python serve_script.py <dataset_file.csv> <prior_calibration_file.xlsx> <n_records> <annotator1> [<annotator2> ...]
```

### Example
```bash
python serve_script.py dataset.csv prior_annotations.xlsx 100 JohnDoe JaneDoe
```

This command will sample 100 records from `dataset.csv`, excluding any records found in `prior_annotations.xlsx`, and generate `JohnDoe.xlsx` and `JaneDoe.xlsx` for the annotators John Doe and Jane Doe respectively.

## Function Descriptions
- `serve(file, prior_calibration_file, n_records, annotators)`: Main function for sampling and serving records for annotation.
- `output_annotation_df(annotation_df, annotators)`: Generates personalized annotation Excel files for each annotator.
- `sort_by_date(df)`: Placeholder function for future implementation to sort records by date.
- `sample(df, n_records, prior_mid)`: Samples a specified number of records, excluding those with MIDs found in the prior calibration file.
- `main()`: Entry point of the script, parsing command line arguments and initiating the serving process.

## Output Files
- **Annotator Excel Files:** Each annotator specified in the command line arguments will receive an Excel file named after them containing the records to annotate. These files include columns for recording annotations related to title eligibility, inclusion criteria, and any other exclusion reasons.

# Serve vocabulary script

## Introduction
The FORAS Project Serve Vocabulary script is specifically designed for the early calibration phase of annotation. Its primary function is to provide annotators with a diverse set of records from a dataset to examine the evolution of terms and concepts over time. The script selects 100 of the oldest records, 100 random records, and 100 of the newest records from the dataset, aiming to capture the variance in vocabulary and thematic focus across different periods.

## Features
- **Vocabulary Calibration:** Helps identify changes in terms and concepts throughout the years within a dataset.
- **Targeted Record Selection:** Selects records from three distinct time periods: oldest, random, and newest.
- **Exclusion of Previously Annotated Records:** Ensures that records previously used in calibration are not included again.
- **Annotator-Specific Files:** Generates personalized Excel files for each annotator with the selected records.

## Requirements
- Python 3.x
- Libraries: `pandas`, `numpy`, `argparse`, `warnings`, `pathlib`, `sys`
- ASReview (`asreview`) for systematic review data configurations

## Installation
Ensure Python and the required libraries are installed on your system. Install the necessary Python libraries using pip:

```
pip install pandas numpy asreview
```

## Usage
This script is executed from the command line, accepting the dataset file, a prior calibration file, the number of records to sample, and the list of annotators as arguments.

### Command Line Syntax
```bash
python serve_vocabulary_script.py <dataset_file.csv> <prior_calibration_file.xlsx> <n_records> <annotator1> [<annotator2> ...]
```

### Example
```bash
python serve_vocabulary_script.py dataset.csv prior_annotations.xlsx 100 JohnDoe JaneDoe
```

This command will process `dataset.csv`, excluding records found in `prior_annotations.xlsx`, and generate `JohnDoe.xlsx` and `JaneDoe.xlsx` for the annotators John Doe and Jane Doe, respectively. Each file will contain 300 records, including the oldest, randomly selected, and newest records from the dataset.

## Function Descriptions
- `serve(file, prior_calibration_file, n_records, annotators)`: Main function for selecting and serving records for vocabulary calibration.
- `output_annotation_df(annotation_df, annotators)`: Generates personalized annotation Excel files for each annotator.
- `sort_by_date(df)`: Sorts the dataframe by the year column in ascending order.
- `old_random_new(df, n_records, prior_mid)`: Selects old, random, and new records from the dataframe.
- `main()`: Entry point of the script, parsing command line arguments and initiating the record serving process.

## Output Files
- **Annotator Excel Files:** Each annotator specified in the command line arguments will receive an Excel file containing the selected records for annotation. These files include necessary columns for recording annotations related to title eligibility, inclusion criteria, and other exclusion reasons.

# Insert labels script

## Introduction
The FORAS Project Insert Labels script is designed to integrate annotations from annotator-specific files back into the main dataset, referred to as the "motherfile". This process is crucial for consolidating annotated data, facilitating analysis, and ensuring that all annotations are accurately reflected in the central dataset. The script matches records based on a unique identifier (MID), then inserts the corresponding labels and batch information from the annotation file into the motherfile.

## Features
- **Label Column Integration:** Adds empty label columns to the motherfile based on names from the annotation file.
- **Record Matching:** Identifies matching records between the annotation file and the motherfile using the MID.
- **Label Insertion:** Inserts label values and batch information from the annotation file into the corresponding records in the motherfile.

## Requirements
- Python 3.x
- Libraries: `pandas`, `numpy`, `sys`, `re`
- ASReview (`asreview`) for handling systematic review data configurations

## Installation
Ensure Python and the necessary libraries are installed on your system. You can install the required Python libraries using pip:

```
pip install pandas numpy asreview
```

## Usage
This script is executed from the command line, taking the motherfile name, the annotation file name, and the batch identifier as arguments.

### Command Line Syntax
```bash
python insert_labels_script.py <motherfile.csv> <annotation_file.xlsx> <batch>
```

### Example
```bash
python insert_labels_script.py dataset.csv JohnDoe_annotations.xlsx Batch1
```

This command will process `JohnDoe_annotations.xlsx`, matching its records with those in `dataset.csv` based on MID, and insert the annotations along with the batch identifier (Batch1) into the motherfile.

## Function Descriptions
- `insert(motherfile, annotation_file, batch)`: Main function to insert label values from the annotation file into the motherfile.
- `add_label_columns(mother_df, annotation_df)`: Adds empty label columns to the motherfile based on the annotation file.
- `set_label_values(mother_frame, annotation_frame, mother_index, annotation_index, columns, batch)`: Inserts label values and batch information into the motherfile.
- `records_match(df1, df2, index1, index2)`: Checks if records in two dataframes match based on MID.
- `main()`: Entry point of the script, parsing command line arguments and initiating the label insertion process.

## Output File
- **Updated Motherfile:** The script outputs an updated version of the motherfile with added labels from the annotation file and batch information. The file is saved with a "+labels.csv" suffix to denote that labels have been inserted.

## Note
These scripts are part of the FORAS Project, aimed at streamlining the preparation of datasets for systematic reviews and analysis.
These scripts are intended for use in research and systematic reviews.
