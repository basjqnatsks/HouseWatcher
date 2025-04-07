import pandas as pd

# 1) Read the pivoted CSV
df = pd.read_csv("pivoted_simulator_data.csv")

# 2) Locate the row for 1995-01-02.
#    We expect exactly one row to match this condition; use .iloc[0] to get that row as a Series.
row_19950102 = df[df["dateprice"] == "1995-01-03"]
if row_19950102.empty:
    raise ValueError("No row found for dateprice == 1995-01-03!")
row_19950102 = row_19950102.iloc[0]

# 3) Identify columns that have -1 on that date
cols_to_remove = []
for col in row_19950102.index:
    if col != "dateprice" and row_19950102[col] == -1:
        cols_to_remove.append(col)

print("Dropping columns:", cols_to_remove)

# 4) Drop those columns
df.drop(columns=cols_to_remove, inplace=True)



row_19950102 = df[df["dateprice"] == "2025-03-13"]
if row_19950102.empty:
    raise ValueError("No row found for dateprice == 2025-03-13!")
row_19950102 = row_19950102.iloc[0]

# 3) Identify columns that have -1 on that date
cols_to_remove = []
for col in row_19950102.index:
    if col != "dateprice" and row_19950102[col] == -1:
        cols_to_remove.append(col)

print("Dropping columns:", cols_to_remove)

# 4) Drop those columns
df.drop(columns=cols_to_remove, inplace=True)





df = df[df["aa"] != -1]



# df = df[(df != -1).all(axis=1)]












# cols_to_keep = ["dateprice"]  # always keep this

# for col in df.columns:
#     if col == "dateprice":
#         continue  # already keeping it
#     # if column has at least one -1, we skip it; otherwise, we keep it
#     if not (df[col] == -1).any():
#         cols_to_keep.append(col)

# # 3) Filter DataFrame to keep only desired columns
# df = df[cols_to_keep]





ticker_cols = df.columns.difference(["dateprice"])
mask_80_percent = (df[ticker_cols] == -1).sum(axis=1) / len(ticker_cols) >= 0.8
df_filtered = df[~mask_80_percent]















df_filtered.to_csv("filtered_data.csv", index=False)


print("Filtered CSV saved as 'filtered_data.csv'.")
