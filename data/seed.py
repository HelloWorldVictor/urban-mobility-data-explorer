import os

import polars as pl
from dotenv import load_dotenv

load_dotenv()


DB_URI = os.getenv("DB_URI", "")
df = pl.read_csv("data/train.csv")

# first 5 rows of the dataframe
print(df.head())

# print the column names
print(df.columns)

# sumary of the dataframe
print(df.describe())

# summary show number of nulls in each column
print(df.null_count())  # <-- there are no missing or null values in the dataset


# convert the column "pickup_datetime" and "dropoff_datetime" to datetime
df = df.with_columns(
    pl.col("pickup_datetime").str.to_datetime(format="%Y-%m-%d %H:%M:%S"),
    pl.col("dropoff_datetime").str.to_datetime(format="%Y-%m-%d %H:%M:%S"),
)

print(
    df.select(["pickup_datetime", "dropoff_datetime"]).head()
)  # <-- now in the current type.


# Finally, crosscheck all types with column names
print("Column names and their data types:\n======================")
for col, dtype in zip(df.columns, df.dtypes):
    print(f"{col}: {dtype}")

# Write the dataframe to a SQL database
print("Writing to database...")
df.write_database(table_name="trips", connection=DB_URI)
print("Done!")