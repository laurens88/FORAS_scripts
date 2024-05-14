import pandas as pd

mother = pd.read_excel('Motherfile_130524.xlsx')

def rule1(row):
    return row['Synergy_TI-AB_inclusion'] == 1

def rule2(row):
    return row['Batch'] == "Calibration1" and row['TI-AB_final_label_Rutger'] == 1

def rule3(row):
    return row['Batch'] == "Calibration2" and row['TI-AB_final_label_Bruno'] == 1

def rule4(row):
    return row['Batch'] == "Calibration2" and row['TI-AB_final_label_Rutger'] == 1 and row['TI-AB_final_label_Bruno'] == 0

def rule5(row):
    return str(row['Batch'])[0] == "B" and row['TI-AB_final_label_Bruno'] == 1

def rule6(row):
    return row['included']-row['asreview_prior'] == 1

def rule7(row):
    return row['Synergy_TI-AB_inclusion'] == 0

def rule8(row):
    return row['title_eligible_Bruno'] == "N"

mother['TIAB_origin'] = [[] for _ in range(len(mother))]


for index, row in mother.iterrows():
    rule9 = True
    if rule1(row):
        rule9 = False
        mother.at[index, 'TIAB_origin'] = mother.at[index, 'TIAB_origin'] + [1]

    if rule2(row):
        rule9 = False
        mother.at[index, 'TIAB_origin'] = mother.at[index, 'TIAB_origin'] + [2]
    
    if rule3(row):
        rule9 = False
        mother.at[index, 'TIAB_origin'] = mother.at[index, 'TIAB_origin'] + [3]

    if rule4(row):
        rule9 = False
        mother.at[index, 'TIAB_origin'] = mother.at[index, 'TIAB_origin'] + [4]

    if rule5(row):  
        rule9 = False
        mother.at[index, 'TIAB_origin'] = mother.at[index, 'TIAB_origin'] + [5]

    if rule6(row):
        rule9 = False
        mother.at[index, 'TIAB_origin'] = mother.at[index, 'TIAB_origin'] + [6]

    if rule7(row):
        rule9 = False
        mother.at[index, 'TIAB_origin'] = mother.at[index, 'TIAB_origin'] + [777]

    if rule8(row):
        rule9 = False
        mother.at[index, 'TIAB_origin'] = mother.at[index, 'TIAB_origin'] + [888]

    if rule9:
        mother.at[index, 'TIAB_origin'] = mother.at[index, 'TIAB_origin'] + [999]
    

mother.to_excel('Motherfile_130524_V2.xlsx', index=False)