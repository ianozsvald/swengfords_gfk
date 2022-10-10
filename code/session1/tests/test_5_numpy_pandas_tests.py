import numpy as np
import pandas as pd

# BONUS this one will bend your mind, don't be annoyed if you have to 
# switch to the solution folder - this is deliberately hard to read
# but do have a crack at it!


def calculate_a_thing(inputs):
    outputs = np.sin(inputs)
    return outputs


def test_numpy():
    inputs = np.array([0, np.pi / 2, np.pi], dtype=np.double)
    expected_outputs = [0, 1, 0]  # note Python list, not a numpy array
    outputs = calculate_a_thing(inputs)

    # this will fail - why? what _two_ problems might we have?
    assert expected_outputs == outputs
    # you might try the following, it still fails
    # and you might add `-v` as a verbose flag to pytest
    # to get a bit more context
    # assert (expected_outputs == outputs).all()

    # solution:
    # google for 'numpy testing' and choose an appropriate method


DATES = [
    pd.to_datetime(d) for d in ["2019-01-01", "2019-01-01", "2019-01-02", "2019-01-04"]
]


def count_events_by_days(df):
    df = df.resample("d").sum()
    return df


def test_pandas():
    df = pd.DataFrame({"events": [1, 0, 2, 3]}, index=DATES)
    print(df)  # use -s in pytest to show stdout
    # you might try adding `breakpoint()` here to practice nagivating
    # with the pdb Python debugging
    # breakpoint()
    # for breakpoint() try `list` to show where you are, `c` for continue, `n` for next statement
    # `p df` will print the df
    # `whatis df` will print the item's type
    # note that `s` steps into a function and then you'll be walking through lots of pandas (so use `c` to continue out)
    df = count_events_by_days(df)

    # STUDENT - ARE THESE COUNTS RIGHT? DID WE MAKE A TYPO HERE PERHAPS?
    expected_counts = [1, 1, 0, 3]
    assert (df.events == expected_counts).all()

    # what if we use the Pandas methods rather than the more permissive
    # Python methods?
    # we can setup an expected index along with a series
    # you'll need to fix the expected_counts bug above first (we need the right counts here too)
    # and you'll have at least one bug when making the expected_counts_series
    expected_index = pd.date_range("2019-01-01", periods=4, freq="d")
    expected_counts_series = pd.Series(expected_counts, index=expected_index)
    pd.testing.assert_series_equal(df.events, expected_counts_series)
