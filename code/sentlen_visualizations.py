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



def plot_seaborn(data, dataset, filename): 
    regplot = sns.regplot(x="year", y="avgsentlen", marker=".", data=data, x_jitter=0.3, order=3, color="#117b99").set_title("Average sentence length per novel in " + dataset)
    fig = regplot.get_figure()
    plt.grid()
    fig.savefig(filename, dpi=600)
    

def plot_pygal(data, dataset, filename): 
    data = data.round({'avgsentlen': 2})
    mystyle = Style(
        colors=('#2D882D', '#88CC88', '#55AA55', '#116611', '#004400'))
    scatterplot = pygal.XY(show_legend = False, 
                    human_readable = True,
                    style = mystyle,
                    range = (5,70),
                    show_x_guides=True)
    scatterplot.title = "Average sentence length per novel in " + dataset
    scatterplot.x_title = "Year of publication"
    scatterplot.y_title = "Average sentence length"
    for row in data.iterrows(): 
        #print(row)
        #print(row[1][1], row[1][2])
        #print(row[1][0], row[0])
        point = [(row[1]["year"], row[1]["avgsentlen"])] # year, avgsentlen
        label = str(row[1][0]) + " (" + str(row[0]) + ")" # idno, author
        label = re.sub("\+", " ", label)
        scatterplot.add(label, point)
    scatterplot.render_to_file(filename)



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
    #datasets = ["Gutenberg_sample5"]
    #datasets = ["ELTeC-deu_level2"]
    #datasets = ["ELTeC-hun_level2"]
    datasets = ["Gutenberg_sample8"]
    for dataset in datasets: 
        # Files, folders, data container
        datafile = join("..", "results", dataset, "avgsentlens.csv")
        metadatafile = join(".:", "data", dataset, "metadata.csv")
        filename_sns = join("..", "results", dataset, "avgsentlens+regression.png")
        filename_pyg = join("..", "results", dataset, "avgsentlens+labels.svg")
        data = read_data(datafile)
        plot_seaborn(data, dataset, filename_sns)
        plot_pygal(data, dataset, filename_pyg)
        print("\nDone visualizing", dataset)
        
main()
