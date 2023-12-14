import pandas as pd



def main():
    df = pd.read_csv("Motherfile_1412.csv")

    for i in range(len(df)):
        df.iloc[i, df.columns.get_loc('MID')] = "M"+str(df.iloc[i, df.columns.get_loc('MID')])

    df.to_csv("Motherfile_1412_fixed.csv", index=False)

if __name__ == "__main__":
    main()