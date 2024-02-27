import pandas as pd

df = pd.read_excel("Motherfile_270224.xlsx")

for i in range(len(df)):
    df.at[i, "MID"] = "M"+str(df.at[i, "MID"])

df.to_excel("Motherfile_270224_V2.xlsx")