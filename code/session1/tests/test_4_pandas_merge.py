import pandas as pd

# QUESTION - is it "better" to use join or merge? We should discuss this
# TIP think about whether we're doing an outer/inner join - what's default for merge?

# TIP remember to try `flake8 test_4_pandas_merge.py` - does it give any advice?

DF1 = pd.DataFrame(
    {"animals": ["sheep", "cows", "chicken", "rabbits"], "code": ["a", "b", "c", "d"]}
)
DF2 = pd.DataFrame({"counts": [3, 1, 9, 2, 3]}, index=["a", "a", "b", "b", "c"])


def my_merge(df1, df2):
    """Merge by code, keep all animals, use a 0 for missing counts"""
    result = pd.merge(df1, df2, right_index=True, left_on="code").fillna(0)
    return result


def test():
    result = my_merge(DF1, DF2)
    print("After merging we get:")
    print(result)
    # check we get all the 4 animals we expect
    assert set(result["animals"].unique()) == set(
        ["sheep", "cows", "chicken", "rabbits"]
    )
