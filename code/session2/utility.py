import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def make_max_water_by_temp_dataframe():
    # saturation pressure
    # ps = 610.78 *exp( t / ( t + 238.3 ) *17.2694 )
    # via https://www.conservationphysics.org/atmcalc/atmoclc1.html
    temperatures = np.arange(0, 31, 0.1)
    # note we can only calculate the correct 100% saturated water content for positive temperatures
    if not (temperatures >= 0).all():
        raise ValueError(
            f"Some temperatures e.g. {temperatures.min()} are negative but our formula is only correct for >= 0degC"
        )
    saturation_pressures = 560.78 * np.exp(
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


def load_data(filename):
    df = pd.read_csv(filename, parse_dates=True)

    # check for the badness from data supplier
    # we check that these columns are hard to read (that's the supplier's fault!)
    cols = [
        "Timestamp\xa0for\xa0sample\xa0frequency\xa0every\xa01 min\xa0min",
        " Temperature_Celsius",
        "Relative_Humidity",
    ]
    for idx, expected_col_name in enumerate(cols):
        if df.columns[idx] != expected_col_name:
            raise ValueError(
                f"Column {idx} expected to say {expected_col_name} but instead has {df.columns[idx]}"
            )

    # and then we can rename the columns to something sane
    df.columns = ["timestamp", "t_c", "rh"]

    df["timestamp"] = pd.to_datetime(df.reset_index()["timestamp"])

    df = df.set_index("timestamp")  # FIXED NO INPLACE
    print(f"Date range {df.index.min()} - {df.index.max()}")
    return df


def plot_day(df_day, day_to_choose):
    fig, axs = plt.subplots(ncols=2, figsize=(16, 6), constrained_layout=True)
    fig.suptitle(f"Temperatue & Relative Humidity for {day_to_choose}")
    ax = axs[0]
    df_day.plot(x="timestamp", y="t_c", marker="o", ax=ax)
    # title = f'Temperature over time on {day_to_choose}'
    set_common_mpl_styles(ax, ylabel="Temperature $^oC$", grid_axis="both")
    ax.set_ylim((0, 30))
    ax = axs[1]
    df_day.plot(x="timestamp", y="rh", marker="o", ax=ax)
    set_common_mpl_styles(
        ax, ylabel="Relative Humidity (30% expected minimum)", grid_axis="both"
    )
    ax.set_ylim((30, 100))


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


def make_estimated_water_plot(dfx, filename, day_to_choose):
    fig, axs = plt.subplots(constrained_layout=True, figsize=(12, 8), nrows=3)
    ax = axs[0]

    dfx = dfx.copy().rename(columns={"t_c": "temperature_C"})
    line_temp = dfx["temperature_C"].plot(ylabel="Temperature C", ax=ax, marker="o")
    title = f"Estimated moisture in house air on {day_to_choose}\n{filename}"
    set_common_mpl_styles(
        ax, grid_axis="both", title=title, ymin=0, legend=False, xlabel=""
    )
    ax.set_ylim((14, 22))  # sensible internal temperature range

    ax = axs[1]
    dfx["rh"].plot(
        ylabel="Relative Humidify (%)", c="orange", marker="o", ax=ax, xlabel=""
    )
    set_common_mpl_styles(ax, grid_axis="both", legend=False)
    ax.set_ylim((55, 75))  # sensible internal RH range

    ax = axs[2]
    dfx["est_water_gm3"].plot(ylabel="Temperature C", c="green", marker="s", ax=ax)
    ax.set_ylabel("Estimated water content (grams per $m^3$)")
    set_common_mpl_styles(ax, grid_axis="both", legend=False)
    ax.set_ylim((7, 12))  # sensible internal moisture range


def make_bootstrap(temperatures):
    # reproducible bootstrap version with fixed seed
    rng = np.random.default_rng(0)  # seed of 0
    # NOTE this will give the exact same results on every run
    # which might not be what we want in a bigger research project
    bootstrap_statistics = []
    # NOTE in a research project maybe we want >100 runs?
    for n in range(100):
        mask = rng.integers(0, temperatures.shape, temperatures.shape)
        bootstrap_sample = temperatures[mask]
        bootstrap_statistics.append(bootstrap_sample.mean())

    bootstrap_statistics = sorted(bootstrap_statistics)
    bootstrap_statistics = np.array(bootstrap_statistics)
    pc_lower_idx = int(bootstrap_statistics.shape[0] * 0.05)
    pc_mid_idx = int(bootstrap_statistics.shape[0] * 0.5)
    pc_higher_idx = int(bootstrap_statistics.shape[0] * 0.95)
    pc_lower = bootstrap_statistics[pc_lower_idx]
    pc_mid = bootstrap_statistics[pc_mid_idx]
    pc_higher = bootstrap_statistics[pc_higher_idx]
    return bootstrap_statistics, pc_lower, pc_mid, pc_higher


def make_bin_edges(desc, left_inf=True, right_inf=True):
    """Given bin description (e.g. "1 2 ... 10") make a sequence bounded by Infs
    desc=='0 1 ... 5' -> [-np.inf, 0, 1, 2, 3, 4, 5, np.inf]
    desc=='5 4 ... 0' -> [np.inf, 5, 4, 3, 2, 1, 0, -np.inf]
    desc=='5 4 ... 0' -> [5, 4, 3, 2, 1, 0] if left_inf==right_inf==False"""
    # From https://github.com/ianozsvald/notes_to_self/blob/master/simpler_pandas.py

    parts = desc.split(" ")
    # hopefully we have floats, if not this will just die
    start = float(parts[0])
    step = float(parts[1]) - float(parts[0])
    end = float(parts[3])
    num = round((end - start) / step) + 1
    # print(start, end, step, num)
    bins = np.linspace(start, end, num=num)

    # concatenate infs (if needed) and the calculated bins
    items = []
    left_inf_val, right_inf_val = -np.inf, np.inf
    if step < 0:
        # if step is descending we have to make left-inf large and right-inf small
        left_inf_val, right_inf_val = np.inf, -np.inf
    if left_inf:
        items.append([left_inf_val])
    items.append(bins)
    if right_inf:
        items.append([right_inf_val])
    bins = np.concatenate(items)

    return bins
