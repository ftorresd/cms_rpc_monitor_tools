#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import numpy as np
import csv

import mplhep as hep


# MWGR 2022
chambers_off = [
    "W+2_RB3-_S01",
    "W+2_RB1out_S04",
    "W+2_RB1in_S05",
    "W+2_RB2in_S05",
    "W+2_RB3-_S06",
    "W+2_RB2in_S08",
    "W+2_RB3-_S09",
    "W+2_RB3+_S10",
    "W+2_RB3-_S11",
    "W+2_RB3-_S12",
    "W+2_RB3+_S12",
    "W+1_RB2out_S03",
    "W+1_RB4--_S04",
    "W+1_RB4-_S04",
    "W+1_RB4++_S04",
    "W+1_RB1out_S05",
    "W+1_RB3+_S07",
    "W+1_RB1out_S08",
    "W+1_RB3+_S08",
    "W+1_RB4-_S10",
    "W-1_RB2in_S01",
    "W-1_RB2out_S01",
    "W-1_RB1in_S02",
    "W-1_RB1out_S02",
    "W-1_RB3-_S02",
    "W-1_RB3+_S02",
    "W-1_RB4-_S02",
    "W-1_RB4+_S02",
    "W-1_RB3+_S03",
    "W-1_RB4-_S03",
    "W-1_RB3-_S04",
    "W-1_RB3+_S04",
    "W-1_RB4--_S04",
    "W-1_RB4-_S04",
    "W-1_RB3-_S05",
    "W-1_RB3+_S05",
    "W-1_RB3-_S06",
    "W-1_RB3+_S06",
    "W-1_RB2out_S07",
    "W-1_RB1in_S08",
    "W-1_RB1out_S08",
    "W-1_RB3-_S09",
    "W-1_RB3+_S09",
    "W-1_RB1in_S10",
    "W-1_RB1out_S10",
    "W-1_RB3-_S10",
    "W-1_RB3+_S10",
    "W-1_RB4+_S10",
    "W-1_RB1in_S11",
    "W-1_RB1out_S11",
    "W-1_RB3-_S11",
    "W-2_RB2in_S01",
    "W-2_RB2out_S01",
    "W-2_RB3+_S03",
    "W-2_RB2in_S04",
    "W-2_RB2out_S04",
    "W-2_RB4--_S04",
    "W-2_RB4-_S04",
    "W-2_RB4+_S04",
    "W-2_RB4++_S04",
    "W-2_RB2in_S06",
    "W-2_RB3-_S06",
    "W-2_RB3+_S06",
    "W-2_RB1in_S07",
    "W-2_RB1out_S08",
    "W-2_RB3+_S08",
    "W-2_RB1out_S09",
    "W-2_RB3-_S10",
    "W-2_RB3+_S10",
    "W-2_RB3-_S11",
    "W0_RB3-_S12",
    "W0_RB3+_S12",
    "W-1_RB3+_S12",
    "W-1_RB4-_S12",
    "W0_RB4-_S01",
    "W0_RB1in_S02",
    "W0_RB1out_S02",
    "W0_RB3+_S02",
    "W0_RB1out_S03",
    "W0_RB2out_S04",
    "W0_RB3-_S04",
    "W0_RB3+_S04",
    "W0_RB1in_S05",
    "W0_RB1out_S05",
    "W0_RB3-_S05",
    "W0_RB3+_S05",
    "W0_RB1out_S06",
    "W0_RB2in_S06",
    "W0_RB3-_S06",
    "W0_RB3+_S06",
    "W0_RB4-_S07",
    "W0_RB4+_S07",
    "W0_RB3-_S08",
    "W0_RB3+_S08",
    "W0_RB1in_S10",
    "W0_RB1out_S10",
    "W0_RB3-_S11",
    "W0_RB3+_S11",
]


def bar_plot(selected_region, selected_wheel_disk):
    x = []
    y = []

    with open("outputs/outputs.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        next(plots, None)  # skip the headers

        for chamber, region, wheel_disk, dipid, average_current in plots:
            if region == selected_region and wheel_disk == selected_wheel_disk:
                x.append(chamber)
                if chamber not in chambers_off:
                    y.append(round(float(average_current), 2))
                else:
                    y.append(0)

    fig = plt.figure(figsize=(10, 17))
    # fig = plt.figure()
    ax = plt.axes()

    ax.barh(x, y, label="Average Current")
    for i, v in enumerate(y):
        if x[i] in chambers_off:
            ax.text(v + 0.04, i - 0.2, str("HV OFF"), color="black", fontweight="bold")
        else:
            ax.text(v + 0.04, i - 0.2, str(v), color="black", fontweight="bold")

    ax.set_ylabel("")
    ax.set_xlabel("Average Current ($\mu$A)")
    ax.set_title("")
    ax.grid(alpha=0.4)

    fig.tight_layout()
    plt.savefig(f"outputs/currents_{selected_region}_{selected_wheel_disk}.png")
    plt.savefig(f"outputs/currents_{selected_region}_{selected_wheel_disk}.pdf")


def histogram():
    y_barrel = []
    y_endcap = []

    with open("outputs/outputs.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        next(plots, None)  # skip the headers

        for chamber, region, wheel_disk, dipid, average_current in plots:
            if chamber not in chambers_off:
                if region == "barrel":
                    y_barrel.append(round(float(average_current), 2))
                if region == "endcap":
                    y_endcap.append(round(float(average_current), 2))

    fig = plt.figure(figsize=(8, 6))
    # fig = plt.figure()
    ax = plt.axes()

    bins = 25
    ax.hist(
        y_barrel,
        alpha=0.6,
        bins=bins,
        label=f"Barrel\nMean: {round(np.array(y_barrel).mean(),2)} $\mu$A",
    )
    ax.hist(
        y_endcap,
        alpha=0.6,
        bins=bins,
        label=f"Endcap\nMean: {round(np.array(y_endcap).mean(),2)} $\mu$A",
    )

    ax.set_ylabel("Number of channels")
    ax.set_xlabel("Average Current ($\mu$A) @ 8000 V\nExcluding HV OFF chambers. ")
    ax.set_title("")
    ax.grid(alpha=0.4)

    ax.legend(prop={"size": 20})

    fig.tight_layout()
    plt.savefig(f"outputs/hist_currrents.png")
    plt.savefig(f"outputs/hist_currrents.pdf")


def main():
    os.system("rm -rf outsputs/* ; touch outsputs/__PLACE_HOLDER__")
    bar_plot("barrel", "+2")
    bar_plot("barrel", "+1")
    bar_plot("barrel", "0")
    bar_plot("barrel", "-1")
    bar_plot("barrel", "-2")
    bar_plot("endcap", "-4")
    bar_plot("endcap", "-3")
    bar_plot("endcap", "-2")
    bar_plot("endcap", "-1")
    bar_plot("endcap", "+1")
    bar_plot("endcap", "+2")
    bar_plot("endcap", "+3")
    bar_plot("endcap", "+4")
    hep.style.use("CMS")
    histogram()


if __name__ == "__main__":
    main()
