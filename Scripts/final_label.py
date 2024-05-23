import pandas as pd

mother = pd.read_excel('Motherfile_230524.xlsx')

for i in range(len(mother)):
    if mother.loc[i, 'TI-AB_disagreement'] != 0 and not pd.isnull(mother.loc[i, 'TI-AB_final_label_Bruno']):
        mother.loc[i, 'TI-AB_final_label'] = mother.loc[i, 'TI-AB_final_label_Bruno']
    elif mother.loc[i, 'TI-AB_disagreement'] == 0:
        mother.loc[i, 'TI-AB_final_label'] = mother.loc[i, 'TI-AB_final_label_Bruno']
    else:
        mother.loc[i, 'TI-AB_final_label'] = mother.loc[i, 'Synergy_TI-AB_inclusion']
                                     
mother.to_excel('Motherfile_230524_V4.xlsx', index=False)