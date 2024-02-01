import pandas as pd
import sys

def source_counts(dataframe, output_file):
    source_cols = [col for col in dataframe.columns if 'Data_' in col and 'included_' not in col]
    df = dataframe[source_cols]
    df['row_as_str'] = df.apply(lambda row: ''.join(row.values.astype(int).astype(str)), axis=1)

    # Count the frequency of each unique row
    df_freq = df['row_as_str'].value_counts().reset_index()
    df_freq.columns = ['row_as_str', 'frequency']

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    with open(output_file[:-4]+'.txt', 'a') as file:
        original_stdout = sys.stdout
        sys.stdout = file
        print(df_freq)
        # df_freq.to_csv("../Output/stats_"+output_file, index=False)

        # Convert the string rows back to a DataFrame
        df_freq = df_freq.join(df_freq['row_as_str'].apply(lambda x: pd.Series(list(x))))
        df_freq = df_freq.drop(columns=['row_as_str'])

        print()
        print(df_freq)
        sys.stdout = original_stdout


def main():
    dataframe = pd.read_csv(sys.argv[1])
    output_file = sys.argv[2]
    source_counts(dataframe, output_file)


if __name__ == '__main__':
    main()
