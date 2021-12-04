# sentlens

Sentence length in corpora of literary texts, specifically in ELTeC-eng and the Gutenberg Corpus. An analysis performed by Christof Schöch in late November, 2021. 

# Result in a nutshell

![](https://raw.githubusercontent.com/christofs/sentlens/main/results/Gutenberg_sample5/avgsentlens%2Bregression.png)

The largest and probably the most reliable sample is sample 5 from the Gutenberg Corpus, with 1020 works of fiction from the period 1800–1950. The regression line appears to indicate an evolution towards shorter sentences, from about 25 words per sentence in 1860 to just below 20 words per sentence in 1920, as the period with the most reliable data. See, however, the various tests described below. And, there remain some caveats with regard to dating of texts. 

# Data 

The analysis is based on two corpora: 
* ELTeC-eng, The English novel collection for the ELTeC, the European Literary Text Collection, produced by the COST Action Distant Reading for European Literary History (CA16204, https://distant-reading.net), release 1.0.1 (https://doi.org/10.5281/zenodo.4662490), edited by Lou Burnard and published in April 2021. Details: https://github.com/COST-ELTeC/ELTeC-eng
* The Gutenberg Corpus as described by Martin Gerlach and Francesc Font-Clos, see: https://arxiv.org/abs/1812.08092, using a copy extracted in November 2021. 
* For comparison's sake, and because they are readily available, ELTeC-fra, ELTeC-deu and ELTec-hun, have also been analysed. 

# Analysis

Samples and analyses

* ELTeC-eng_level2: Analysis based on the linguistically-annotated version of ELTeC-eng, containing 100 novels for the period 1840–1920. Calculates the ratio between the number of sentences (detected via annotated sentence boundaries) and the number of tokens contained in each novel. Reliable metadata. 
* ELTeC-eng_level1: Analysis based on the version of ELTeC-eng without any linguistic annotation. Again, the same 100 novels from 1840–1920. Uses element.tree to extract the plain text from the XML files and spaCy to split the texts into sentences and tokens. Then, the ratio of tokens per sentence is calculated again for each novel. As expected, the results are almost identical for both ELTeC versions. 
* Gutenberg_sample1: A small sample of 100 novels from 1840–1920, meant as a direct comparison to the ELTeC texts. Less reliable metadata: in particular, the date of publication is not recorded in the Gutenberg metadata, and a very rough estimate, basically derived as the middle year between the years of birth and death of the author, has been used. The method used for calculating the average sentence length per novel is the same as for ELTeC-eng level1. Results have a somewhat wider range than for ELTeC, and the trend line as somewhat differing beginnings and endings, meaning some caution is on order where data is sparse. 
* Gutenberg_sample2: A larger sample of 1000 novels from 1840–1920. Denser data and narrower confidence interval, confirms the overall trend. 
* Gutenberg_sample3: A mid-sized sample of 300 novels covering a wider range than sample2, with novels first published between 1800 and 1950. Data density is lower for 1800-1840 and for 1920-1950 than for the core period, so caution is in order there.
* Gutenberg_sample4: 1750-1950, with somewhat improved publication years based on Worldcat data. There remain some caveats with regard to dating of texts (the clusters at 1800 and 1900 are artefacts that need to be resolved). Data density is very weak for 1750-1800 and weak for 1920-1950. The general trend ist robust. 
* Gutenberg_sample5: yet another sample, for the years 1800-1950, with the same improved but still imperfect publication years based on Worldcat data. General trend is confirmed once more. 
* ELTeC-fra: 100 French novels from 1840-1920. Interestingly, no comparably clear trend is discernible here. 
* ELTeC-deu: 100 German novels from 1840-1920. Same trend of decreasing sentence length as in English, from about 22 words in 1840 to 15 words in 1920.
* ELTeC-hun: 100 Hungarian novels from 1840-1920. Same trend, from about 22 words in 1840 to about 15 words in 1920. 

Visualizations

* Using seaborn, a scatterplot with a regression line is produced. The regression line is a third-degree polynomial. Good for seeing the general trend of the data. 
* Using pygal, a scatterplot with embedded metadata is produced. Good for looking at individual cases. 

