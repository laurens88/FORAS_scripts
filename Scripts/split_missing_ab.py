import pandas as pd
import sys

def main():
    file = sys.argv[1]
    ab_column = sys.argv[2]
    if '.xlsx' in file:
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    df_ma = df[df[ab_column].isna()]
    df_wa = df[~df[ab_column].isna()]

    if '.xlsx' in file:
        df_ma.to_excel("no_abstracts_"+file, index=False)
        df_wa.to_excel("with_abstracts_"+file, index=False)
    else:
        df_ma.to_csv("no_abstracts_"+file, index=False)
        df_wa.to_csv("with_abstracts_"+file, index=False)

if __name__ == '__main__':
    main()

