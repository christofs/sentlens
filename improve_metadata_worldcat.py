# Imports

import re
import json
import pandas as pd
from os.path import join
import requests
import time
from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
                


def load_metadata(metadatafile): 
    with open(metadatafile, "r", encoding="utf8") as infile: 
        metadata = pd.read_csv(infile, sep=",", index_col=0)
        metadata = metadata#.iloc[0:10,:]
    return metadata


def get_authorname(author): 
    # Get last name of author
    author = re.sub(" \(.*?\)", "", author)
    authorlist = re.split(", ", author)
    authorname = authorlist[1] + "+" + authorlist[0]
    authorname = authorname.lower()
    #print(authorname)
    return authorname


def get_titlewords(title): 
    # Get first content word in title
    title = re.split("\W+", title)
    stopwords = ["Volume"]
    title = [word for word in title if word not in stopwords]
    title = [word for word in title if len(word) > 3]
    try: 
        titlewords = title[0] +"+"+ title[1]
    except: 
        titlewords = title[0]    
    titlewords = titlewords.lower()
    #print(titlewords)
    return titlewords


def search_worldcat(authorname, titlewords): 
    querystring = str(authorname) + "+" + str(titlewords)
    url = "https://www.worldcat.org/search?q="+querystring+"&fq=&dblist=638&qt=sort&se=yr&sd=asc&qt=sort_yr_asc"
    #print(url)
    result = requests.get(url)
    time.sleep(2)
    result = result.text
    #print(result)
    allyears = re.findall("title=\"(\d\d\d\d)\"", result)
    #print(allyears)
    try: 
        firstpubyear = min(allyears)
    except: 
        print("--No year found.")
        firstpubyear = "NA"
    #print(firstpubyear)
    return firstpubyear, url


def merge_and_save_results(metadata, results): 
    #print(metadata.head())
    #print(results.head())
    mergedmetadata = metadata.join(results, how="outer")
    print(mergedmetadata.head())
    with open("augmented-metadata.csv", "w", encoding="utf8") as outfile: 
        mergedmetadata.to_csv(outfile, sep=";")
    

# === Main ===

metadatafile = join("Gutenberg_sample1", "metadata-selected-sample.csv")
#metadatafile = "metadata.csv"


def main(metadatafile): 
    metadata = load_metadata(metadatafile)
    metadata_grouped = metadata.groupby("author")
    results = {}
    for author,group in metadata_grouped: 
        print(author)
        #print(group)
        authorname = get_authorname(author)
        for item in group.iterrows():
            pgid = item[0]
            title = item[1]["title"]
            #print(pgid, author, title)
            titlewords = get_titlewords(title)
            #print(authorname, titlewords)
            firstpubyear, url = search_worldcat(authorname, titlewords)
            results[pgid] = {"firstpubyear":firstpubyear,
                             "shortauthor" : authorname,
                             "shorttitle":titlewords,
                             "worldcaturl" : url}
            #print(pgid, results[pgid])
    #print(results)
    #print(len(results))
    results = pd.DataFrame.from_dict(results, orient="index", columns=["firstpubyear",
                                                                       "shortauthor",
                                                                       "shorttitle",
                                                                       "worldcaturl"])
    merge_and_save_results(metadata, results)
        

main(metadatafile)
