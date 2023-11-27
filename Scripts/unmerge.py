import pandas as pd
import sys

def unmerge(output_file, input_files):
    dataframe = pd.read_csv(output_file)
    source_columns = [col for col in dataframe.columns if ".csv" in col and not "include" in col]
    
    reconstructed_df_list = []
    for source_col in source_columns:
        df = dataframe[dataframe[source_col] == 1]
        reconstructed_df_list.append(df)
        # df.to_csv(source_col[:-4]+"_reconstructed.csv", index=False)  
    
    input_df_list = []
    for file in input_files:
        df = pd.read_csv(file)
        input_df_list.append(df)
    
    diff_df_list = []
    i = 0
    for df1, df2 in zip(input_df_list, reconstructed_df_list):
        merged = pd.merge(df1, df2, how='outer', indicator=True)
        diff = merged[merged['_merge'] == 'right_only']
        if not diff.empty:
            diff.to_csv(input_files[i][:-4]+"_diff.csv", index=False)
        i += 1
        # diff_df = pd.DataFrame(diff, columns=df1.columns)  # Convert the difference to a DataFrame
        # diff_df_list.append(diff_df)
        # df.to_csv(df1[:-4]+"_diff.csv", index=False)
    
    

def main():
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    unmerge(output_file, input_files)

if __name__ == "__main__":
    main()