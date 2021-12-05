"""
Improve Worldcat and Gutenberg metadata
"""

import pandas as pd
import numpy as np


def read_metadatafile(metadatafile): 
    with open(metadatafile, "r", encoding="utf8") as infile: 
        metadata = pd.read_csv(infile, sep=";", index_col=0)
    print(metadata.head())
    return metadata


def calculate_refyear(row): 
    # if there are values for birth and death, and worldcat is between birth and death, use worldcat
    if row["year-birth"] > 0 and row["year-death"] > 0 and row["year-worldcat"] < row["year-death"] and row["year-worldcat"] > row["year-birth"]: 
        refyear = int(row["year-worldcat"])
    # otherwise, if there are values for birth and death and worldcat is more recent than death, use midlife
    elif row["year-birth"] > 0 and row["year-death"] > 0 and row["year-worldcat"] >= row["year-death"]: 
        refyear = int(np.round(row["year-birth"] + (((row["year-death"]-row["year-birth"])/2)+10)))
    # otherwise, if there are values for birth and death and worldcat is older than birth, also use midlife
    elif row["year-birth"] > 0 and row["year-death"] > 0 and row["year-worldcat"] <= row["year-birth"]: 
        refyear = int(np.round(row["year-birth"] + (((row["year-death"]-row["year-birth"])/2)+10)))
    # otherwise, regardless of birth and death, if there is a worldcat year, use it
    elif row["year-worldcat"] > 0: 
        refyear = int(row["year-worldcat"])
    # otherwise, that is if there is no worldcat year, but there is birth and death, use midlife
    elif row["year-birth"] > 0 and row["year-death"] > 0: 
        refyear = int(np.round(row["year-birth"] + (((row["year-death"]-row["year-birth"])/2)+10)))
    # otherwise, if there is only birth, use birth + 20
    elif row["year-birth"] > 0: 
        refyear = row["year-birth"]+20
    # otherwise, if there is only death, use death - 20
    elif row["year-death"] > 0: 
        refyear = row["year-death"]-20
    # otherwise, that is if there is no data at all, use 0
    else:
        refyear = int(0)       
    return refyear


def add_refyear(metadata): 
    metadata.fillna(0)
    metadata["year-ref"] = metadata.apply(lambda row: calculate_refyear(row), axis=1)
    metadata.sort_values(by="year-ref", ascending=True, inplace=True)
    return metadata


def write_metadatafile(metadata, metadatafile):     
    columns = ["title", "author", "year-birth", "year-death", "year-worldcat", "year-ref", 
               "language", "downloads", "subjects", "shortauthor", "shorttitle", "worldcaturl"]
    with open(metadatafile, "w", encoding="utf8") as outfile: 
        metadata.to_csv(outfile, sep=";", columns=columns)



def main():
    metadata = read_metadatafile("metadata-fiction+worldcat.csv") 
    metadata = add_refyear(metadata)
    write_metadatafile(metadata, "metadata-fiction+worldcat+heuristics.csv")

main()

