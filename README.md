# sentlens

Sentence length in corpora of literary texts, specifically in ELTeC-eng. An analysis performed by Christof Schöch in late November, 2021. 

# Data 

The analysis is based on two corpora: 
* ELTeC-eng, The English novel collection for the ELTeC, the European Literary Text Collection, produced by the COST Action Distant Reading for European Literary History (CA16204, https://distant-reading.net), release 1.0.1 (https://doi.org/10.5281/zenodo.4662490), edited by Lou Burnard and published in April 2021. Details: https://github.com/COST-ELTeC/ELTeC-eng
* The Gutenberg Corpus as described by Martin Gerlach and Francesc Font-Clos, see: https://arxiv.org/abs/1812.08092, using a copy extracted in November 2021. 

# Analysis

Samples and analyses

* ELTeC-eng_level2: Analysis based on the linguistically-annotated version of ELTeC-eng, containing 100 novels for the period 1840–1920. Calculates the ratio between the number of sentences (detected via annotated sentence boundaries) and the number of tokens contained in each novel. 
* ELTeC-eng_level1: Analysis based on the version of ELTeC-eng without any linguistic annotation. Again, the same 100 novels from 1840–1920. Uses element.tree to extract the plain text from the XML files and spaCy to split the texts into sentences and tokens. Then, the ratio of tokens per sentence is calculated again for each novel. As expected, the results are almost identical for both ELTeC versions. 
* Gutenberg_sample1: A small sample of 100 novels from 1840–1920, meant as a direct comparison to the ELTeC texts. The method used for calculating the average sentence length per novel is the same as for ELTeC-eng level1. Results have a somewhat wider range than for ELTeC, and the trend line as somewhat differing beginnings and endings, meaning some caution is on order where data is sparse. 
* Gutenberg_sample2: A larger sample of 1000 novels from 1840–1920. Denser data and narrower confidence interval, confirms the overall trend. 
* Gutenberg_sample3: A mid-sized sample of 300 novels covering a wider range than sample2, with novels first published between 1800 and 1950. Data density is lower for 1800-1840 and for 1920-1950 than for the core period, so caution is in order there.

Visualizations

* Using seaborn, a scatterplot with a regression line is produced. The regression line is a third-degree polynomial. Good for seeing the general trend of the data. 
* Using pygal, a scatterplot with embedded metadata is produced. Good for looking at individual cases. 

