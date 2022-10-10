"""Be wary of default arguments and assumptions"""

import pandas as pd

DF1 = pd.DataFrame(
    {"code": ["a", "a", "b", "c", pd.NA, pd.NA, "d"], "values": [1, 2, 3, 4, 5, 5, 6]}
)


def my_groupby(df):
    """Get the size of each grouping, don't lose any data, give column a sensible name"""
    df_result = (
        df.groupby("code", dropna=False).size().to_frame().rename(columns={0: "sizes"})
    )
    return df_result


def test():
    df_result = my_groupby(DF1)
    nbr_keys = df_result.shape[0]
    print(df_result)
    print(df_result.info())

    assert nbr_keys == 5, "Expecting to see all 5 keys"
    assert df_result.columns == ["sizes"]
