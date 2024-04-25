import pandas as pd

mother = pd.read_excel("Motherfile_100424.xlsx")
title_df = pd.read_excel('titles.xlsx')
not_found = pd.DataFrame(columns=['title'])

for title in title_df['Paper Title']:
    match = False
    for mother_title in mother['title']:
        title_clean = str(title).lower().strip().replace(" ", "").replace(".", "").replace(",", "")
        mother_title_clean = str(mother_title).lower().strip().replace(" ", "").replace(".", "").replace(",", "")
        if title_clean == mother_title_clean:
            match = True
            # print the row number of the motherfile that matches the title
            mother_index =mother[mother['title'] == mother_title].index
            print(mother_title)
            print(title)
            #set MID column of mother to "YYY" at mother_index
            mother.loc[mother_index, 'MID'] = "YYY"

    if match is False:
        not_found.loc[len(not_found), 'title'] = title
not_found.to_excel('not_found.xlsx', index=False)
mother.to_excel('Motherfile_altered.xlsx', index=False)
