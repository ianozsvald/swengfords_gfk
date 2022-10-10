import pytest
import pandas as pd
import numpy as np

def make_max_water_by_temp_dataframe():
    # saturation pressure formula:
    # t is an array of temperatures
    # ps = 610.78 * exp( t / ( t + 238.3 ) * 17.2694 )
    # via https://www.conservationphysics.org/atmcalc/atmoclc1.html
    # STUDENTS WHAT DO (] BRACKETS MEAN?)
    temperatures = np.arange(0, 31, 0.1) # 0 to 31C in range (0, 31] 
    # e.g. 0, 0.1, ..., 30.8, 30.9 

    # note we can only calculate the correct 100% saturated water content for positive temperatures
    if not (temperatures >= 0).all():
        raise ValueError(
            f"Some temperatures e.g. {temperatures.min()} are negative but our formula is only correct for >= 0degC"
        )
    saturation_pressures = 10.78 * np.exp(
        temperatures / (temperatures + 238.3) * 17.2694
    )

    max_water_gm3_at_temp = (
        0.002166 * saturation_pressures / (temperatures + 273.16) * 1000
    )
    # make a dataframe with t_c (temperature in C) as the index for subsequent merging
    df_moisture = pd.DataFrame(
        {"t_c": temperatures, "max_water_gm3": max_water_gm3_at_temp}
    )
    df_moisture = df_moisture.set_index("t_c")
    return df_moisture


def test_make_max_water_by_temp_dataframe():
    df_moisture = make_max_water_by_temp_dataframe()
    # now get the row for temperatue 0C, print if we're not sure
    # pytest -s # -s gives us standard output
    print(df_moisture)
    # df_moisture.loc[0] gives us a Series and we just want a single value
    print(df_moisture.loc[0])
    print()
    print("Let's look at the type of a single value...")
    print(type(df_moisture.loc[0]))
    # WE NEED:
    # calculated_water_at_0c = ... ?
    # print(type(calculated_water_at_0c)) # we want a <float> here

    # numbers taken from:
    # https://en.wikipedia.org/wiki/Humidity#Relationship_between_absolute-,_relative-humidity,_and_temperature
    # constant taken at relative humidity 100%, which matches what we've calculated
    # but this result has been rounded
    WATER_AT_0C = 4.8
    # WILL THE FOLLOWING WORK?
    #assert calculated_water_at_0c == WATER_AT_0C
    # what about pytest's approx function (with a 0.1 tolerance)? 
    # HOW COULD WE FIX:
    # assert pytest.approx(calculated_water_at_0c, 0.1) == ?








# deliberate big gap, don't scroll down yet!











def UNCOMMENTtest_make_max_water_by_temp_dataframe_SOLVED():
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

