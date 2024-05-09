import pandas as pd

mother = pd.read_excel('Motherfile_070524.xlsx')

bruno = pd.read_excel('FT_Screening_Bruno_labeled.xlsx')

mother['A'] = 0  # Add a new column 'A' initialized with 0

for index, row in bruno.iterrows():
    print(index)
    for i, r in mother.iterrows():
        if row['MID'] == r['MID']:
            mother.at[i, 'A'] = 1
    
    

mother.to_excel('Motherfile_090524.xlsx', index=False)