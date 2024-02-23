import pandas as pd

df = pd.read_csv("Motherfile_200224 - Copy.csv")
         
count = 0
for i in range(len(df)):
    if df.at[i,'../Data/Data_0_Synergy.csv'] == 1 & df.at[i,'../Data/Data_1_old_replication.csv'] == 0 & \
    df.at[i,'../Data/Data_2_old_comprehensive.csv'] == 0 & df.at[i,'Data_4a_snowballing.csv'] == 0 & \
    df.at[i,'Data_3a_inlusion_criteria.csv'] == 0 & df.at[i, 'Data_3b_includedrecords_top88.csv'] == 0 & df.at[i,'Data_3c_active_learning_total1000.csv'] == 0:
            count += 1
print(count)