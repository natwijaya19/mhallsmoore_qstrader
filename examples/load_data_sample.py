import pathlib

import pandas as pd

csv_dir = pathlib.Path("..", "data")
csv_file = "SPY.csv"
file_path = pathlib.Path(csv_dir, csv_file)
csv_df = pd.read_csv(file_path, index_col="Date", parse_dates=True).sort_index()
print(f"csv_df: {csv_df}")
