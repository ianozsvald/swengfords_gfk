# STUDENTS DON'T READ ME YET!
import numpy as np
import pytest
from utility import make_max_water_by_temp_dataframe







# deliberate big gap, don't scroll down yet!











def test_make_max_water_by_temp_dataframe_SOLVED():
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


