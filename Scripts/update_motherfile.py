import pandas as pd

mother = pd.read_excel('Motherfile_290424.xlsx')

rutger = pd.read_excel('rutger_labels.xlsx')

columns_to_drop = rutger.columns[1:-4]
rutger.drop(columns=columns_to_drop, inplace=True)

merged_df = pd.merge(mother, rutger, on='MID')


merged_df.to_excel('Motherfile_070524.xlsx', index=False)