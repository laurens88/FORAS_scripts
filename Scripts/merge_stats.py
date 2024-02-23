import pandas as pd
import sys

def source_counts(dataframe, output_file):
    columns_of_interest = ['../Data/Data_0_Synergy.csv', '../Data/Data_1_old_replication.csv', 
                       '../Data/Data_2_old_comprehensive.csv', 'Data_4a_snowballing.csv', 
                       'Data_3a_inlusion_criteria.csv', 'Data_3b_includedrecords_top88.csv', 
                       'Data_3c_active_learning_total1000.csv']
    df = dataframe[columns_of_interest]
    df['row_as_str'] = df.apply(lambda row: ''.join(row.values.astype(int).astype(str)), axis=1)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Count the frequency of each unique row
    df_freq = df['row_as_str'].value_counts().reset_index()

    df_freq.columns = ['row_as_str', 'frequency']

    for i in range(len(df_freq)):
        for j in range(7):
            df_freq.at[i, columns_of_interest[j]] = df_freq.at[i, 'row_as_str'][j]
    
    df_freq = df_freq.drop(columns='row_as_str')

    cols = df_freq.columns.tolist()
    cols.append(cols.pop(cols.index('frequency')))
    df_freq = df_freq[cols]

    df_freq.to_excel(output_file, index=False)


def main():
    dataframe = pd.read_excel(sys.argv[1])
    output_file = sys.argv[2]
    source_counts(dataframe, output_file)


if __name__ == '__main__':
    main()
