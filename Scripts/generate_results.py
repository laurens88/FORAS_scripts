import pandas as pd
import numpy as np

counts = pd.read_excel("270224_stats.xlsx")
inclusion_counts = pd.read_excel("inclusion_stats.xlsx")
columns_of_interest = ['Data_0_Synergy.csv', 'Data_1_old_replication.csv', 
                       'Data_2_old_comprehensive.csv', 'Data_4a_snowballing.csv', 
                       'Data_3a_inlusion_criteria.csv', 'Data_3b_includedrecords_top88.csv', 
                       'Data_3c_active_learning_total1000.csv']

#rename frequency to total_frequency
counts.rename(columns={'frequency': 'total_frequency'}, inplace=True)

#add and fill TI-AB_inclusion_frequency column
counts['TI-AB_inclusion_frequency'] = ""
for inclusion_row in range(len(inclusion_counts)):
    for counts_row in range(len(counts)):
        match = True
        for col in columns_of_interest:
            if counts.at[counts_row, col] != inclusion_counts.at[inclusion_row, col]:
                match = False
        if match:
            counts.at[counts_row, 'TI-AB_inclusion_frequency'] = inclusion_counts.at[inclusion_row, "frequency"]


#add FT_inclusion_frequency column
counts['FT_inclusion_frequency'] = np.nan

counts.to_excel("test.xlsx", index=False)