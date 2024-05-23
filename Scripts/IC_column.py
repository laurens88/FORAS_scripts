import pandas as pd

mother = pd.read_excel('Motherfile_230524_V4.xlsx')

tiab_agreements = mother[mother['TI-AB_disagreement'] != 1].index

mother['TI_final_label'][tiab_agreements] = mother['title_eligible_Bruno'][tiab_agreements]
mother['TI-AB_IC1_final'][tiab_agreements] = mother['TI-AB_IC1_Bruno'][tiab_agreements]
mother['TI-AB_IC2_final'][tiab_agreements] = mother['TI-AB_IC2_Bruno'][tiab_agreements]
mother['TI-AB_IC3_final'][tiab_agreements] = mother['TI-AB_IC3_Bruno'][tiab_agreements]
mother['TI-AB_IC4_final'][tiab_agreements] = mother['TI-AB_IC4_Bruno'][tiab_agreements]

mother.to_excel('Motherfile_230524_V5.xlsx', index=False)