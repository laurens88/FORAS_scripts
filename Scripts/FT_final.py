import pandas as pd

mother = pd.read_excel('Motherfile_230524_V9.xlsx')

mother['FT_inclusion_final'] = (mother['Synergy_FT_inclusion_corrected'] == 1) | (mother['FT_inclusion_Bruno'] == 1) | (mother['FT_inclusion_X'] == 1)
mother['FT_inclusion_final'] = mother['FT_inclusion_final'].astype(int)
# mother['FT_inclusion_final'] = mother['FT_inclusion_final'].fillna(0).astype(int)

mother.to_excel('Motherfile_230524_V10.xlsx', index=False)