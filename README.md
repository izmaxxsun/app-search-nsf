# App Search with NSF Data
Built off of arXiv dataset and modified with NSF proposal attributes to show Elastic App Search features.

## Create Elastic Deployment
* Create an Elastic deployment, the easiest way is Elastic Cloud.
* If not using Elastic Cloud, follow instructions to enable App Search
* Note the App Search URL: ____________
* Note the App Search API Key: __________
* Create an App Search Engine

## Populate Data from Arxiv
Update [get_arxiv_data.py](get_arxiv_data.py) to specify desired search terms.

```
search = arxiv.Search(
  query = "ti:climate",
  max_results = 500,
  sort_by = arxiv.SortCriterion.SubmittedDate
)
```
Update App Search URL and set environment variable for App Search API key.

```
app_search = AppSearch("https://izmaxx-ml.ent.us-central1.gcp.cloud.es.io:9243",bearer_auth=os.environ.get('APP_SEARCH_API_KEY'))
```
## Create Data View

## Create Visualizations


To start App Search UI, run the following:
- npm install
- npm start

## Logstash 
See logstash configuration file for example of pulling Twitter data through http poller and sending it an ESS instance.

This was used to demonstrate pulling tweets related to a keyword and running NLP task of Named Entity Recognition.

## Arxiv API
See "get_arxiv_data.py" for example query syntax for retrieving data from arXiv
