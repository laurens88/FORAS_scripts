import pandas as pd

df = pd.read_excel("Batch_2.xlsx")
df['abstract']

df_ma = df[df['abstract'].isna()]
df_wa = df[~df['abstract'].isna()]

df_ma.to_excel("Batch2_no_abstracts.xlsx", index=False)
df_wa.to_excel("Batch2_with_abstracts.xlsx", index=False)


