import pandas as pd

df = pd.read_excel("batches.xlsx")

print(df['MID'].value_counts(sort=True, ascending=False))