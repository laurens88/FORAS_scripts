import pandas as pd

mother = pd.read_excel('Motherfile_230524_V6.xlsx')

FT_labels = pd.read_excel('FT_Screening_Bruno_labeled.xlsx')

mother['FT_inclusion'] = mother.apply(lambda row: FT_labels.loc[FT_labels['MID'] == row['MID'], 'FT_final_label_Bruno'].values[0] if row['MID'] in FT_labels['MID'].values else None, axis=1)

mother.to_excel('Motherfile_230524_V7.xlsx', index=False)