import csv
from utils import sql_postgre

DB = sql_postgre.SQLP("house")

# 1) Collect all distinct dates and tickers
all_dates = DB.Query("""
    SELECT DISTINCT dateprice
    FROM public.simulator
    ORDER BY dateprice
""")
all_dates = [row[0] for row in all_dates]

all_tickers = DB.Query("""
    SELECT DISTINCT ticker
    FROM public.simulator
    ORDER BY ticker
""")
all_tickers = [row[0] for row in all_tickers]

# 2) Build a structure to hold the "pivoted" data
#    (dictionary keyed by dateprice, each value is another dict of {ticker: closeprice})
pivot_data = {}
for date_val in all_dates:
    pivot_data[date_val] = {}

# 3) Query close prices (or whichever column you want) for every (dateprice, ticker)
rows = DB.Query("""
    SELECT dateprice, ticker, closeprice::numeric
    FROM public.simulator
                where database = 'INV'
    ORDER BY dateprice, ticker
""")

# 4) Fill pivot_data
for dateprice, ticker, closeprice in rows:
    pivot_data[dateprice][ticker] = closeprice

# 5) Write out to CSV in pivoted format
with open("pivoted_simulator_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # Write header row: "dateprice" plus each ticker
    header = ["dateprice"] + all_tickers
    writer.writerow(header)
    
    # For each date, build a row with closeprice for each ticker
    for date_val in all_dates:
        row = [str(date_val)]
        for ticker in all_tickers:
            # If there is no entry for this ticker on this date, write NULL
            val = pivot_data[date_val].get(ticker, None)
            if val is None:
                row.append(-1)
            else:
                row.append(float(val))  # or just val if you prefer
        writer.writerow(row)

print("Pivoted data written to 'pivoted_simulator_data.csv'.")
