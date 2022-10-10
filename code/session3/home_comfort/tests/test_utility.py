import pytest
import pandas as pd
import numpy as np

from src.utility import make_max_water_by_temp_dataframe
from src.utility import get_room_from_filename, concat_dedupe_sort_ts


def test_make_max_water_by_temp_dataframe():
    df_moisture = make_max_water_by_temp_dataframe()
    print(df_moisture.loc[0])
    # numbers taken from:
    # https://en.wikipedia.org/wiki/Humidity#Relationship_between_absolute-,_relative-humidity,_and_temperature
    calculated_water_at_0c = df_moisture.loc[0].to_numpy()[0]
    assert calculated_water_at_0c == pytest.approx(4.8, 0.1)
    WATER_AT_0C = 4.8
    assert calculated_water_at_0c == pytest.approx(WATER_AT_0C, 0.1)
    assert float(df_moisture.loc[0]) == pytest.approx(WATER_AT_0C, 0.1)
    # https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose.html#numpy.testing.assert_allclose
    np.testing.assert_allclose(4.8, calculated_water_at_0c, atol=0.1)

    WATER_AT_20C = 17.3
    calculated_water_at_20c = float(df_moisture.loc[20])
    assert calculated_water_at_20c == pytest.approx(WATER_AT_20C, 0.1)

    WATER_AT_30C = 30.4
    calculated_water_at_30c = float(df_moisture.loc[30])
    assert calculated_water_at_30c == pytest.approx(WATER_AT_30C, 0.1)



@pytest.mark.parametrize("filename, expected", [("Kitchen_export_202112311652.csv", "Kitchen_export"), ("First floor hall_export_202112311700.csv", "First floor hall_export"), ('room_202_202101011234.csv', 'room_202'), ("Kai's Room_export_202107070553.csv", "Kai's Room_export")])
def test_get_room_from_filename(filename, expected):
    assert get_room_from_filename(filename) == expected


def test_concat_dedupe_sort_ts():
    index1 = pd.date_range("2021-01-01T00:00", "2021-01-01T12:00", freq="H")
    df_tst1 = pd.DataFrame({'t_c': 10, 'rh': 50}, index=index1)
    assert df_tst1.shape[0] == 13, "Expecting 13 rows"

    df_tst_result = concat_dedupe_sort_ts([df_tst1])
    assert df_tst_result.shape[0] == 13, "Expecting 13 non-overlapping rows"
    assert (df_tst_result.index == df_tst_result.sort_index().index).all(), "Expecting sorted index"

    index2 = pd.date_range("2021-01-01T06:00", "2021-01-01T18:00", freq="H")
    df_tst2 = pd.DataFrame({'t_c': 10, 'rh': 50}, index=index2)
    assert df_tst2.shape[0] == 13, "Expecting 13 rows"

    df_tst_result = concat_dedupe_sort_ts([df_tst1, df_tst2])
    assert df_tst_result.shape[0] == 19, "Expecting 19 non-overlapping rows"
    assert (df_tst_result.index == df_tst_result.sort_index().index).all(), "Expecting sorted index"
