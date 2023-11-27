### Merge script: Functions and Their Roles

### Preprocess script: Functions and Their Roles
1. **`preprocess(file, output_file)`:** Main function to preprocess the dataset.
    - Reads a CSV file.
    - Applies various cleaning and standardization functions.
    - Saves the processed data to a new CSV file.
2. **`clean_columns(dataframe)`:** Removes columns that are either empty or have the name "Unnamed".
3. **`generalize_title_column(dataframe)`:** Standardizes the column name for titles using a mapping from `config.COLUMN_DEFINITIONS`.
4. **`generalize_year_column(dataframe)`:** Renames any column containing 'year' in its name to 'year'.
5. **`generalize_doi_column(dataframe)`:** Renames columns related to DOI (Digital Object Identifier) to a standard 'doi' name.
6. **`prepare_label_column(dataframe)`:** Processes columns related to inclusion criteria.
    - Replaces -1 with None (missing values).
    - Renames the column to include the file name.
7. **`clean_doi_column(dataframe)`:** Cleans the DOI column.
    - Converts to string.
    - Removes URL parts from DOI strings.
