# App-Search-Nsf

Prepared for demonstration with NSF-ICF

Built off of arXiv dataset and modified with NSF proposal attributes to show App Search features

To start App Search UI, run the following:
- npm install
- npm start

## Logstash 
See logstash configuration file for example of pulling Twitter data through http poller and sending it an ESS instance.

This was used to demonstrate pulling tweets related to a keyword and running NLP task of Named Entity Recognition.

## Arxiv API
See "get_arxiv_data.py" for example query syntax for retrieving data from arXiv
