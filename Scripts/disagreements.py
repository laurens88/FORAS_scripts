import pandas as pd

df = pd.read_excel("Motherfile_270224.xlsx")

for i in range(len(df)):
    bruno = df.at[i, "TI-AB_final_label_Bruno"]
    bruno_overlap = df.at[i, "Overlap_Synergy_Bruno"]
    rutger = df.at[i, "TI-AB_final_label_Rutger"]

    if bruno in [0,1] and rutger in [0,1]:
        df.at[i, "TI-AB_disagreement"] = int(bruno != rutger)

    if bruno_overlap in [0,1] and rutger in [0,1]:
        df.at[i, "TI-AB_disagreement"] = int(bruno_overlap != rutger)

df.to_excel("Motherfile_270224.xlsx", index=False)