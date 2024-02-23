import pandas as pd
from pyalex import Works

df = pd.read_excel("Motherfile_230224.xlsx")

for i in range(len(df)):
    doi = "doi.org/"+str(df.at[i, "doi"])
    print(100*i/len(df))
    if doi != "doi.org/nan":
        try:
            openalex_id = Works()[doi]['id']
            df.at[i, 'openalex_id'] = openalex_id
        except:
            print(f"No OpenAlex Id found for DOI: {doi}.")

df.to_excel("Motherfile_230224_V2.xlsx", index=False)