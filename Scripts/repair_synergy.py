import pandas as pd

mother = pd.read_excel('Motherfile_090524.xlsx')

for index, row in mother.iterrows():
    if row['Data_0_Synergy.csv'] == 1 and str(row['Synergy_TI-AB_inclusion']) == 'nan':
        mother.at[index, 'Synergy_TI-AB_inclusion'] = 0

mother.to_excel('Motherfile_090524_repaired.xlsx', index=False)