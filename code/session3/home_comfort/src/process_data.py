import glob
import os
import pandas as pd
import pandera as pa

# import numpy as np
from functools import partial

from src.utility import add_actual_water_content, make_max_water_by_temp_dataframe

FOLDER = os.path.join("../data/raw", "*.csv")
OUT_FOLDER = "../data/processed"


def fetch_sql_data(room_key):
    """TODO as data moves from CSV from Postgres, we need to build this function"""
    # make an SQLAlchemy connect to our Postgres data
    # select all rows matching room_key in date order
    # we might need to rename the table columns to our desired columns
    # "t_c" and "rh"
    # check that timestamps is set to the dataframe's index
    # return this dataframe


def fetch_csv_data(filename):
    """Use Pandas to load a CSV, apply expected cleaning rules"""
    df_raw = pd.read_csv(filename, parse_dates=True)

    # check for the badness from data supplier
    # we check that these columns are hard to read (that's the supplier's fault!)
    cols = [
        "Timestamp\xa0for\xa0sample\xa0frequency\xa0every\xa01 min\xa0min",
        " Temperature_Celsius",
        "Relative_Humidity",
    ]
    for idx, expected_col_name in enumerate(cols):
        if df_raw.columns[idx] != expected_col_name:
            raise ValueError(
                f"Column {idx} expected to say {expected_col_name} but instead has {df_raw.columns[idx]}"
            )

    # and then we can rename the columns to something sane
    df_raw.columns = ["timestamp", "t_c", "rh"]
    df_raw["timestamp"] = pd.to_datetime(df_raw["timestamp"])
    return df_raw


def load_data(fetch_fn):
    """Load data from any source via a partial fetch_fn, return with estimated water content added"""
    df_raw = fetch_fn()  # run the partially bound function

    # check that the raw loaded data conforms to our basic schema
    min_date = pd.Timestamp("2020-01-01")
    max_date = pd.Timestamp("2022-12-31")
    # will be identified as broken data
    schema = pa.DataFrameSchema(
        {
            "timestamp": pa.Column(
                "datetime64[ns]", checks=[pa.Check.gt(min_date), pa.Check.lt(max_date)]
            ),
            "t_c": pa.Column(float, checks=[pa.Check.gt(0), pa.Check.lt(35)]),
            "rh": pa.Column(float, checks=[pa.Check.gt(0), pa.Check.lt(101)]),
        },
        ordered=True,
    )
    schema(df_raw)
    # validated_df = schema(df)
    # print(validated_df) # useful if we're debugging perhaps?

    df_raw = df_raw.set_index("timestamp")

    # now add the estimated water content and validate some more
    df_moisture = make_max_water_by_temp_dataframe()
    df_water = add_actual_water_content(df_raw, df_moisture)

    schema = pa.DataFrameSchema(
        {
            "t_c": pa.Column(float, checks=[pa.Check.gt(0), pa.Check.lt(35)]),
            "rh": pa.Column(float, checks=[pa.Check.gt(0), pa.Check.lt(101)]),
            "max_water_gm3": pa.Column(float, checks=[pa.Check.gt(0), pa.Check.lt(40)]),
            "est_water_gm3": pa.Column(float, checks=[pa.Check.gt(0), pa.Check.lt(40)]),
        },
        index=pa.Index(
            "datetime64[ns]", checks=[pa.Check.gt(min_date), pa.Check.lt(max_date)]
        ),
        ordered=True,
        strict=True,
    )  # NOTE use of strict, we want _everything_ specified here to the data-processor knows what to expect next
    # we could be even smarter and chain that est_water_gm3 is <= max_water_gm3?
    schema(df_water)

    return df_water


if __name__ == "__main__":
    # process locally stored data
    filenames = glob.glob(FOLDER)
    print(f"Processing {filenames}")

    for filename in filenames:
        fetch_fn = partial(fetch_csv_data, filename)
        df_raw = load_data(fetch_fn)
        df_30min = df_raw.resample("30min").mean()
        out_filename = os.path.join(OUT_FOLDER, filename.split("/")[-1])
        out_filename = out_filename.replace(".csv", ".pickle")
        print(f"Writing to {out_filename}")
        df_30min.to_pickle(out_filename)
