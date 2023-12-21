import pandas as pd
import sys

def counts(dataframe):
    source_cols = [col for col in dataframe.columns if 'Data_' in col and 'included' not in col]
    df = dataframe[source_cols]
    df['row_as_str'] = df.apply(lambda row: ''.join(row.values.astype(int).astype(str)), axis=1)

    # Count the frequency of each unique row
    df_freq = df['row_as_str'].value_counts().reset_index()
    df_freq.columns = ['row_as_str', 'frequency']

    print(df_freq)

    # Convert the string rows back to a DataFrame
    df_freq = df_freq.join(df_freq['row_as_str'].apply(lambda x: pd.Series(list(x))))
    df_freq = df_freq.drop(columns=['row_as_str'])

    print(df_freq)


def main():
    dataframe = pd.read_csv(sys.argv[1])
    counts(dataframe)


if __name__ == '__main__':
    main()
