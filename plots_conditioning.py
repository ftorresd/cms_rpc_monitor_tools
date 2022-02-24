#!/usr/bin/env python3


import matplotlib.pyplot as plt
import numpy as np
import csv


def plot(selected_region, selected_wheel_disk):
    x = []
    y = []

    with open("outputs.csv", "r") as csvfile:
        plots = csv.reader(csvfile, delimiter=",")
        next(plots, None)  # skip the headers

        for chamber, region, wheel_disk, dipid, average_current in plots:
            if region == selected_region and wheel_disk == selected_wheel_disk:
                x.append(chamber)
                y.append(round(float(average_current), 2))

    fig = plt.figure(figsize=(10, 20))
    # fig = plt.figure()
    ax = plt.axes()

    ax.barh(x, y, label="Average Current")
    for i, v in enumerate(y):
        ax.text(v, i - 0.1, str(v), color="black", fontweight="bold")

    ax.set_ylabel("")
    ax.set_xlabel("Average Current ($\mu$A)")
    ax.set_title("")
    ax.grid(alpha=0.4)

    fig.tight_layout()
    plt.savefig(f"currents_{selected_region}_{selected_wheel_disk}.png")
    plt.savefig(f"currents_{selected_region}_{selected_wheel_disk}.pdf")


def main():
    plot("barrel", "+2")
    plot("barrel", "+1")
    plot("barrel", "0")
    plot("barrel", "-1")
    plot("barrel", "-2")
    plot("endcap", "-4")
    plot("endcap", "-3")
    plot("endcap", "-2")
    plot("endcap", "-1")
    plot("endcap", "+1")
    plot("endcap", "+2")
    plot("endcap", "+3")
    plot("endcap", "+4")


if __name__ == "__main__":
    main()
