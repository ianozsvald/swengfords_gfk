import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def make_estimated_water_plot(dfx, filename, time_range):
    fig, axs = plt.subplots(constrained_layout=True, figsize=(12, 8), nrows=3)
    ax = axs[0]

    dfx = dfx.copy().rename(columns={'t_c': 'temperature_C'})
    line_temp = dfx["temperature_C"].plot(ylabel="Temperature C", ax=ax, marker='o')
    title = f"Estimated moisture in house air on {time_range}\n{filename}"
    set_common_mpl_styles(ax, grid_axis="both", title=title, ymin=0, legend=False, xlabel="")
    ax.set_ylim((10, 22)) # sensible internal temperature range

    ax = axs[1]
    dfx["rh"].plot(ylabel="Relative Humidify (%)", c="orange", marker='o', ax=ax, xlabel="")
    set_common_mpl_styles(ax, grid_axis="both", legend=False)
    ax.set_ylim((45, 75)) # sensible internal RH range

    ax = axs[2]
    dfx["est_water_gm3"].plot(ylabel="Temperature C", c="green", marker='s', ax=ax)
    ax.set_ylabel("Estimated water content (grams per $m^3$)")
    set_common_mpl_styles(ax, grid_axis="both", legend=False)
    ax.set_ylim((3, 12)) # sensible internal moisture range


def set_common_mpl_styles(
    ax,
    legend=True,
    grid_axis="y",
    ylabel=None,
    xlabel=None,
    title=None,
    ymin=None,
    xmin=None,
):
    """Nice common plot configuration
    We might use it via `fig, ax = plt.subplots(constrained_layout=True, figsize=(8, 6))`
    """
    if grid_axis is not None:
        # note b=True needs to be visible=True
        ax.grid(visible=True, which="both", axis=grid_axis)
    if legend is False:
        if ax.legend_:
            ax.legend_.remove()
    else:
        ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if title is not None:
        ax.set_title(title)
    if ymin is not None:
        ax.set_ylim(ymin=ymin)
    if xmin is not None:
        ax.set_xlim(xmin=xmin)


def make_max_water_by_temp_dataframe():
    """Build df of max water (g/m^3) in 1m^3 air at normal pressure by common temperatures"""
    # saturation pressure
    # ps = 610.78 *exp( t / ( t + 238.3 ) *17.2694 )
    # via https://www.conservationphysics.org/atmcalc/atmoclc1.html
    temperatures = np.arange(0, 31, 0.1)
    # note we can only calculate the correct 100% saturated water content for positive temperatures
    if not (temperatures >= 0).all():
        raise ValueError(
            f"Some temperatures e.g. {temperatures.min()} are negative but our formula is only correct for >= 0degC"
        )
    saturation_pressures = 610.78 * np.exp(
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


def add_actual_water_content(df, df_moisture):
    """Given govee processed data and a water content table, join the nearest water to each reading"""
    df_water = pd.merge_asof(
        df.sort_values("t_c"), df_moisture, left_on="t_c", right_index=True
    ).sort_index()
    df_water["est_water_gm3"] = df_water["max_water_gm3"] * df_water["rh"] / 100
    return df_water


def get_room_from_filename(filename):
    """Split the date and postfix from the filename e.g. abc_202101011234.csv -> abc_"""
    # note we could use a regexp here but for 2021 and 2022 the following probably works
    # just fine, as I'd not expect to have these numbers as a room descriptor
    # thought for the future "room_202_202101011234.csv" would indeed be split incorrectly
    # but since I don't number my house rooms this way, I'm not going to worry about this
    # return filename.split('202')[0]
    # being slightly obsessive I decided to worry about this, despite the fact that this
    # is not going to happen
    # this regular expression matches anything up to an underscore, followed by
    # digits until ".csv", then it returns the 0th groups of the 0th result
    # and we'd expect only 2 groups (the brackets) and 1 result
    # Useful builder: https://regex101.com/
    # Useful explainer: https://regexper.com (and copy in from the opening bracket to v)
    result = re.findall(r"(.*)_(\d.*).csv", filename)[0][0]
    return result

def concat_dedupe_sort_ts(ts_lst):
    """Take out of order dataframes which overlap, sort and deduplicate"""
    df_ts = pd.concat(ts_lst)
    non_dup = ~(df_ts.index.duplicated())
    df_ts_dedupe = df_ts[non_dup]
    #df_ts_dedupe = df_ts_dedupe.sort_index(ascending=False) # bad sort should fail a unit test
    df_ts_dedupe = df_ts_dedupe.sort_index()
    return df_ts_dedupe

