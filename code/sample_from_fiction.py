
# === Imports

import pandas as pd 
import numpy as np
import os
from os.path import join
import shutil


# === Functions

def read_metadata(fictionmetadatafilename): 
    with open(fictionmetadatafilename, "r", encoding="utf8") as infile: 
        data = pd.read_csv(infile, sep=";", index_col=0)
    print(data.head())
    return data
    


def filter_metadata(data, timeframe): 
    # select only texts between specific publication dates
    data = data[(data["firstpubyear"] >= timeframe[0]) & (data["firstpubyear"] <= timeframe[1])]
    # clean up
    print(data.head())
    print(data.shape)
    return data



def create_sample(data, samplesize):
    """
    Selects a random sample of relevant texts from the selected data.
    """
    datasample = data.sample(n=samplesize)
    return datasample



def save_metadata(data, samplemetadatafilename):
    with open(join(samplemetadatafilename), "w", encoding="utf8") as outfile: 
        data.to_csv(outfile) 
        


def copy_subset(datasample, origdir, destdir): 
    selids = list(datasample.index)
    selfns = [join(origdir, selid + "_text.txt") for selid in selids]
    print(len(selfns))
    #print(selfns)
    for selfn in selfns: 
        if os.path.isfile(selfn):
            shutil.copy(selfn, destdir)
            


# === Main

def main(): 
    # Parameters
    fictionmetadatafilename = join("..", "data", "Gutenberg-fiction", "metadata-fiction+worldcat.csv")
    dataset = "Gutenberg_sample5"
    origdir = join("..", "..", "..", "gutenberg", "data", "text", "")
    destdir = join("..", "data", dataset, "texts", "")
    samplemetadatafilename = join("..", "data", dataset, "metadata.csv")
    samplesize = 1050
    timeframe = [1800,1950]
    if not os.path.exists(destdir): 
        os.makedirs(destdir)
    # Create sample
    data = read_metadata(fictionmetadatafilename)
    data = filter_metadata(data, timeframe)
    datasample = create_sample(data, samplesize)
    save_metadata(datasample, samplemetadatafilename)
    copy_subset(datasample, origdir, destdir)

main()
