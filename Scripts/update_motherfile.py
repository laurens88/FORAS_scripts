import pandas as pd

mother = pd.read_excel('Motherfile_210524_V1.xlsx')

print(mother['TI-AB_final_label_Rutger'].sum())

indici = mother[mother['TI-AB_final_label_Rutger'].isnull()].index


mother['TI-AB_final_label_Rutger'][indici] = mother['TI-AB_included_ASReview'][indici]
    

mother.to_excel('Motherfile_210524_V2.xlsx', index=False)