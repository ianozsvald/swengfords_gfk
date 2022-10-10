from functools import partial
from tempfile import NamedTemporaryFile
import pytest
import pandas as pd
from src.process_data import fetch_csv_data, load_data
from pandera.errors import SchemaError

# NOTE FROM IAN
# BECAUSE process_data.py WAS WELL AND TIGHTLY TESTED
# I HAD TO ITERATE ON THE FOLLOWING make_good_df
# AS MAKING UP RANDOM NUMBERS WASN'T SO EASY!

# pytest -s -l -v test_integration.p
COL_TIMESTAMP = "Timestamp\xa0for\xa0sample\xa0frequency\xa0every\xa01 min\xa0min"
COL_TEMP = " Temperature_Celsius"


def make_good_df():
    """Make a good example dataframe"""
    items = {
        COL_TIMESTAMP: ["2021-12-01 06:00", "2021-12-01 07:00"],
        COL_TEMP: [25.0, 26],
        "Relative_Humidity": [50.0, 50.0],
    }
    df = pd.DataFrame(items)
    return df


def test_good_water_estimate():
    df = make_good_df()
    with NamedTemporaryFile() as f:
        print(f"Writing to {f.name}")
        df.to_csv(f.name, index=False)

        fetch = partial(fetch_csv_data, f.name)
        df_read = load_data(fetch)
        print(df_read)
        row = df_read.query("t_c == 25").iloc[0]
        print(row)
        assert row["est_water_gm3"] == pytest.approx(11.5, 0.1)


def test_large_temp():
    df = make_good_df()
    df.loc[0, COL_TEMP] = 100  # invalid huge value
    with NamedTemporaryFile() as f:
        print(f"Writing to {f.name}")
        df.to_csv(f.name, index=False)

        fetch = partial(fetch_csv_data, f.name)
        with pytest.raises(SchemaError):
            load_data(fetch)


def test_bad_column_name():
    df = make_good_df()
    cols = list(df.columns)
    cols[0] = "timeystampy"
    df.columns = cols
    with NamedTemporaryFile() as f:
        print(f"Writing to {f.name}")
        df.to_csv(f.name, index=False)

        fetch = partial(fetch_csv_data, f.name)
        with pytest.raises(ValueError):
            load_data(fetch)
