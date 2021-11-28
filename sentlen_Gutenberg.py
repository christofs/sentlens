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
import os
import spacy
from spacy.lang.en import English as eng
from spacy.tokenizer import Tokenizer as tok


# === Functions


def get_metadata(metadatafile, item, idno): 
    with open(metadatafile, "r", encoding="utf8") as infile: 
        metadata = pd.read_csv(infile, sep=",", index_col=0)
    #print(metadata.head())
    metadatum = metadata.loc[idno, item]
    return metadatum
    

def use_spacy(text, nlp, tok): 
    numtokens = len(tok(text))
    numsents = len(list(nlp(text).sents))
    return numtokens, numsents


def get_sentlen(textfile, nlp, tok): 
    """
    Calculates the average sentence length of a novel. 
    """
    with open(textfile, "r", encoding="utf8") as infile: 
        text = infile.read()
    numtokens, numsents = use_spacy(text, nlp, tok)
    avgsentlen = numtokens / numsents
    #avgsentlen = 33
    return avgsentlen
                
  
def save_data(data, datafile): 
    """
    Saves the sentence length data to a CSV file / table. 
    """
    data = pd.DataFrame(data).T
    #print(data.head())
    with open(datafile, "w", encoding="utf8") as outfile: 
        data.to_csv(outfile, sep=";")


# === Main

def main(): 
    """
    Coordinates the process. 
    """
    # Datasets
    datasets = ["Gutenberg_sample3"] # could be several
    # spaCy setup
    nlp = eng()
    nlp.add_pipe("sentencizer")
    nlp.max_length = 3000000
    tok = nlp.tokenizer
    for dataset in datasets: 
        # Files, folders, data container
        folder = join(dataset, "data", "PG*.txt")
        datafile = join(dataset, "results", "avgsentlens.csv")
        metadatafile = join(dataset, "metadata-selected-sample.csv")
        if not os.path.exists(join(dataset, "results", "")): 
            os.makedirs(join(dataset, "results", ""))
        data = {}
        # processing
        for textfile in glob.glob(folder): 
            basename,ext = re.split("\.", os.path.basename(textfile))
            idno = re.split("_", basename)[0]
            year = int(get_metadata(metadatafile, "pyearp", idno))
            author = re.split(",", get_metadata(metadatafile, "author", idno))[0]
            print(idno, year, author)
            avgsentlen = get_sentlen(textfile, nlp, tok)
            data[idno] = {"author" : author, "year" : year, "avgsentlen" : avgsentlen}
        save_data(data, datafile)
        
main()
