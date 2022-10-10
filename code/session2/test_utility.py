import numpy as np
import pytest
from utility import make_max_water_by_temp_dataframe

# GOAL - make a useful working test
# it must test that we calculate the water at 0C to match the result in wikipedia
# note we'll have a floating point representation problem
# we'll also have a Pandas Series vs float problem

# `pytest -s -l test_utility.py`
# -s gives us stdout (print statements)
# -l shows us local variables if we get a failure

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
