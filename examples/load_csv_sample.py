import pathlib

import pandas as pd

# The directory is ../data/
CSV_DIR: pathlib.Path = pathlib.Path("../data")

# The file is ../data/SPY.csv
CSV_FILE: pathlib.Path = pathlib.Path(CSV_DIR, "SPY.csv")

df: pd.DataFrame = pd.read_csv(CSV_FILE, parse_dates=True, index_col=0)

print(df.head())
