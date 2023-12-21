import pandas as pd
import sys

def unmerge(output_file, input_files):
    dataframe = pd.read_csv(output_file)
    source_columns = [col for col in dataframe.columns if ".csv" in col and not "include" in col]
    
    reconstructed_df_list = []
    for source_col in source_columns:
        df = dataframe[dataframe[source_col] == 1]
        reconstructed_df_list.append(df)
        df.to_csv(source_col[:-4]+"_reconstructed.csv", index=False)  
    

def main():
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    unmerge(output_file, input_files)

if __name__ == "__main__":
    main()