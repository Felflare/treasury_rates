import pathlib
from datetime import datetime
import pandas as pd

CSV_FILE='ust.csv'
PATH = pathlib.Path(__file__).parent.absolute().parent
DATA_PATH = PATH.joinpath("data").resolve()
CSV_OUT_PATH = DATA_PATH.joinpath("yield_curve.csv")

def prepare_csv(csv_file):
    yield_curves = pd.read_csv(csv_file)
    yield_curves.drop("Unnamed: 12", axis=1, inplace=True)

    maturities = ["1-month", "3-month", "6-month", 
                 "1-year", "2-year", "3-year",
                 "5-year", "7-year", "10-year", 
                 "20-year", "30-year", ]
    maturities_df = pd.DataFrame({'maturities':maturities})

    final_df = pd.concat([maturities_df,yield_curves], ignore_index=True, axis=1)
    final_df.columns = ["x","y","z[0]","z[1]","z[2]","z[3]",
                       "z[4]","z[5]","z[6]","z[7]","z[8]",
                       "z[9]","z[10]",]
    return final_df

if __name__ == "__main__":
    df = prepare_csv(CSV_FILE)
    df.to_csv(CSV_OUT_PATH, index=False)
    print(f"Processed {CSV_FILE} on {datetime.today().strftime('%Y-%m-%d')}")
