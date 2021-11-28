"""
Script to visualize the average sentence length per novel, and over time.
"""

# === Imports

import re
import pandas as pd
import glob
from os.path import join
import matplotlib.pyplot as plt
import pygal
from pygal.style import BlueStyle
from pygal.style import Style
import os
import seaborn as sns


# === Functions

def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile: 
        data = pd.read_csv(infile, sep=";", index_col=0)
    #print(data.head())
    return data



def plot_seaborn(data, dataset): 
    regplot = sns.regplot(x="year", y="avgsentlen", data=data, x_jitter=0.2, order=3, color="#117b99").set_title("Average sentence length per novel in " + dataset)
    fig = regplot.get_figure()
    plt.grid()
    fig.savefig(join(dataset, "results", "avgsentlens+regression.png"), dpi=600)
    

def plot_pygal(data, dataset): 
    data = data.round({'avgsentlen': 2})
    mystyle = Style(
        colors=('#2D882D', '#88CC88', '#55AA55', '#116611', '#004400'))
    scatterplot = pygal.XY(show_legend = False, 
                    human_readable = True,
                    style = mystyle,
                    range = (8,50),
                    show_x_guides=True)
    scatterplot.title = "Average sentence length per novel in " + dataset
    scatterplot.x_title = "Year of publication"
    scatterplot.y_title = "Average sentence length"
    for row in data.iterrows(): 
        label = str(row[1][0]) + " ("+ str(row[0]) + ")"
        point = [(row[1][1], row[1][2])]
        scatterplot.add(label, point)
    scatterplot.render_to_file(join(dataset, "results", "avgsentlens.svg"))



# === Main

def main(): 
    """
    Coordinates the process. 
    TODO: Fix interference issue when doing several datasets in a row.
    """
    # Datasets
    #datasets = ["ELTeC-eng_level1"]
    #datasets = ["ELTeC-eng_level2"]
    #datasets = ["Gutenberg_sample1"]
    #datasets = ["Gutenberg_sample2"]
    datasets = ["Gutenberg_sample3"]
    for dataset in datasets: 
        # Files, folders, data container
        datafile = join(dataset, "results", "avgsentlens.csv")
        metadatafile = join(dataset, "metadata-selected.csv")
        data = read_data(datafile)
        plot_pygal(data, dataset)
        plot_seaborn(data, dataset)
        print("Done visualizing", dataset)
        
main()
