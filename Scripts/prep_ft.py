import pandas as pd
import numpy as np

df = pd.read_csv('Motherfile_200224_dedup.csv')

df = df[df['TI-AB_final_label_Bruno'] == 1]



annotator = 'Bruno'
df[f'FT_IC1_{annotator}'] = np.nan
df[f'FT_IC2_{annotator}'] = np.nan
df[f'FT_IC3_{annotator}'] = np.nan
df[f'FT_IC4_{annotator}'] = np.nan
df[f'FT_other_exlusion_reason_{annotator}'] = np.nan
df[f'FT_final_label_{annotator}'] = np.nan
df['duplicate'] = np.nan
df['clinical'] = np.nan
df['distal'] = np.nan

df.to_excel('FT_Screening_Bruno.xlsx')