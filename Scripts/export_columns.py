import pandas as pd

mother = pd.read_excel('Motherfile_090524.xlsx')

columns = mother.columns

column_df = pd.DataFrame(columns, columns=['Columns'])

column_df.to_excel('Columns_explained.xlsx', index=False)