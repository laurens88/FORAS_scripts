import pandas as pd

mother = pd.read_excel('Motherfile_210524_V2.xlsx')

labels_rutger = mother[(mother['TI-AB_final_label_Rutger'] == 0) | (mother['TI-AB_final_label_Rutger'] == 1)].index


mother['TI-AB_disagreement'][labels_rutger] = mother['TI-AB_final_label_Rutger'][labels_rutger] != mother['TI-AB_final_label_Bruno'][labels_rutger]

mother['TI-AB_disagreement'] = mother['TI-AB_disagreement'].apply(lambda x: int(x) if pd.notnull(x) else x)

mother.to_excel('Motherfile_210524_V3.xlsx', index=False)