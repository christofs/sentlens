"""
Script to establish the average sentence length per novel, and over time, 
in the English corpus of the European Literary Text Collection (ELTeC-eng). 
"""

# === Imports

import re
import pandas as pd
import glob
from os.path import join
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pygal
from pygal.style import BlueStyle
from pygal.style import Style
import seaborn as sns

# === Functions

def get_sentlen(xmlfile): 
    """
    Calculates the average sentence length of a novel. 
    Does not calculate the length of each sentence separately. 
    Based on the level-2 encoding of ELTeC. 
    Simply counts the total number of tokens and divides this number
    by the total number of sentence boundary punctuation.     
    """
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    root = ET.parse(xmlfile).getroot()
    tokens = root.findall(".//tei:body//tei:w", ns)
    boundaries = root.findall(".//tei:body//tei:w[@n='SENT']", ns)
    avgsentlen = len(tokens) / len(boundaries)
    return avgsentlen
                
  
def save_data(data, datafile): 
    """
    Saves the sentence length data to a CSV file / table. 
    """
    data = pd.DataFrame(data).T
    #print(data.head())
    with open(datafile, "w", encoding="utf8") as outfile: 
        data.to_csv(outfile, sep=";")


def read_data(datafile): 
    with open(datafile, "r", encoding="utf8") as infile: 
        data = pd.read_csv(infile, sep=";", index_col=0)
    #print(data.head())
    return data


def plot_pandas(data):
    data.sort_values("year", ascending=True, inplace=True)
    ax = data.plot.scatter(x="year", y="avgsentlen", title="Average sentence length per novel in ELTeC-eng")
    ax.set_xlabel("Year of publication")
    ax.set_ylabel("Average sentence length")
    plt.savefig("avgsentlens_ELTeC-eng.png", dpi=300, bbox_inches="tight", pad_inches=0.2)


def plot_seaborn(data): 
    plot = sns.regplot(x="year", y="avgsentlen", data=data)
    fig = plot.get_figure()
    fig.savefig("avgsentlens+regression_ELTeC-eng.png", dpi=300)
    



def plot_pygal(data): 
    data = data.round({'avgsentlen': 2})
    mystyle = Style(
        colors=('#201f52', '#201f52', '#201f52', '#201f52', '#201f52'))
  
  
    plot = pygal.XY(show_legend = False, 
                    human_readable = True,
                    style = mystyle)
    plot.title = "Average sentence length per novel in ELTeC-eng"
    plot.x_title = "Year of publication"
    plot.y_title = "Average sentence length"
    for row in data.iterrows(): 
        label = str(row[1][0]) + " ("+ str(row[0]) + ")"
        point = [(row[1][1], row[1][2])]
        plot.add(label, point)
    plot.render_to_file("avgsentlens_ELTeC-eng.svg")



# === Main

def main(): 
    """
    Coordinates the process. 
    """
    folder = join("level2", "ENG*.xml")
    datafile = "avgsentlens_ELTeC-eng.csv"
    #data = {}
    #for xmlfile in glob.glob(folder): 
    #    idno = re.split("[\/\_]", xmlfile)[1]
    #    year = re.findall("\d\d\d\d", xmlfile)[0]
    #    author = re.split("_", xmlfile)[1][:-4]
    #    avgsentlen = get_sentlen(xmlfile)
    #    data[idno] = {"author" : author, "year" : year, "avgsentlen" : avgsentlen}
    #save_data(data, datafile)
    data = read_data(datafile)
    plot_pandas(data)
    plot_pygal(data)
    plot_seaborn(data)
        
main()
